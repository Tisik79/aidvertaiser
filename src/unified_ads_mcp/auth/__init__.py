"""Authentication module for Unified Ads MCP.

This module provides OAuth authentication handlers for both Google Ads and Meta Ads,
with browser-based token acquisition and automatic refresh.

Components:
    - oauth_server: Shared local callback server for OAuth flows
    - google_auth: Google Ads OAuth handler with YAML config support
    - meta_auth: Meta Ads OAuth handler with long-lived token exchange
"""

from unified_ads_mcp.auth.oauth_server import (
    start_oauth_server,
    save_token,
    load_token,
    TOKEN_CACHE_DIR,
)
from unified_ads_mcp.auth.google_auth import GoogleAdsAuth, get_google_auth
from unified_ads_mcp.auth.meta_auth import MetaAdsAuth, get_meta_auth

__all__ = [
    "start_oauth_server",
    "save_token",
    "load_token",
    "TOKEN_CACHE_DIR",
    "GoogleAdsAuth",
    "get_google_auth",
    "MetaAdsAuth",
    "get_meta_auth",
]
