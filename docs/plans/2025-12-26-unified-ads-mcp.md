# Unified Ads MCP Server Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a single MCP server that provides full ad management for both Google Ads and Meta Ads with automatic OAuth browser-based token refresh.

**Architecture:** Unified FastMCP server with platform-specific modules. Each platform (Google, Meta) has its own auth handler and tool namespace. OAuth uses local callback server that auto-opens browser when token expires/missing.

**Tech Stack:**
- FastMCP 2.14+ for MCP server
- `google-ads` v28.4.1 for Google Ads API
- `facebook-business` v22.0 for Meta Ads API
- Python 3.12+, uv for dependency management

---

## Project Structure

```
adsmcp/
├── pyproject.toml
├── README.md
├── src/
│   └── unified_ads_mcp/
│       ├── __init__.py
│       ├── __main__.py           # Entry point
│       ├── server.py             # FastMCP server setup
│       ├── auth/
│       │   ├── __init__.py
│       │   ├── oauth_server.py   # Local callback server (shared)
│       │   ├── google_auth.py    # Google OAuth handler
│       │   └── meta_auth.py      # Meta OAuth handler
│       ├── google/
│       │   ├── __init__.py
│       │   ├── client.py         # Google Ads client factory
│       │   ├── campaigns.py      # Campaign CRUD
│       │   ├── ad_groups.py      # Ad Group CRUD
│       │   ├── ads.py            # Ad CRUD
│       │   ├── keywords.py       # Keyword management
│       │   ├── targeting.py      # Targeting options
│       │   └── reporting.py      # GAQL queries
│       └── meta/
│           ├── __init__.py
│           ├── client.py         # Meta API client factory
│           ├── campaigns.py      # Campaign CRUD
│           ├── adsets.py         # AdSet CRUD
│           ├── ads.py            # Ad CRUD
│           ├── creatives.py      # Creative management
│           ├── targeting.py      # Audience targeting
│           └── insights.py       # Reporting
└── tests/
    └── ...
```

---

## Task 1: Project Setup

**Files:**
- Create: `pyproject.toml`
- Create: `src/unified_ads_mcp/__init__.py`
- Create: `src/unified_ads_mcp/__main__.py`

**Step 1: Create pyproject.toml**

```toml
[project]
name = "unified-ads-mcp"
version = "1.0.0"
description = "Unified MCP server for Google Ads and Meta Ads management"
readme = "README.md"
requires-python = ">=3.12"
license = "MIT"

dependencies = [
    "fastmcp>=2.14.1",
    "google-ads>=28.4.0",
    "facebook-business>=22.0.0",
    "httpx>=0.28.0",
    "pyyaml>=6.0",
    "python-dotenv>=1.0.0",
]

[project.scripts]
unified-ads-mcp = "unified_ads_mcp:main"

[tool.uv]
package = true

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/unified_ads_mcp"]
```

**Step 2: Create __init__.py**

```python
"""Unified Ads MCP Server for Google Ads and Meta Ads."""
from unified_ads_mcp.server import main

__version__ = "1.0.0"
__all__ = ["main"]
```

**Step 3: Create __main__.py**

```python
"""Entry point for unified-ads-mcp."""
from unified_ads_mcp.server import main

if __name__ == "__main__":
    main()
```

**Step 4: Verify setup**

Run: `uv sync && uv run python -c "import unified_ads_mcp; print('OK')"`

---

## Task 2: OAuth Callback Server (Shared)

**Files:**
- Create: `src/unified_ads_mcp/auth/__init__.py`
- Create: `src/unified_ads_mcp/auth/oauth_server.py`

**Step 1: Create oauth_server.py**

This is the core shared OAuth callback server that handles browser-based auth for both platforms.

```python
"""Shared OAuth callback server for browser-based authentication."""
import asyncio
import json
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from typing import Optional, Callable
import time

# Token storage
_tokens: dict[str, dict] = {}
_server: Optional[HTTPServer] = None
_server_thread: Optional[threading.Thread] = None
_port: int = 8888

TOKEN_CACHE_DIR = Path.home() / ".unified-ads-mcp"


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callbacks from Google and Meta."""

    def log_message(self, format, *args):
        pass  # Suppress HTTP logs

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/callback/google":
            self._handle_google_callback(parsed)
        elif parsed.path == "/callback/meta":
            self._handle_meta_callback(parsed)
        elif parsed.path == "/callback":
            # Meta uses fragment, handle via JS redirect
            self._serve_meta_fragment_handler()
        else:
            self.send_error(404)

    def _handle_google_callback(self, parsed):
        """Handle Google OAuth callback with authorization code."""
        params = parse_qs(parsed.query)
        if "code" in params:
            _tokens["google_code"] = params["code"][0]
            self._send_success("Google Ads authentication successful!")
        elif "error" in params:
            self._send_error(f"Google auth error: {params.get('error', ['Unknown'])[0]}")
        else:
            self._send_error("No authorization code received")

    def _handle_meta_callback(self, parsed):
        """Handle Meta OAuth callback (receives token via POST from JS)."""
        # This is called by JS after extracting token from fragment
        pass

    def do_POST(self):
        """Handle POST for Meta token submission."""
        if self.path == "/callback/meta":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()
            try:
                data = json.loads(body)
                if "access_token" in data:
                    _tokens["meta"] = {
                        "access_token": data["access_token"],
                        "expires_in": data.get("expires_in", 3600),
                        "created_at": int(time.time()),
                    }
                    self._send_json({"status": "success"})
                else:
                    self._send_json({"status": "error", "message": "No token"})
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)})
        else:
            self.send_error(404)

    def _serve_meta_fragment_handler(self):
        """Serve HTML page that extracts token from URL fragment."""
        html = """<!DOCTYPE html>
<html>
<head><title>Meta Ads Authentication</title></head>
<body>
<h1>Processing authentication...</h1>
<script>
const hash = window.location.hash.substring(1);
const params = new URLSearchParams(hash);
const token = params.get('access_token');
const expiresIn = params.get('expires_in');
if (token) {
    fetch('/callback/meta', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({access_token: token, expires_in: parseInt(expiresIn) || 3600})
    }).then(() => {
        document.body.innerHTML = '<h1>Meta Ads authentication successful!</h1><p>You can close this window.</p>';
    });
} else {
    document.body.innerHTML = '<h1>Authentication failed</h1><p>No token received.</p>';
}
</script>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def _send_success(self, message: str):
        html = f"""<!DOCTYPE html>
<html><body><h1>{message}</h1><p>You can close this window.</p></body></html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def _send_error(self, message: str):
        html = f"""<!DOCTYPE html>
<html><body><h1>Authentication Error</h1><p>{message}</p></body></html>"""
        self.send_response(400)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def _send_json(self, data: dict):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


def start_oauth_server(port: int = 8888) -> int:
    """Start the OAuth callback server if not running."""
    global _server, _server_thread, _port

    if _server is not None:
        return _port

    # Find available port
    for p in range(port, port + 100):
        try:
            _server = HTTPServer(("localhost", p), OAuthCallbackHandler)
            _port = p
            break
        except OSError:
            continue
    else:
        raise RuntimeError("Could not find available port for OAuth server")

    _server_thread = threading.Thread(target=_server.serve_forever, daemon=True)
    _server_thread.start()
    return _port


def get_google_auth_code() -> Optional[str]:
    """Get the Google authorization code if available."""
    return _tokens.get("google_code")


def get_meta_token() -> Optional[dict]:
    """Get the Meta access token if available."""
    return _tokens.get("meta")


def clear_tokens():
    """Clear all stored tokens."""
    _tokens.clear()


def open_auth_url(url: str):
    """Open authentication URL in browser."""
    webbrowser.open(url)


def save_token(platform: str, token_data: dict):
    """Save token to disk cache."""
    TOKEN_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = TOKEN_CACHE_DIR / f"{platform}_token.json"
    with open(cache_file, "w") as f:
        json.dump(token_data, f)


def load_token(platform: str) -> Optional[dict]:
    """Load token from disk cache."""
    cache_file = TOKEN_CACHE_DIR / f"{platform}_token.json"
    if cache_file.exists():
        try:
            with open(cache_file) as f:
                return json.load(f)
        except:
            return None
    return None
```

---

## Task 3: Google Ads Authentication

**Files:**
- Create: `src/unified_ads_mcp/auth/google_auth.py`
- Create: `src/unified_ads_mcp/google/__init__.py`
- Create: `src/unified_ads_mcp/google/client.py`

**Step 1: Create google_auth.py**

```python
"""Google Ads OAuth authentication handler."""
import os
import time
from typing import Optional
from pathlib import Path
import yaml
import requests

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from .oauth_server import (
    start_oauth_server,
    get_google_auth_code,
    open_auth_url,
    save_token,
    load_token,
    clear_tokens,
)

# Google OAuth endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_ADS_SCOPE = "https://www.googleapis.com/auth/adwords"


class GoogleAdsAuth:
    """Handles Google Ads OAuth authentication with browser flow."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.environ.get(
            "GOOGLE_ADS_CREDENTIALS",
            str(Path.home() / "google-ads.yaml")
        )
        self._config = self._load_config()
        self._credentials: Optional[Credentials] = None

    def _load_config(self) -> dict:
        """Load Google Ads config from YAML file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Google Ads config not found at {self.config_path}. "
                "Set GOOGLE_ADS_CREDENTIALS env var or create ~/google-ads.yaml"
            )
        with open(self.config_path) as f:
            return yaml.safe_load(f)

    @property
    def developer_token(self) -> str:
        return self._config.get("developer_token", "")

    @property
    def client_id(self) -> str:
        return self._config.get("client_id", "")

    @property
    def client_secret(self) -> str:
        return self._config.get("client_secret", "")

    @property
    def login_customer_id(self) -> Optional[str]:
        return self._config.get("login_customer_id")

    def get_credentials(self, force_refresh: bool = False) -> Credentials:
        """Get valid Google credentials, refreshing or re-authenticating if needed."""
        # Try cached credentials first
        if not force_refresh:
            cached = load_token("google")
            if cached and self._is_token_valid(cached):
                self._credentials = Credentials(
                    token=cached.get("access_token"),
                    refresh_token=cached.get("refresh_token"),
                    token_uri=GOOGLE_TOKEN_URL,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
                if self._credentials.expired and self._credentials.refresh_token:
                    self._credentials.refresh(Request())
                    self._save_credentials()
                return self._credentials

        # Check if we have refresh token in config
        if self._config.get("refresh_token") and not force_refresh:
            self._credentials = Credentials(
                token=None,
                refresh_token=self._config["refresh_token"],
                token_uri=GOOGLE_TOKEN_URL,
                client_id=self.client_id,
                client_secret=self.client_secret,
            )
            self._credentials.refresh(Request())
            self._save_credentials()
            return self._credentials

        # Need browser-based OAuth flow
        return self._browser_auth_flow()

    def _browser_auth_flow(self) -> Credentials:
        """Perform browser-based OAuth flow."""
        port = start_oauth_server()
        redirect_uri = f"http://localhost:{port}/callback/google"

        auth_url = (
            f"{GOOGLE_AUTH_URL}?"
            f"client_id={self.client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"scope={GOOGLE_ADS_SCOPE}&"
            f"response_type=code&"
            f"access_type=offline&"
            f"prompt=consent"
        )

        print(f"\n[Google Ads] Opening browser for authentication...")
        print(f"If browser doesn't open, visit: {auth_url}\n")
        clear_tokens()
        open_auth_url(auth_url)

        # Wait for callback
        for _ in range(120):  # 2 minute timeout
            code = get_google_auth_code()
            if code:
                break
            time.sleep(1)
        else:
            raise TimeoutError("Google authentication timed out")

        # Exchange code for tokens
        response = requests.post(GOOGLE_TOKEN_URL, data={
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        })

        if response.status_code != 200:
            raise RuntimeError(f"Token exchange failed: {response.text}")

        token_data = response.json()
        self._credentials = Credentials(
            token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            token_uri=GOOGLE_TOKEN_URL,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        self._save_credentials()
        print("[Google Ads] Authentication successful!")
        return self._credentials

    def _save_credentials(self):
        """Save credentials to cache."""
        if self._credentials:
            save_token("google", {
                "access_token": self._credentials.token,
                "refresh_token": self._credentials.refresh_token,
                "created_at": int(time.time()),
            })

    def _is_token_valid(self, token_data: dict) -> bool:
        """Check if cached token is still valid."""
        created_at = token_data.get("created_at", 0)
        # Tokens typically last 1 hour, but refresh tokens are long-lived
        return token_data.get("refresh_token") is not None


# Global instance
_google_auth: Optional[GoogleAdsAuth] = None


def get_google_auth() -> GoogleAdsAuth:
    """Get or create the Google Ads auth handler."""
    global _google_auth
    if _google_auth is None:
        _google_auth = GoogleAdsAuth()
    return _google_auth
```

**Step 2: Create google/client.py**

```python
"""Google Ads API client factory."""
from typing import Optional
from google.ads.googleads.client import GoogleAdsClient

from ..auth.google_auth import get_google_auth

_client: Optional[GoogleAdsClient] = None


def get_google_ads_client(login_customer_id: Optional[str] = None) -> GoogleAdsClient:
    """Get a configured Google Ads client."""
    global _client

    auth = get_google_auth()
    credentials = auth.get_credentials()

    client = GoogleAdsClient(
        credentials=credentials,
        developer_token=auth.developer_token,
        login_customer_id=login_customer_id or auth.login_customer_id,
    )

    return client
```

---

## Task 4: Meta Ads Authentication

**Files:**
- Create: `src/unified_ads_mcp/auth/meta_auth.py`
- Create: `src/unified_ads_mcp/meta/__init__.py`
- Create: `src/unified_ads_mcp/meta/client.py`

**Step 1: Create meta_auth.py**

```python
"""Meta Ads OAuth authentication handler."""
import os
import time
import requests
from typing import Optional

from .oauth_server import (
    start_oauth_server,
    get_meta_token,
    open_auth_url,
    save_token,
    load_token,
    clear_tokens,
)

# Meta OAuth config
META_AUTH_URL = "https://www.facebook.com/v22.0/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/v22.0/oauth/access_token"
META_SCOPE = "ads_management,ads_read,business_management,pages_show_list,pages_read_engagement"


class MetaAdsAuth:
    """Handles Meta Ads OAuth authentication with browser flow."""

    def __init__(self):
        self.app_id = os.environ.get("META_APP_ID", "779761636818489")
        self.app_secret = os.environ.get("META_APP_SECRET", "")
        self._access_token: Optional[str] = None
        self._token_expires_at: int = 0

    def get_access_token(self, force_refresh: bool = False) -> str:
        """Get valid Meta access token, refreshing or re-authenticating if needed."""
        # Check environment variable first
        env_token = os.environ.get("META_ACCESS_TOKEN")
        if env_token and not force_refresh:
            # Validate the token
            if self._validate_token(env_token):
                return env_token

        # Try cached token
        if not force_refresh:
            cached = load_token("meta")
            if cached and self._is_token_valid(cached):
                token = cached.get("access_token")
                if self._validate_token(token):
                    self._access_token = token
                    return token

        # Need browser-based OAuth flow
        return self._browser_auth_flow()

    def _browser_auth_flow(self) -> str:
        """Perform browser-based OAuth flow."""
        port = start_oauth_server()
        redirect_uri = f"http://localhost:{port}/callback"

        auth_url = (
            f"{META_AUTH_URL}?"
            f"client_id={self.app_id}&"
            f"redirect_uri={redirect_uri}&"
            f"scope={META_SCOPE}&"
            f"response_type=token"
        )

        print(f"\n[Meta Ads] Opening browser for authentication...")
        print(f"If browser doesn't open, visit: {auth_url}\n")
        clear_tokens()
        open_auth_url(auth_url)

        # Wait for callback
        for _ in range(120):  # 2 minute timeout
            token_data = get_meta_token()
            if token_data:
                break
            time.sleep(1)
        else:
            raise TimeoutError("Meta authentication timed out")

        short_lived_token = token_data["access_token"]

        # Exchange for long-lived token if we have app secret
        if self.app_secret:
            long_lived = self._exchange_for_long_lived(short_lived_token)
            if long_lived:
                token_data = long_lived

        save_token("meta", token_data)
        self._access_token = token_data["access_token"]
        print("[Meta Ads] Authentication successful!")
        return self._access_token

    def _exchange_for_long_lived(self, short_token: str) -> Optional[dict]:
        """Exchange short-lived token for long-lived (60 days)."""
        try:
            response = requests.get(META_TOKEN_URL, params={
                "grant_type": "fb_exchange_token",
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "fb_exchange_token": short_token,
            })

            if response.status_code == 200:
                data = response.json()
                return {
                    "access_token": data["access_token"],
                    "expires_in": data.get("expires_in", 5184000),  # 60 days
                    "created_at": int(time.time()),
                }
        except Exception as e:
            print(f"[Meta] Warning: Could not exchange for long-lived token: {e}")
        return None

    def _is_token_valid(self, token_data: dict) -> bool:
        """Check if cached token is still valid."""
        created_at = token_data.get("created_at", 0)
        expires_in = token_data.get("expires_in", 3600)
        return int(time.time()) < (created_at + expires_in - 300)  # 5 min buffer

    def _validate_token(self, token: str) -> bool:
        """Validate token against Meta API."""
        try:
            response = requests.get(
                "https://graph.facebook.com/v22.0/me",
                params={"access_token": token}
            )
            return response.status_code == 200
        except:
            return False

    def invalidate(self):
        """Invalidate current token."""
        self._access_token = None
        self._token_expires_at = 0


# Global instance
_meta_auth: Optional[MetaAdsAuth] = None


def get_meta_auth() -> MetaAdsAuth:
    """Get or create the Meta Ads auth handler."""
    global _meta_auth
    if _meta_auth is None:
        _meta_auth = MetaAdsAuth()
    return _meta_auth
```

**Step 2: Create meta/client.py**

```python
"""Meta Ads API client factory."""
from typing import Optional
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

from ..auth.meta_auth import get_meta_auth

_api_initialized = False


def get_meta_api() -> FacebookAdsApi:
    """Get initialized Meta Ads API."""
    global _api_initialized

    auth = get_meta_auth()
    access_token = auth.get_access_token()

    if not _api_initialized:
        FacebookAdsApi.init(access_token=access_token)
        _api_initialized = True
    else:
        FacebookAdsApi.get_default_api().set_access_token(access_token)

    return FacebookAdsApi.get_default_api()


def get_ad_account(account_id: str) -> AdAccount:
    """Get an AdAccount object."""
    get_meta_api()  # Ensure API is initialized
    if not account_id.startswith("act_"):
        account_id = f"act_{account_id}"
    return AdAccount(account_id)
```

---

## Task 5: FastMCP Server Setup

**Files:**
- Create: `src/unified_ads_mcp/server.py`

**Step 1: Create server.py**

```python
"""Unified Ads MCP Server."""
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP(
    name="Unified Ads MCP",
    instructions="""
    Unified MCP server for Google Ads and Meta Ads management.

    Google Ads tools are prefixed with 'google_'.
    Meta Ads tools are prefixed with 'meta_'.

    Authentication happens automatically via browser when needed.
    """,
)

# Import tool modules to register them
from . import google
from . import meta


def main():
    """Run the MCP server."""
    print("Starting Unified Ads MCP Server...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
```

---

## Task 6: Google Ads Campaign Tools

**Files:**
- Create: `src/unified_ads_mcp/google/campaigns.py`

**Step 1: Create campaigns.py with full CRUD**

```python
"""Google Ads Campaign management tools."""
from typing import Any, Optional
from google.ads.googleads.errors import GoogleAdsException
from fastmcp.exceptions import ToolError

from ..server import mcp
from .client import get_google_ads_client


@mcp.tool()
def google_list_accounts() -> list[dict[str, Any]]:
    """List all accessible Google Ads accounts.

    Returns:
        List of account dictionaries with id and descriptive_name.
    """
    client = get_google_ads_client()
    customer_service = client.get_service("CustomerService")

    accessible = customer_service.list_accessible_customers()
    accounts = []

    for resource_name in accessible.resource_names:
        customer_id = resource_name.split("/")[-1]
        try:
            ga_service = client.get_service("GoogleAdsService")
            query = "SELECT customer.id, customer.descriptive_name FROM customer LIMIT 1"
            response = ga_service.search(customer_id=customer_id, query=query)
            for row in response:
                accounts.append({
                    "id": customer_id,
                    "name": row.customer.descriptive_name,
                })
        except:
            accounts.append({"id": customer_id, "name": "Unknown"})

    return accounts


@mcp.tool()
def google_list_campaigns(
    customer_id: str,
    status: Optional[str] = None,
) -> list[dict[str, Any]]:
    """List campaigns for a Google Ads account.

    Args:
        customer_id: Google Ads customer ID (digits only).
        status: Optional filter - ENABLED, PAUSED, or REMOVED.

    Returns:
        List of campaign dictionaries.
    """
    client = get_google_ads_client()
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            campaign_budget.amount_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros
        FROM campaign
    """

    if status:
        query += f" WHERE campaign.status = '{status}'"

    try:
        response = ga_service.search_stream(customer_id=customer_id, query=query)
        campaigns = []
        for batch in response:
            for row in batch.results:
                campaigns.append({
                    "id": str(row.campaign.id),
                    "name": row.campaign.name,
                    "status": row.campaign.status.name,
                    "channel_type": row.campaign.advertising_channel_type.name,
                    "budget_micros": row.campaign_budget.amount_micros,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost_micros": row.metrics.cost_micros,
                })
        return campaigns
    except GoogleAdsException as e:
        raise ToolError(str(e.failure.errors[0].message)) from e


@mcp.tool()
def google_create_campaign(
    customer_id: str,
    name: str,
    budget_amount_micros: int,
    channel_type: str = "SEARCH",
    status: str = "PAUSED",
) -> dict[str, Any]:
    """Create a new Google Ads campaign.

    Args:
        customer_id: Google Ads customer ID.
        name: Campaign name.
        budget_amount_micros: Daily budget in micros (1,000,000 = $1).
        channel_type: SEARCH, DISPLAY, VIDEO, SHOPPING, PERFORMANCE_MAX.
        status: ENABLED or PAUSED.

    Returns:
        Created campaign details with resource names.
    """
    client = get_google_ads_client()

    try:
        # Create budget
        budget_service = client.get_service("CampaignBudgetService")
        budget_op = client.get_type("CampaignBudgetOperation")
        budget = budget_op.create
        budget.name = f"{name} Budget"
        budget.amount_micros = budget_amount_micros
        budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD

        budget_response = budget_service.mutate_campaign_budgets(
            customer_id=customer_id,
            operations=[budget_op],
        )
        budget_resource = budget_response.results[0].resource_name

        # Create campaign
        campaign_service = client.get_service("CampaignService")
        campaign_op = client.get_type("CampaignOperation")
        campaign = campaign_op.create
        campaign.name = name
        campaign.campaign_budget = budget_resource
        campaign.advertising_channel_type = getattr(
            client.enums.AdvertisingChannelTypeEnum, channel_type
        )
        campaign.status = getattr(client.enums.CampaignStatusEnum, status)
        campaign.target_spend.target_spend_micros = 0

        campaign_response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[campaign_op],
        )

        return {
            "campaign_id": campaign_response.results[0].resource_name.split("/")[-1],
            "campaign_resource": campaign_response.results[0].resource_name,
            "budget_resource": budget_resource,
            "status": "created",
        }
    except GoogleAdsException as e:
        raise ToolError(str(e.failure.errors[0].message)) from e


@mcp.tool()
def google_update_campaign(
    customer_id: str,
    campaign_id: str,
    name: Optional[str] = None,
    status: Optional[str] = None,
) -> dict[str, Any]:
    """Update an existing Google Ads campaign.

    Args:
        customer_id: Google Ads customer ID.
        campaign_id: Campaign ID to update.
        name: New campaign name.
        status: New status - ENABLED, PAUSED, or REMOVED.

    Returns:
        Update confirmation.
    """
    client = get_google_ads_client()
    campaign_service = client.get_service("CampaignService")

    campaign_op = client.get_type("CampaignOperation")
    campaign = campaign_op.update
    campaign.resource_name = f"customers/{customer_id}/campaigns/{campaign_id}"

    fields = []
    if name:
        campaign.name = name
        fields.append("name")
    if status:
        campaign.status = getattr(client.enums.CampaignStatusEnum, status)
        fields.append("status")

    if not fields:
        raise ToolError("No fields to update")

    campaign_op.update_mask.paths.extend(fields)

    try:
        response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[campaign_op],
        )
        return {
            "campaign_id": campaign_id,
            "updated_fields": fields,
            "status": "updated",
        }
    except GoogleAdsException as e:
        raise ToolError(str(e.failure.errors[0].message)) from e


@mcp.tool()
def google_run_query(
    customer_id: str,
    query: str,
) -> list[dict[str, Any]]:
    """Execute a GAQL query for reporting.

    Args:
        customer_id: Google Ads customer ID.
        query: Google Ads Query Language (GAQL) query.

    Returns:
        Query results as list of dictionaries.
    """
    client = get_google_ads_client()
    ga_service = client.get_service("GoogleAdsService")

    try:
        response = ga_service.search_stream(customer_id=customer_id, query=query)
        results = []
        for batch in response:
            for row in batch.results:
                row_dict = {}
                for field in batch.field_mask.paths:
                    parts = field.split(".")
                    value = row
                    for part in parts:
                        value = getattr(value, part, None)
                        if value is None:
                            break
                    if hasattr(value, "name"):  # Enum
                        value = value.name
                    row_dict[field] = value
                results.append(row_dict)
        return results
    except GoogleAdsException as e:
        raise ToolError(str(e.failure.errors[0].message)) from e
```

---

## Task 7: Meta Ads Campaign Tools

**Files:**
- Create: `src/unified_ads_mcp/meta/campaigns.py`

**Step 1: Create campaigns.py**

```python
"""Meta Ads Campaign management tools."""
from typing import Any, Optional
import json
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.exceptions import FacebookRequestError

from ..server import mcp
from .client import get_meta_api, get_ad_account


@mcp.tool()
def meta_list_accounts() -> list[dict[str, Any]]:
    """List all accessible Meta Ads accounts.

    Returns:
        List of ad account dictionaries.
    """
    api = get_meta_api()

    try:
        from facebook_business.adobjects.user import User
        me = User(fbid="me")
        accounts = me.get_ad_accounts(fields=[
            "id", "name", "account_status", "currency", "amount_spent"
        ])

        return [
            {
                "id": acc["id"],
                "name": acc.get("name", "Unknown"),
                "status": acc.get("account_status"),
                "currency": acc.get("currency"),
                "amount_spent": acc.get("amount_spent"),
            }
            for acc in accounts
        ]
    except FacebookRequestError as e:
        from ..auth.meta_auth import get_meta_auth
        # Token might be expired - trigger re-auth
        auth = get_meta_auth()
        auth.invalidate()
        raise


@mcp.tool()
def meta_list_campaigns(
    account_id: str,
    status: Optional[str] = None,
    limit: int = 25,
) -> list[dict[str, Any]]:
    """List campaigns for a Meta Ads account.

    Args:
        account_id: Meta Ads account ID (with or without act_ prefix).
        status: Optional filter - ACTIVE, PAUSED, DELETED, ARCHIVED.
        limit: Maximum results to return.

    Returns:
        List of campaign dictionaries.
    """
    account = get_ad_account(account_id)

    params = {"limit": limit}
    if status:
        params["effective_status"] = [status]

    campaigns = account.get_campaigns(
        fields=[
            "id", "name", "status", "objective",
            "daily_budget", "lifetime_budget",
            "created_time", "updated_time"
        ],
        params=params,
    )

    return [
        {
            "id": c["id"],
            "name": c["name"],
            "status": c["status"],
            "objective": c.get("objective"),
            "daily_budget": c.get("daily_budget"),
            "lifetime_budget": c.get("lifetime_budget"),
        }
        for c in campaigns
    ]


@mcp.tool()
def meta_create_campaign(
    account_id: str,
    name: str,
    objective: str,
    status: str = "PAUSED",
    daily_budget: Optional[int] = None,
    lifetime_budget: Optional[int] = None,
    special_ad_categories: Optional[list[str]] = None,
) -> dict[str, Any]:
    """Create a new Meta Ads campaign.

    Args:
        account_id: Meta Ads account ID.
        name: Campaign name.
        objective: OUTCOME_AWARENESS, OUTCOME_TRAFFIC, OUTCOME_ENGAGEMENT,
                   OUTCOME_LEADS, OUTCOME_SALES, OUTCOME_APP_PROMOTION.
        status: ACTIVE or PAUSED.
        daily_budget: Daily budget in cents.
        lifetime_budget: Lifetime budget in cents.
        special_ad_categories: List of categories if applicable (HOUSING, CREDIT, etc.)

    Returns:
        Created campaign details.
    """
    account = get_ad_account(account_id)

    params = {
        "name": name,
        "objective": objective,
        "status": status,
        "special_ad_categories": special_ad_categories or [],
    }

    if daily_budget:
        params["daily_budget"] = daily_budget
    if lifetime_budget:
        params["lifetime_budget"] = lifetime_budget

    campaign = account.create_campaign(params=params)

    return {
        "id": campaign["id"],
        "name": name,
        "objective": objective,
        "status": status,
    }


@mcp.tool()
def meta_update_campaign(
    campaign_id: str,
    name: Optional[str] = None,
    status: Optional[str] = None,
    daily_budget: Optional[int] = None,
) -> dict[str, Any]:
    """Update an existing Meta Ads campaign.

    Args:
        campaign_id: Campaign ID to update.
        name: New campaign name.
        status: New status - ACTIVE, PAUSED, DELETED, ARCHIVED.
        daily_budget: New daily budget in cents.

    Returns:
        Update confirmation.
    """
    campaign = Campaign(campaign_id)

    params = {}
    if name:
        params["name"] = name
    if status:
        params["status"] = status
    if daily_budget:
        params["daily_budget"] = daily_budget

    if not params:
        raise ValueError("No fields to update")

    campaign.api_update(params=params)

    return {
        "id": campaign_id,
        "updated_fields": list(params.keys()),
        "status": "updated",
    }


@mcp.tool()
def meta_get_insights(
    object_id: str,
    date_preset: str = "last_30d",
    level: str = "campaign",
) -> list[dict[str, Any]]:
    """Get performance insights for a Meta Ads object.

    Args:
        object_id: Campaign, AdSet, or Ad ID.
        date_preset: today, yesterday, last_7d, last_30d, this_month, etc.
        level: campaign, adset, or ad.

    Returns:
        List of insight dictionaries with metrics.
    """
    from facebook_business.adobjects.adsinsights import AdsInsights

    if object_id.startswith("act_"):
        obj = get_ad_account(object_id)
    else:
        # Could be campaign, adset, or ad
        obj = Campaign(object_id)

    params = {
        "date_preset": date_preset,
        "level": level,
    }

    fields = [
        "campaign_name", "impressions", "clicks", "spend",
        "cpc", "cpm", "ctr", "reach", "frequency",
        "actions", "conversions", "cost_per_action_type",
    ]

    insights = obj.get_insights(fields=fields, params=params)

    return [dict(insight) for insight in insights]
```

---

## Task 8: Register Tool Modules

**Files:**
- Update: `src/unified_ads_mcp/google/__init__.py`
- Update: `src/unified_ads_mcp/meta/__init__.py`

**Step 1: Update google/__init__.py**

```python
"""Google Ads tools."""
from . import campaigns
# Future imports:
# from . import ad_groups
# from . import ads
# from . import keywords
```

**Step 2: Update meta/__init__.py**

```python
"""Meta Ads tools."""
from . import campaigns
# Future imports:
# from . import adsets
# from . import ads
# from . import creatives
```

---

## Task 9: Update MCP Server Config

**Files:**
- Create: Config entry for ~/.claude/mcp_servers.json

**Step 1: Test the server locally**

```bash
cd /home/david/Work/Programming/adsmcp
uv sync
uv run unified-ads-mcp
```

**Step 2: Add to mcp_servers.json**

```json
{
  "unified-ads": {
    "command": "uv",
    "args": ["run", "--directory", "/home/david/Work/Programming/adsmcp", "unified-ads-mcp"],
    "env": {
      "GOOGLE_ADS_CREDENTIALS": "/home/david/google-ads.yaml",
      "META_APP_ID": "779761636818489",
      "META_APP_SECRET": "YOUR_APP_SECRET_HERE"
    }
  }
}
```

---

## Summary

This plan creates a unified MCP server with:

**Google Ads Tools:**
- `google_list_accounts` - List accessible accounts
- `google_list_campaigns` - List campaigns with metrics
- `google_create_campaign` - Create new campaigns
- `google_update_campaign` - Update campaign settings
- `google_run_query` - Execute any GAQL query

**Meta Ads Tools:**
- `meta_list_accounts` - List accessible accounts
- `meta_list_campaigns` - List campaigns with metrics
- `meta_create_campaign` - Create new campaigns
- `meta_update_campaign` - Update campaign settings
- `meta_get_insights` - Get performance reports

**Authentication:**
- Browser-based OAuth for both platforms
- Automatic token refresh
- Persistent token caching
- Long-lived token exchange for Meta

---

Plan complete and saved to `docs/plans/2025-12-26-unified-ads-mcp.md`. Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
