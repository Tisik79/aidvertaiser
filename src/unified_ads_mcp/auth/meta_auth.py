"""Meta Ads OAuth authentication handler.

This module provides OAuth2 authentication for the Meta (Facebook) Ads API with:
    - Browser-based OAuth flow with automatic browser opening
    - Short-lived to long-lived token exchange
    - Automatic token refresh and persistent caching
    - Token validation against Meta's API
    - Config file support (~/meta-ads.yaml)

Configuration:
    Set META_ADS_CREDENTIALS env var to point to your meta-ads.yaml file,
    or place it at ~/meta-ads.yaml (default location).

    Required fields in meta-ads.yaml:
        app_id: Facebook App ID
        app_secret: Facebook App Secret (for long-lived tokens)
        access_token: (optional) Pre-existing access token
        system_user_token: (optional) Never-expiring system user token

    Or use environment variables:
        META_APP_ID: Facebook App ID
        META_APP_SECRET: Facebook App Secret
        META_ACCESS_TOKEN: Pre-existing access token
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional

import requests
import yaml

from .oauth_server import (
    start_oauth_server,
    get_meta_token,
    open_auth_url,
    save_token,
    load_token,
    clear_tokens,
)

# Meta OAuth2 endpoints
META_AUTH_URL = "https://www.facebook.com/v22.0/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/v22.0/oauth/access_token"
META_GRAPH_URL = "https://graph.facebook.com/v22.0"

# Required permissions for ads management
META_SCOPE = "ads_management,ads_read,business_management,pages_show_list,pages_read_engagement"

# Default App ID (can be overridden via environment)
DEFAULT_APP_ID = "779761636818489"

# Default config path
DEFAULT_CREDENTIALS_PATH = os.path.expanduser("~/meta-ads.yaml")

# Refresh tokens 7 days before expiry
TOKEN_REFRESH_BUFFER = 7 * 24 * 60 * 60


class MetaAdsAuth:
    """Handles Meta Ads OAuth authentication with browser flow.

    This class manages the OAuth2 flow for Meta Ads API access, including:
        - Config file support (~/meta-ads.yaml)
        - System user tokens (never expire)
        - Browser-based authentication when tokens are missing/expired
        - Short-lived to long-lived token exchange (60 days)
        - Automatic token refresh before expiry
        - Persistent token caching with config file updates

    Example:
        >>> auth = MetaAdsAuth()
        >>> access_token = auth.get_access_token()
        >>> # Use access_token with facebook-business SDK
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
    ):
        """Initialize the Meta Ads auth handler.

        Args:
            config_path: Path to meta-ads.yaml config file.
                        Defaults to META_ADS_CREDENTIALS env var or ~/meta-ads.yaml.
            app_id: Facebook App ID. Overrides config file.
            app_secret: Facebook App Secret. Overrides config file.
        """
        self.config_path = config_path or os.environ.get(
            "META_ADS_CREDENTIALS",
            DEFAULT_CREDENTIALS_PATH
        )
        self._config = self._load_config()

        # Allow overrides from parameters or env vars
        self.app_id = app_id or os.environ.get("META_APP_ID") or self._config.get("app_id", DEFAULT_APP_ID)
        self.app_secret = app_secret or os.environ.get("META_APP_SECRET") or self._config.get("app_secret", "")
        self._access_token: Optional[str] = None
        self._token_expires_at: int = self._config.get("token_expires_at", 0)

    def _load_config(self) -> dict:
        """Load Meta Ads config from YAML file.

        Returns:
            Dictionary with configuration values, or empty dict if no file.
        """
        if not os.path.exists(self.config_path):
            return {}

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return config or {}
        except Exception as e:
            print(f"[Meta Ads] Warning: Could not load config: {e}", file=sys.stderr)
            return {}

    def _save_config(self) -> None:
        """Save updated config back to YAML file."""
        if not self.config_path:
            return

        try:
            # Update config with current values
            self._config["access_token"] = self._access_token
            self._config["token_expires_at"] = self._token_expires_at
            self._config["app_id"] = self.app_id
            if self.app_secret:
                self._config["app_secret"] = self.app_secret

            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(self._config, f, default_flow_style=False)
            print(f"[Meta Ads] Config saved to {self.config_path}", file=sys.stderr)
        except Exception as e:
            print(f"[Meta Ads] Warning: Could not save config: {e}", file=sys.stderr)

    def get_access_token(self, force_refresh: bool = False) -> str:
        """Get valid Meta access token, refreshing or re-authenticating if needed.

        This method attempts to get a token in the following order:
            1. Check for system_user_token in config (never expires)
            2. Check META_ACCESS_TOKEN environment variable
            3. Try token from config file (with auto-refresh if near expiry)
            4. Try cached token from disk
            5. Fall back to browser-based OAuth flow

        Args:
            force_refresh: If True, force re-authentication via browser.

        Returns:
            A valid Meta API access token string.

        Raises:
            TimeoutError: If browser authentication times out.
            RuntimeError: If authentication fails.
        """
        if not force_refresh:
            # 1. Check for system user token (never expires)
            system_token = self._config.get("system_user_token")
            if system_token:
                if self._validate_token(system_token):
                    print("[Meta Ads] Using system user token (never expires)", file=sys.stderr)
                    self._access_token = system_token
                    return system_token
                else:
                    print("[Meta Ads] System user token is invalid", file=sys.stderr)

            # 2. Check environment variable
            env_token = os.environ.get("META_ACCESS_TOKEN")
            if env_token:
                if self._validate_token(env_token):
                    print("[Meta Ads] Using token from environment", file=sys.stderr)
                    return env_token
                else:
                    print("[Meta Ads] Environment token is invalid/expired", file=sys.stderr)

            # 3. Try token from config file
            config_token = self._config.get("access_token")
            if config_token:
                # Check if we should auto-refresh (7 days before expiry)
                if self._should_refresh_token():
                    print("[Meta Ads] Token expiring soon, attempting refresh...", file=sys.stderr)
                    refreshed = self._refresh_long_lived_token(config_token)
                    if refreshed:
                        return refreshed

                # Validate current token
                if self._validate_token(config_token):
                    print("[Meta Ads] Using token from config file", file=sys.stderr)
                    self._access_token = config_token
                    return config_token
                else:
                    print("[Meta Ads] Config token is invalid/expired", file=sys.stderr)

            # 4. Try cached token
            cached = load_token("meta")
            if cached and self._is_token_valid(cached):
                token = cached.get("access_token")
                if token and self._validate_token(token):
                    self._access_token = token
                    self._token_expires_at = cached.get("created_at", 0) + cached.get("expires_in", 0)
                    return token
                else:
                    print("[Meta Ads] Cached token is invalid/expired", file=sys.stderr)

        # 5. Need browser-based OAuth flow
        return self._browser_auth_flow()

    def _should_refresh_token(self) -> bool:
        """Check if token should be refreshed (within 7 days of expiry)."""
        if self._token_expires_at == 0:
            return False
        return int(time.time()) > (self._token_expires_at - TOKEN_REFRESH_BUFFER)

    def _refresh_long_lived_token(self, current_token: str) -> Optional[str]:
        """Refresh a long-lived token to get a new one.

        Long-lived tokens can be refreshed once per day as long as they're still valid.
        This gives you a new 60-day token.

        Args:
            current_token: The current long-lived token.

        Returns:
            New access token if refresh succeeded, None otherwise.
        """
        if not self.app_secret:
            print("[Meta Ads] Cannot refresh without app_secret", file=sys.stderr)
            return None

        try:
            response = requests.get(
                META_TOKEN_URL,
                params={
                    "grant_type": "fb_exchange_token",
                    "client_id": self.app_id,
                    "client_secret": self.app_secret,
                    "fb_exchange_token": current_token,
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                new_token = data["access_token"]
                expires_in = data.get("expires_in", 5184000)  # Default 60 days

                self._access_token = new_token
                self._token_expires_at = int(time.time()) + expires_in

                # Save updated token to config
                self._save_config()
                save_token("meta", {
                    "access_token": new_token,
                    "expires_in": expires_in,
                    "created_at": int(time.time()),
                    "token_type": "long_lived",
                })

                print(f"[Meta Ads] Token refreshed! New expiry: {expires_in // 86400} days", file=sys.stderr)
                return new_token
            else:
                error = response.json().get("error", {})
                print(f"[Meta Ads] Token refresh failed: {error.get('message', 'Unknown')}", file=sys.stderr)
        except Exception as e:
            print(f"[Meta Ads] Token refresh error: {e}", file=sys.stderr)

        return None

    def _browser_auth_flow(self) -> str:
        """Perform browser-based OAuth flow.

        Uses the implicit grant flow which returns the access token directly
        in the URL fragment. A local callback page extracts the token using
        JavaScript and posts it to our server.

        Returns:
            A valid Meta API access token string.

        Raises:
            TimeoutError: If user doesn't complete auth within 2 minutes.
            RuntimeError: If authentication fails.
        """
        port = start_oauth_server()
        redirect_uri = f"http://localhost:{port}/callback"

        # Build authorization URL (implicit grant flow)
        auth_params = {
            "client_id": self.app_id,
            "redirect_uri": redirect_uri,
            "scope": META_SCOPE,
            "response_type": "token",  # Implicit grant - token in fragment
        }
        auth_url = META_AUTH_URL + "?" + "&".join(
            f"{k}={v}" for k, v in auth_params.items()
        )

        print("\n" + "=" * 60, file=sys.stderr)
        print("[Meta Ads] Authentication required", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(f"Opening browser for authentication...", file=sys.stderr)
        print(f"If browser doesn't open, visit:\n{auth_url}", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)

        clear_tokens()
        if not open_auth_url(auth_url):
            print("[Meta Ads] Please open the URL above in your browser", file=sys.stderr)

        # Wait for callback with token
        print("[Meta Ads] Waiting for authentication...", file=sys.stderr)
        timeout = 120  # 2 minute timeout
        for i in range(timeout):
            token_data = get_meta_token()
            if token_data:
                break
            time.sleep(1)
            if i > 0 and i % 30 == 0:
                print(f"[Meta Ads] Still waiting... ({timeout - i}s remaining)", file=sys.stderr)
        else:
            raise TimeoutError(
                "Meta authentication timed out after 2 minutes. "
                "Please try again and complete the authentication in the browser."
            )

        short_lived_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 3600)

        # Exchange for long-lived token if we have app secret
        if self.app_secret:
            print("[Meta Ads] Exchanging for long-lived token...", file=sys.stderr)
            long_lived = self._exchange_for_long_lived(short_lived_token)
            if long_lived:
                token_data = long_lived
                print("[Meta Ads] Got long-lived token (60 days)", file=sys.stderr)
            else:
                print("[Meta Ads] Could not get long-lived token, using short-lived", file=sys.stderr)
        else:
            print(
                "[Meta Ads] No META_APP_SECRET set - token will expire in ~1 hour",
                file=sys.stderr
            )

        # Save token to both cache and config file
        save_token("meta", token_data)
        self._access_token = token_data["access_token"]
        self._token_expires_at = int(time.time()) + token_data.get("expires_in", 3600)
        self._save_config()

        print("[Meta Ads] Authentication successful!", file=sys.stderr)
        return self._access_token

    def _exchange_for_long_lived(self, short_token: str) -> Optional[dict]:
        """Exchange short-lived token for long-lived (60 days).

        Args:
            short_token: The short-lived access token from OAuth.

        Returns:
            Dictionary with long-lived token data, or None on failure.
        """
        try:
            response = requests.get(
                META_TOKEN_URL,
                params={
                    "grant_type": "fb_exchange_token",
                    "client_id": self.app_id,
                    "client_secret": self.app_secret,
                    "fb_exchange_token": short_token,
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "access_token": data["access_token"],
                    "expires_in": data.get("expires_in", 5184000),  # Default 60 days
                    "created_at": int(time.time()),
                    "token_type": "long_lived",
                }
            else:
                error = response.json().get("error", {})
                print(
                    f"[Meta Ads] Long-lived token exchange failed: {error.get('message', 'Unknown error')}",
                    file=sys.stderr
                )
        except Exception as e:
            print(f"[Meta Ads] Long-lived token exchange error: {e}", file=sys.stderr)

        return None

    def _is_token_valid(self, token_data: dict) -> bool:
        """Check if cached token data is still valid based on expiration.

        Args:
            token_data: Dictionary with token information.

        Returns:
            True if token hasn't expired (with 5 minute buffer).
        """
        created_at = token_data.get("created_at", 0)
        expires_in = token_data.get("expires_in", 3600)

        # Add 5 minute buffer before expiration
        expires_at = created_at + expires_in - 300
        return int(time.time()) < expires_at

    def _validate_token(self, token: str) -> bool:
        """Validate token against Meta's API.

        Makes a simple API call to verify the token is valid and has
        the required permissions.

        Args:
            token: The access token to validate.

        Returns:
            True if token is valid, False otherwise.
        """
        try:
            response = requests.get(
                f"{META_GRAPH_URL}/me",
                params={"access_token": token},
                timeout=10,
            )
            return response.status_code == 200
        except Exception as e:
            print(f"[Meta Ads] Token validation error: {e}", file=sys.stderr)
            return False

    def debug_token(self, token: Optional[str] = None) -> Optional[dict]:
        """Get detailed information about a token.

        Useful for debugging token issues.

        Args:
            token: Token to debug. Defaults to current token.

        Returns:
            Dictionary with token debug information, or None on failure.
        """
        token = token or self._access_token
        if not token:
            return None

        try:
            response = requests.get(
                f"{META_GRAPH_URL}/debug_token",
                params={
                    "input_token": token,
                    "access_token": f"{self.app_id}|{self.app_secret}" if self.app_secret else token,
                },
                timeout=10,
            )

            if response.status_code == 200:
                return response.json().get("data", {})
        except Exception as e:
            print(f"[Meta Ads] Token debug error: {e}", file=sys.stderr)

        return None

    def invalidate(self) -> None:
        """Invalidate current token, forcing re-authentication on next use."""
        self._access_token = None
        self._token_expires_at = 0

    def get_token_expiry(self) -> Optional[int]:
        """Get the expiration timestamp of the current token.

        Returns:
            Unix timestamp when token expires, or None if no token.
        """
        if self._token_expires_at > 0:
            return self._token_expires_at
        return None


# Global singleton instance
_meta_auth: Optional[MetaAdsAuth] = None


def get_meta_auth(
    config_path: Optional[str] = None,
    app_id: Optional[str] = None,
    app_secret: Optional[str] = None,
) -> MetaAdsAuth:
    """Get or create the Meta Ads auth handler singleton.

    Args:
        config_path: Optional path to meta-ads.yaml config file.
        app_id: Optional Facebook App ID (only used on first call).
        app_secret: Optional Facebook App Secret (only used on first call).

    Returns:
        The MetaAdsAuth singleton instance.
    """
    global _meta_auth

    if _meta_auth is None:
        _meta_auth = MetaAdsAuth(config_path, app_id, app_secret)

    return _meta_auth


def reset_meta_auth() -> None:
    """Reset the Meta auth singleton (useful for testing)."""
    global _meta_auth
    _meta_auth = None
