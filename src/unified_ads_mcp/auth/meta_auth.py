"""Meta Ads authentication handler - NO BROWSER FLOW.

This module provides token-based authentication for the Meta (Facebook) Ads API.
Tokens must be configured in ~/meta-ads.yaml or via environment variables.

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
from pathlib import Path
from typing import Optional

import requests
import yaml

# Meta OAuth2 endpoints
META_TOKEN_URL = "https://graph.facebook.com/v22.0/oauth/access_token"
META_GRAPH_URL = "https://graph.facebook.com/v22.0"

# Default App ID
DEFAULT_APP_ID = "779761636818489"

# Default config path
DEFAULT_CREDENTIALS_PATH = os.path.expanduser("~/meta-ads.yaml")

# Refresh tokens 7 days before expiry
TOKEN_REFRESH_BUFFER = 7 * 24 * 60 * 60


class MetaAdsAuth:
    """Handles Meta Ads token-based authentication.

    No browser flow - tokens must be pre-configured.
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
    ):
        """Initialize the Meta Ads auth handler."""
        self.config_path = config_path or os.environ.get(
            "META_ADS_CREDENTIALS",
            DEFAULT_CREDENTIALS_PATH
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

                print(f"[Meta Ads] Token refreshed! Expires in {expires_in // 86400} days", file=sys.stderr)
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
                print("[Meta Ads] Using token from META_ACCESS_TOKEN env var", file=sys.stderr)
                self._access_token = env_token
                return env_token

        # 2. Check system user token (never expires)
        system_token = config.get("system_user_token")
        if system_token and not force_refresh:
            if self._validate_token(system_token):
                print("[Meta Ads] Using system user token (never expires)", file=sys.stderr)
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
                if token_expires_at > 0 and int(time.time()) > (token_expires_at - TOKEN_REFRESH_BUFFER):
                    print("[Meta Ads] Token expiring soon, refreshing...", file=sys.stderr)
                    if app_secret:
                        refreshed = self._refresh_token(access_token, app_id, app_secret)
                        if refreshed:
                            self._access_token = refreshed
                            return refreshed

                print("[Meta Ads] Using access token from config", file=sys.stderr)
                self._access_token = access_token
                return access_token

            # Token invalid/expired - try to refresh if we have app_secret
            if app_secret:
                print("[Meta Ads] Token expired, attempting refresh...", file=sys.stderr)
                refreshed = self._refresh_token(access_token, app_id, app_secret)
                if refreshed:
                    self._access_token = refreshed
                    return refreshed

        # No valid token available
        raise RuntimeError(
            "Meta Ads: No valid access token available.\n\n"
            "To get a token:\n"
            "1. Go to https://developers.facebook.com/tools/explorer/\n"
            "2. Select your app and click 'Generate Access Token'\n"
            "3. Grant permissions: ads_management, ads_read, business_management\n"
            "4. Copy the token to ~/meta-ads.yaml:\n"
            "   access_token: \"<your-token>\"\n\n"
            "For a never-expiring token, use a System User from Business Manager."
        )

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
