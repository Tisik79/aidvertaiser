"""Matomo Analytics HTTP API client.

This module provides a simple HTTP client for the Matomo API. Configuration
is loaded from ~/matomo.yaml or the path in MATOMO_CREDENTIALS env var.

Configuration (matomo.yaml):
    url: https://your-matomo-instance.com
    token_auth: your_api_token
    default_site_id: 1  # optional
"""

import os
import sys
from typing import Any, Optional

import httpx
import yaml

_CONFIG_PATH = os.environ.get(
    "MATOMO_CREDENTIALS", os.path.expanduser("~/matomo.yaml")
)

_config: Optional[dict] = None
_client: Optional[httpx.Client] = None


def _load_config() -> dict:
    global _config
    if _config is not None:
        return _config

    if not os.path.exists(_CONFIG_PATH):
        raise FileNotFoundError(
            f"Matomo config not found at {_CONFIG_PATH}. "
            "Set MATOMO_CREDENTIALS env var or create ~/matomo.yaml "
            "with: url, token_auth, and optional default_site_id."
        )

    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        _config = yaml.safe_load(f) or {}

    required = ["url", "token_auth"]
    missing = [f for f in required if not _config.get(f)]
    if missing:
        raise ValueError(f"Missing required fields in {_CONFIG_PATH}: {', '.join(missing)}")

    # Normalize URL - strip trailing slash
    _config["url"] = _config["url"].rstrip("/")

    return _config


def _get_client() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(timeout=30.0)
    return _client


def get_matomo_url() -> str:
    return _load_config()["url"]


def get_token() -> str:
    return _load_config()["token_auth"]


def get_default_site_id() -> Optional[int]:
    config = _load_config()
    sid = config.get("default_site_id")
    return int(sid) if sid else None


def resolve_site_id(site_id: Optional[int] = None) -> int:
    if site_id is not None:
        return site_id
    default = get_default_site_id()
    if default is not None:
        return default
    raise ValueError(
        "No site_id provided and no default_site_id configured in matomo.yaml."
    )


def matomo_request(
    method: str,
    params: Optional[dict[str, Any]] = None,
    post: bool = False,
) -> Any:
    """Make a Matomo API request.

    Args:
        method: API method (e.g., "SitesManager.getAllSites").
        params: Additional API parameters.
        post: Use POST instead of GET.

    Returns:
        Parsed JSON response.

    Raises:
        RuntimeError: If the API returns an error.
    """
    config = _load_config()
    client = _get_client()

    base_params = {
        "module": "API",
        "method": method,
        "format": "JSON",
        "token_auth": config["token_auth"],
    }
    if params:
        base_params.update(params)

    url = f"{config['url']}/index.php"

    if post:
        response = client.post(url, data=base_params)
    else:
        response = client.get(url, params=base_params)

    response.raise_for_status()

    data = response.json()

    # Check for Matomo API errors
    if isinstance(data, dict) and data.get("result") == "error":
        raise RuntimeError(f"Matomo API error: {data.get('message', 'Unknown error')}")

    return data


def reset_client() -> None:
    """Reset client and config (for testing)."""
    global _config, _client
    _config = None
    if _client:
        _client.close()
    _client = None
