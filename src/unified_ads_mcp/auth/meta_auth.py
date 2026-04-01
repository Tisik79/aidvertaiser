"""Meta Ads authentication handler with browser-based OAuth flow.

This module provides authentication for the Meta (Facebook) Ads API with support for:
    - Loading tokens from YAML config file or environment variables
    - Browser-based OAuth flow with automatic browser opening (implicit grant)
    - Token refresh and exchange for long-lived tokens
    - Persistent token caching

Configuration:
    Set META_ADS_CREDENTIALS env var to point to your meta-ads.yaml file,
    or place it at ~/meta-ads.yaml (default location).

    Required fields in meta-ads.yaml:
        app_id: Facebook App ID
        app_secret: Facebook App Secret (for long-lived tokens)
        access_token: Access token from Graph API Explorer

    Or for never-expiring tokens:
        system_user_token: System User token from Business Manager

    Environment variables (override config file):
        META_APP_ID: Facebook App ID
        META_APP_SECRET: Facebook App Secret
        META_ACCESS_TOKEN: Access token
"""

import os
import sys
import time
from typing import Optional
from urllib.parse import urlencode

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

# Permissions required for ads management
META_SCOPES = "ads_management,ads_read,business_management"

# Default App ID
DEFAULT_APP_ID = "779761636818489"

# Default config path — unified location
from ..config import resolve_config_path
DEFAULT_CREDENTIALS_PATH = resolve_config_path("meta-ads.yaml", "META_ADS_CREDENTIALS")

# Refresh tokens 7 days before expiry
TOKEN_REFRESH_BUFFER = 7 * 24 * 60 * 60


class MetaAdsAuth:
    """Handles Meta Ads authentication with browser-based OAuth fallback.

    Supports pre-configured tokens and automatic browser OAuth flow when
    no valid token is available.
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
    ):
        """Initialize the Meta Ads auth handler."""
        self.config_path = config_path or os.environ.get(
            "META_ADS_CREDENTIALS", DEFAULT_CREDENTIALS_PATH
        )
        self.app_id = app_id or os.environ.get("META_APP_ID")
        self.app_secret = app_secret or os.environ.get("META_APP_SECRET")
        self._access_token: Optional[str] = None

    def _load_config(self) -> dict:
        """Load fresh config from YAML file."""
        if not os.path.exists(self.config_path):
            return {}

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return config or {}
        except Exception as e:
            print(f"[Meta Ads] Warning: Could not load config: {e}", file=sys.stderr)
            return {}

    def _save_config(self, config: dict) -> None:
        """Save config to YAML file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(config, f, default_flow_style=False)
        except Exception as e:
            print(f"[Meta Ads] Warning: Could not save config: {e}", file=sys.stderr)

    def _validate_token(self, token: str) -> bool:
        """Validate token against Meta's API."""
        try:
            response = requests.get(
                f"{META_GRAPH_URL}/me",
                params={"access_token": token},
                timeout=10,
            )
            return response.status_code == 200
        except Exception:
            return False

    def _refresh_token(self, token: str, app_id: str, app_secret: str) -> Optional[str]:
        """Try to refresh/exchange token for a new long-lived one."""
        try:
            response = requests.get(
                META_TOKEN_URL,
                params={
                    "grant_type": "fb_exchange_token",
                    "client_id": app_id,
                    "client_secret": app_secret,
                    "fb_exchange_token": token,
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                new_token = data.get("access_token")
                expires_in = data.get("expires_in", 5184000)

                # Update config file
                config = self._load_config()
                config["access_token"] = new_token
                config["token_expires_at"] = int(time.time()) + expires_in
                self._save_config(config)

                print(
                    f"[Meta Ads] Token refreshed! Expires in {expires_in // 86400} days",
                    file=sys.stderr,
                )
                return new_token
        except Exception as e:
            print(f"[Meta Ads] Token refresh failed: {e}", file=sys.stderr)

        return None

    def get_access_token(self, force_refresh: bool = False) -> str:
        """Get valid Meta access token.

        Checks tokens in order:
        1. Environment variable META_ACCESS_TOKEN
        2. system_user_token from config (never expires)
        3. access_token from config (with auto-refresh if needed)

        Args:
            force_refresh: If True, try to refresh the token.

        Returns:
            Valid access token.

        Raises:
            RuntimeError: If no valid token is available.
        """
        # Always load fresh config
        config = self._load_config()

        # Get app credentials
        app_id = self.app_id or config.get("app_id", DEFAULT_APP_ID)
        app_secret = self.app_secret or config.get("app_secret", "")

        # 1. Check environment variable first
        env_token = os.environ.get("META_ACCESS_TOKEN")
        if env_token and not force_refresh:
            if self._validate_token(env_token):
                print(
                    "[Meta Ads] Using token from META_ACCESS_TOKEN env var",
                    file=sys.stderr,
                )
                self._access_token = env_token
                return env_token

        # 2. Check system user token (never expires)
        system_token = config.get("system_user_token")
        if system_token and not force_refresh:
            if self._validate_token(system_token):
                print(
                    "[Meta Ads] Using system user token (never expires)",
                    file=sys.stderr,
                )
                self._access_token = system_token
                return system_token
            else:
                print("[Meta Ads] System user token is invalid", file=sys.stderr)

        # 3. Check access_token from config
        access_token = config.get("access_token")
        if access_token:
            # Check if token is valid
            if not force_refresh and self._validate_token(access_token):
                # Check if we should proactively refresh (7 days before expiry)
                token_expires_at = config.get("token_expires_at", 0)
                if token_expires_at > 0 and int(time.time()) > (
                    token_expires_at - TOKEN_REFRESH_BUFFER
                ):
                    print(
                        "[Meta Ads] Token expiring soon, refreshing...", file=sys.stderr
                    )
                    if app_secret:
                        refreshed = self._refresh_token(
                            access_token, app_id, app_secret
                        )
                        if refreshed:
                            self._access_token = refreshed
                            return refreshed

                print("[Meta Ads] Using access token from config", file=sys.stderr)
                self._access_token = access_token
                return access_token

            # Token invalid/expired - try to refresh if we have app_secret
            if app_secret:
                print(
                    "[Meta Ads] Token expired, attempting refresh...", file=sys.stderr
                )
                refreshed = self._refresh_token(access_token, app_id, app_secret)
                if refreshed:
                    self._access_token = refreshed
                    return refreshed

        # 4. Check persistent OAuth cache
        cached = load_token("meta")
        if cached and not force_refresh:
            cached_token = cached.get("access_token")
            if cached_token and self._validate_token(cached_token):
                # Check expiry
                created_at = cached.get("created_at", 0)
                expires_in = cached.get("expires_in", 3600)
                if int(time.time()) < created_at + expires_in - TOKEN_REFRESH_BUFFER:
                    print(
                        "[Meta Ads] Using cached OAuth token",
                        file=sys.stderr,
                    )
                    self._access_token = cached_token
                    return cached_token
                # Token expiring soon, try to refresh
                if app_secret:
                    refreshed = self._refresh_token(cached_token, app_id, app_secret)
                    if refreshed:
                        self._access_token = refreshed
                        return refreshed

        # 5. Fall back to browser-based OAuth flow
        print("[Meta Ads] No valid token found, starting browser OAuth flow...", file=sys.stderr)
        return self._browser_oauth_flow(app_id, app_secret)

    def _browser_oauth_flow(self, app_id: str, app_secret: str) -> str:
        """Perform browser-based OAuth flow using implicit grant.

        Opens the user's browser to Meta's OAuth consent page. Meta redirects
        back to the local callback server with the access token in the URL
        fragment. JavaScript on the callback page extracts the token and POSTs
        it to the server.

        Args:
            app_id: Facebook App ID.
            app_secret: Facebook App Secret (used to exchange for long-lived token).

        Returns:
            Valid access token.

        Raises:
            TimeoutError: If user doesn't complete auth within 2 minutes.
            RuntimeError: If no token is received from the callback.
        """
        port = start_oauth_server()
        redirect_uri = f"http://localhost:{port}/callback"

        # Build Meta OAuth URL (implicit grant - token in fragment)
        auth_params = {
            "client_id": app_id,
            "redirect_uri": redirect_uri,
            "scope": META_SCOPES,
            "response_type": "token",
        }
        auth_url = META_AUTH_URL + "?" + urlencode(auth_params)

        print("\n" + "=" * 60, file=sys.stderr)
        print("[Meta Ads] Authentication required", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("Opening browser for Meta Ads authentication...", file=sys.stderr)
        print(f"If browser doesn't open, visit:\n{auth_url}", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)

        clear_tokens()
        if not open_auth_url(auth_url):
            print(
                "[Meta Ads] Please open the URL above in your browser",
                file=sys.stderr,
            )

        # Wait for callback with access token
        print("[Meta Ads] Waiting for authentication...", file=sys.stderr)
        timeout = 120  # 2 minute timeout
        token_data = None
        for i in range(timeout):
            token_data = get_meta_token()
            if token_data:
                break
            time.sleep(1)
            if i > 0 and i % 30 == 0:
                print(
                    f"[Meta Ads] Still waiting... ({timeout - i}s remaining)",
                    file=sys.stderr,
                )
        else:
            raise TimeoutError(
                "Meta authentication timed out after 2 minutes. "
                "Please try again and complete the authentication in the browser."
            )

        access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 3600)

        # Exchange short-lived token for long-lived token if app_secret is available
        if app_secret:
            print("[Meta Ads] Exchanging for long-lived token...", file=sys.stderr)
            long_lived = self._refresh_token(access_token, app_id, app_secret)
            if long_lived:
                access_token = long_lived

        # Save to config file
        config = self._load_config()
        config["access_token"] = access_token
        config["app_id"] = app_id
        if app_secret:
            config["app_secret"] = app_secret
        # token_expires_at is set by _refresh_token for long-lived tokens
        if "token_expires_at" not in config:
            config["token_expires_at"] = int(time.time()) + expires_in
        self._save_config(config)

        # Also save to OAuth cache
        save_token("meta", {
            "access_token": access_token,
            "expires_in": expires_in,
            "created_at": int(time.time()),
        })

        self._access_token = access_token
        print("[Meta Ads] Authentication successful!", file=sys.stderr)
        return access_token

    def invalidate(self) -> None:
        """Invalidate current token."""
        self._access_token = None

    def get_token_expiry(self) -> Optional[int]:
        """Get the expiration timestamp of the current token."""
        config = self._load_config()
        return config.get("token_expires_at")


# Global singleton instance
_meta_auth: Optional[MetaAdsAuth] = None


def get_meta_auth(
    config_path: Optional[str] = None,
    app_id: Optional[str] = None,
    app_secret: Optional[str] = None,
) -> MetaAdsAuth:
    """Get or create the Meta Ads auth handler singleton."""
    global _meta_auth

    if _meta_auth is None:
        _meta_auth = MetaAdsAuth(config_path, app_id, app_secret)

    return _meta_auth


def reset_meta_auth() -> None:
    """Reset the Meta auth singleton."""
    global _meta_auth
    _meta_auth = None
