"""Google Search Console OAuth authentication handler.

Reuses the same OAuth infrastructure as Google Analytics auth,
with Search Console-specific scopes.
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

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
SEARCHCONSOLE_SCOPES = [
    "https://www.googleapis.com/auth/webmasters",
    "https://www.googleapis.com/auth/siteverification",
]


class GoogleSearchConsoleAuth:
    """Handles Google Search Console OAuth authentication with browser flow."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.environ.get(
            "GOOGLE_SEARCHCONSOLE_CREDENTIALS",
            str(Path.home() / "google-searchconsole.yaml"),
        )
        self._config = self._load_config()
        self._credentials: Optional[Credentials] = None
        self._validate_config()

    def _load_config(self) -> dict:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}

        # Fall back to google-ads.yaml for client credentials
        ads_config_path = os.environ.get(
            "GOOGLE_ADS_CREDENTIALS", str(Path.home() / "google-ads.yaml")
        )
        if not os.path.exists(ads_config_path):
            raise FileNotFoundError(
                f"No Search Console config at {self.config_path} "
                f"and no Google Ads config at {ads_config_path}."
            )

        print(
            f"[Search Console] Reading client credentials from {ads_config_path}",
            file=sys.stderr,
        )
        with open(ads_config_path, "r", encoding="utf-8") as f:
            ads_config = yaml.safe_load(f) or {}

        return {
            "client_id": ads_config.get("client_id"),
            "client_secret": ads_config.get("client_secret"),
        }

    def _validate_config(self) -> None:
        missing = [f for f in ["client_id", "client_secret"] if not self._config.get(f)]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

    @property
    def client_id(self) -> str:
        return self._config.get("client_id", "")

    @property
    def client_secret(self) -> str:
        return self._config.get("client_secret", "")

    def get_credentials(self, force_refresh: bool = False) -> Credentials:
        if not force_refresh:
            cached = load_token("google_searchconsole")
            if cached and cached.get("refresh_token"):
                expiry = None
                if cached.get("expiry"):
                    expiry = datetime.fromtimestamp(cached["expiry"], tz=timezone.utc).replace(tzinfo=None)
                elif cached.get("created_at"):
                    created = datetime.fromtimestamp(cached["created_at"], tz=timezone.utc).replace(tzinfo=None)
                    expiry = created + timedelta(hours=1)

                self._credentials = Credentials(
                    token=cached.get("access_token"),
                    refresh_token=cached.get("refresh_token"),
                    token_uri=GOOGLE_TOKEN_URL,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    scopes=SEARCHCONSOLE_SCOPES,
                    expiry=expiry,
                )

                if self._credentials.expired and self._credentials.refresh_token:
                    try:
                        self._credentials.refresh(Request())
                        self._save_credentials()
                        print("[Search Console] Token refreshed", file=sys.stderr)
                    except Exception as e:
                        print(f"[Search Console] Refresh failed: {e}", file=sys.stderr)
                        self._credentials = None

                if self._credentials:
                    return self._credentials

        return self._browser_auth_flow()

    def _browser_auth_flow(self) -> Credentials:
        port = start_oauth_server()
        redirect_uri = f"http://localhost:{port}/callback/google"

        auth_params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(SEARCHCONSOLE_SCOPES),
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",
        }
        auth_url = GOOGLE_AUTH_URL + "?" + "&".join(f"{k}={v}" for k, v in auth_params.items())

        print("\n" + "=" * 60, file=sys.stderr)
        print("[Search Console] Authentication required", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("Opening browser for authentication...", file=sys.stderr)
        print(f"If browser doesn't open, visit:\n{auth_url}", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)

        clear_tokens()
        if not open_auth_url(auth_url):
            print("[Search Console] Please open the URL above in your browser", file=sys.stderr)

        print("[Search Console] Waiting for authentication...", file=sys.stderr)
        timeout = 120
        for i in range(timeout):
            code = get_google_auth_code()
            if code:
                break
            time.sleep(1)
            if i > 0 and i % 30 == 0:
                print(f"[Search Console] Still waiting... ({timeout - i}s remaining)", file=sys.stderr)
        else:
            raise TimeoutError("Google Search Console authentication timed out.")

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
            raise RuntimeError(f"Token exchange failed: {error_data.get('error_description', token_response.text)}")

        token_data = token_response.json()
        self._credentials = Credentials(
            token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            token_uri=GOOGLE_TOKEN_URL,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=SEARCHCONSOLE_SCOPES,
        )

        self._save_credentials()
        print("[Search Console] Authentication successful!", file=sys.stderr)
        return self._credentials

    def _save_credentials(self) -> None:
        if self._credentials:
            token_data = {
                "access_token": self._credentials.token,
                "refresh_token": self._credentials.refresh_token,
                "created_at": int(time.time()),
            }
            if self._credentials.expiry:
                token_data["expiry"] = self._credentials.expiry.timestamp()
            save_token("google_searchconsole", token_data)

    def invalidate(self) -> None:
        self._credentials = None


_google_searchconsole_auth: Optional[GoogleSearchConsoleAuth] = None


def get_google_searchconsole_auth(config_path: Optional[str] = None) -> GoogleSearchConsoleAuth:
    global _google_searchconsole_auth
    if _google_searchconsole_auth is None:
        _google_searchconsole_auth = GoogleSearchConsoleAuth(config_path)
    return _google_searchconsole_auth


def reset_google_searchconsole_auth() -> None:
    global _google_searchconsole_auth
    _google_searchconsole_auth = None
