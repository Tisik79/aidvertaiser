"""Authentication module for Unified Ads MCP.

This module provides authentication handlers for Google Ads, Meta Ads,
and Bing Webmaster Tools, with browser-based token acquisition and
automatic refresh for OAuth platforms.

Components:
    - oauth_server: Shared local callback server for OAuth flows
    - google_auth: Google Ads OAuth handler with YAML config support
    - meta_auth: Meta Ads OAuth handler with long-lived token exchange
    - bing_auth: Bing Webmaster Tools API key handler
"""

from unified_ads_mcp.auth.oauth_server import (
    start_oauth_server,
    save_token,
    load_token,
    TOKEN_CACHE_DIR,
)
from unified_ads_mcp.auth.google_auth import GoogleAdsAuth, get_google_auth
from unified_ads_mcp.auth.meta_auth import MetaAdsAuth, get_meta_auth
from unified_ads_mcp.auth.bing_auth import BingWebmasterAuth, get_bing_auth

__all__ = [
    "start_oauth_server",
    "save_token",
    "load_token",
    "TOKEN_CACHE_DIR",
    "GoogleAdsAuth",
    "get_google_auth",
    "MetaAdsAuth",
    "get_meta_auth",
    "BingWebmasterAuth",
    "get_bing_auth",
]
