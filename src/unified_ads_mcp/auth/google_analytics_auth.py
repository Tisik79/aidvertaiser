"""Google Analytics OAuth authentication handler.

This module provides OAuth2 authentication for the Google Analytics API with support for:
    - Loading credentials from YAML config file
    - Fallback to Google Ads config for client_id/client_secret
    - Browser-based OAuth flow with automatic browser opening
    - Token refresh and persistent caching
    - Integration with google.oauth2.credentials.Credentials

Configuration:
    Set GOOGLE_ANALYTICS_CREDENTIALS env var to point to your google-analytics.yaml file,
    or place it at ~/google-analytics.yaml (default location).

    Required fields in google-analytics.yaml:
        client_id: OAuth2 client ID
        client_secret: OAuth2 client secret
        default_property_id: (optional) Default GA4 property ID
        refresh_token: (optional) Pre-existing refresh token

    If no analytics config exists, client_id and client_secret will be read from
    ~/google-ads.yaml (since they typically share the same Google Cloud project).
"""

import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import requests
import yaml
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from .oauth_server import (
    start_oauth_server,
    get_google_auth_code,
    open_auth_url,
    save_token,
    load_token,
    clear_tokens,
)

# Google OAuth2 endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
ANALYTICS_SCOPES = [
    "https://www.googleapis.com/auth/analytics.edit",
    "https://www.googleapis.com/auth/analytics.readonly",
]


class GoogleAnalyticsAuth:
    """Handles Google Analytics OAuth authentication with browser flow.

    This class manages the OAuth2 flow for Google Analytics API access, including:
        - Loading configuration from YAML files
        - Fallback to Google Ads config for shared client credentials
        - Browser-based authentication when tokens are missing/expired
        - Automatic token refresh using refresh tokens
        - Persistent token caching

    Example:
        >>> auth = GoogleAnalyticsAuth()
        >>> credentials = auth.get_credentials()
        >>> # credentials is a google.oauth2.credentials.Credentials object
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Google Analytics auth handler.

        Args:
            config_path: Path to google-analytics.yaml config file.
                        Defaults to GOOGLE_ANALYTICS_CREDENTIALS env var or ~/google-analytics.yaml.

        Raises:
            FileNotFoundError: If no config file can be found (neither analytics nor ads).
            ValueError: If config is missing required fields.
        """
        self.config_path = config_path or os.environ.get(
            "GOOGLE_ANALYTICS_CREDENTIALS",
            str(Path.home() / "google-analytics.yaml"),
        )
        self._config = self._load_config()
        self._credentials: Optional[Credentials] = None
        self._validate_config()

    def _load_config(self) -> dict:
        """Load Google Analytics config from YAML file.

        Falls back to google-ads.yaml for client_id and client_secret if the
        analytics config file doesn't exist.

        Returns:
            Dictionary with configuration values.

        Raises:
            FileNotFoundError: If neither analytics nor ads config file exists.
        """
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return config or {}

        # Fall back to google-ads.yaml for client_id and client_secret
        ads_config_path = os.environ.get(
            "GOOGLE_ADS_CREDENTIALS", str(Path.home() / "google-ads.yaml")
        )

        if not os.path.exists(ads_config_path):
            raise FileNotFoundError(
                f"Google Analytics config not found at {self.config_path} "
                f"and Google Ads config not found at {ads_config_path}. "
                "Set GOOGLE_ANALYTICS_CREDENTIALS env var or create ~/google-analytics.yaml"
            )

        print(
            f"[Google Analytics] No analytics config found, "
            f"reading client credentials from {ads_config_path}",
            file=sys.stderr,
        )

        with open(ads_config_path, "r", encoding="utf-8") as f:
            ads_config = yaml.safe_load(f) or {}

        # Only take client_id and client_secret from ads config
        return {
            "client_id": ads_config.get("client_id"),
            "client_secret": ads_config.get("client_secret"),
        }

    def _validate_config(self) -> None:
        """Validate that required config fields are present.

        Raises:
            ValueError: If required fields are missing.
        """
        required_fields = ["client_id", "client_secret"]
        missing = [f for f in required_fields if not self._config.get(f)]

        if missing:
            raise ValueError(
                f"Missing required fields in {self.config_path}: {', '.join(missing)}"
            )

    @property
    def client_id(self) -> str:
        """Get the OAuth2 client ID."""
        return self._config.get("client_id", "")

    @property
    def client_secret(self) -> str:
        """Get the OAuth2 client secret."""
        return self._config.get("client_secret", "")

    @property
    def default_property_id(self) -> Optional[str]:
        """Get the default GA4 property ID."""
        pid = self._config.get("default_property_id")
        if pid:
            return str(pid)
        return None

    def get_credentials(self, force_refresh: bool = False) -> Credentials:
        """Get valid Google credentials, refreshing or re-authenticating if needed.

        This method attempts to get credentials in the following order:
            1. Try cached credentials from disk
            2. Try using refresh_token from config
            3. Fall back to browser-based OAuth flow

        Args:
            force_refresh: If True, force re-authentication via browser.

        Returns:
            A google.oauth2.credentials.Credentials object ready for API use.

        Raises:
            TimeoutError: If browser authentication times out.
            RuntimeError: If token exchange fails.
        """
        if not force_refresh:
            # Try cached credentials first
            cached = load_token("google_analytics")
            if cached and self._is_token_valid(cached):
                # Restore expiry if available, otherwise assume expired to force refresh
                # Note: google-auth expects naive UTC datetimes for expiry
                expiry = None
                if cached.get("expiry"):
                    expiry = datetime.fromtimestamp(cached["expiry"], tz=timezone.utc).replace(tzinfo=None)
                elif cached.get("created_at"):
                    # No expiry stored - assume 1 hour lifetime, treat as expired if older
                    created = datetime.fromtimestamp(cached["created_at"], tz=timezone.utc).replace(tzinfo=None)
                    expiry = created + timedelta(hours=1)

                self._credentials = Credentials(
                    token=cached.get("access_token"),
                    refresh_token=cached.get("refresh_token"),
                    token_uri=GOOGLE_TOKEN_URL,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    scopes=ANALYTICS_SCOPES,
                    expiry=expiry,
                )

                # Refresh if access token is expired but we have refresh token
                if self._credentials.expired and self._credentials.refresh_token:
                    try:
                        self._credentials.refresh(Request())
                        self._save_credentials()
                        print(
                            "[Google Analytics] Token refreshed successfully",
                            file=sys.stderr,
                        )
                    except Exception as e:
                        print(
                            f"[Google Analytics] Token refresh failed: {e}",
                            file=sys.stderr,
                        )
                        # Fall through to browser auth
                        self._credentials = None

                if self._credentials:
                    return self._credentials

            # Check if we have refresh token in config
            config_refresh_token = self._config.get("refresh_token")
            if config_refresh_token:
                self._credentials = Credentials(
                    token=None,
                    refresh_token=config_refresh_token,
                    token_uri=GOOGLE_TOKEN_URL,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    scopes=ANALYTICS_SCOPES,
                )
                try:
                    self._credentials.refresh(Request())
                    self._save_credentials()
                    print(
                        "[Google Analytics] Using refresh token from config",
                        file=sys.stderr,
                    )
                    return self._credentials
                except Exception as e:
                    print(
                        f"[Google Analytics] Config refresh token invalid: {e}",
                        file=sys.stderr,
                    )
                    self._credentials = None

        # Need browser-based OAuth flow
        return self._browser_auth_flow()

    def _browser_auth_flow(self) -> Credentials:
        """Perform browser-based OAuth flow.

        Opens the user's browser to Google's OAuth consent page, waits for
        the callback with authorization code, then exchanges it for tokens.

        Returns:
            A google.oauth2.credentials.Credentials object.

        Raises:
            TimeoutError: If user doesn't complete auth within 2 minutes.
            RuntimeError: If token exchange fails.
        """
        port = start_oauth_server()
        redirect_uri = f"http://localhost:{port}/callback/google"

        # Build authorization URL
        auth_params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(ANALYTICS_SCOPES),
            "response_type": "code",
            "access_type": "offline",  # Required for refresh token
            "prompt": "consent",  # Force consent to get refresh token
        }
        auth_url = (
            GOOGLE_AUTH_URL
            + "?"
            + "&".join(f"{k}={v}" for k, v in auth_params.items())
        )

        print("\n" + "=" * 60, file=sys.stderr)
        print("[Google Analytics] Authentication required", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("Opening browser for authentication...", file=sys.stderr)
        print(f"If browser doesn't open, visit:\n{auth_url}", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)

        clear_tokens()
        if not open_auth_url(auth_url):
            print(
                "[Google Analytics] Please open the URL above in your browser",
                file=sys.stderr,
            )

        # Wait for callback with authorization code
        print("[Google Analytics] Waiting for authentication...", file=sys.stderr)
        timeout = 120  # 2 minute timeout
        for i in range(timeout):
            code = get_google_auth_code()
            if code:
                break
            time.sleep(1)
            if i > 0 and i % 30 == 0:
                print(
                    f"[Google Analytics] Still waiting... ({timeout - i}s remaining)",
                    file=sys.stderr,
                )
        else:
            raise TimeoutError(
                "Google authentication timed out after 2 minutes. "
                "Please try again and complete the authentication in the browser."
            )

        # Exchange authorization code for tokens
        token_response = requests.post(
            GOOGLE_TOKEN_URL,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            },
            timeout=30,
        )

        if token_response.status_code != 200:
            error_data = token_response.json() if token_response.text else {}
            error_msg = error_data.get("error_description", token_response.text)
            raise RuntimeError(f"Token exchange failed: {error_msg}")

        token_data = token_response.json()

        # Create credentials object
        self._credentials = Credentials(
            token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            token_uri=GOOGLE_TOKEN_URL,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=ANALYTICS_SCOPES,
        )

        self._save_credentials()
        print("[Google Analytics] Authentication successful!", file=sys.stderr)
        return self._credentials

    def _save_credentials(self) -> None:
        """Save current credentials to persistent cache."""
        if self._credentials:
            token_data = {
                "access_token": self._credentials.token,
                "refresh_token": self._credentials.refresh_token,
                "created_at": int(time.time()),
            }
            # Save expiry if available
            if self._credentials.expiry:
                token_data["expiry"] = self._credentials.expiry.timestamp()
            save_token("google_analytics", token_data)

    def _is_token_valid(self, token_data: dict) -> bool:
        """Check if cached token data is potentially valid.

        The token might still be expired, but if we have a refresh token,
        we can refresh it. This method checks for presence of refresh token.

        Args:
            token_data: Dictionary with token information.

        Returns:
            True if token data has a refresh token.
        """
        return token_data.get("refresh_token") is not None

    def invalidate(self) -> None:
        """Invalidate current credentials, forcing re-authentication on next use."""
        self._credentials = None


# Global singleton instance
_google_analytics_auth: Optional[GoogleAnalyticsAuth] = None


def get_google_analytics_auth(
    config_path: Optional[str] = None,
) -> GoogleAnalyticsAuth:
    """Get or create the Google Analytics auth handler singleton.

    Args:
        config_path: Optional path to config file (only used on first call).

    Returns:
        The GoogleAnalyticsAuth singleton instance.
    """
    global _google_analytics_auth

    if _google_analytics_auth is None:
        _google_analytics_auth = GoogleAnalyticsAuth(config_path)

    return _google_analytics_auth


def reset_google_analytics_auth() -> None:
    """Reset the Google Analytics auth singleton (useful for testing)."""
    global _google_analytics_auth
    _google_analytics_auth = None
