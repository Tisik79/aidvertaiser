"""Google Search Console API client factory."""

import sys

from googleapiclient.discovery import build

from unified_ads_mcp.auth.google_searchconsole_auth import (
    get_google_searchconsole_auth,
)


def get_searchconsole_service(force_refresh: bool = False):
    """Get a configured Google Search Console API service."""
    auth = get_google_searchconsole_auth()
    credentials = auth.get_credentials(force_refresh=force_refresh)
    try:
        return build("searchconsole", "v1", credentials=credentials)
    except Exception as e:
        print(f"[Search Console] Client creation failed: {e}", file=sys.stderr)
        raise


def get_indexing_service(force_refresh: bool = False):
    """Get a configured Google Indexing API v3 service.

    Uses the same credentials as Search Console (with indexing scope added).
    Requires the 'Web Search Indexing API' to be enabled in Google Cloud Console.
    """
    auth = get_google_searchconsole_auth()
    credentials = auth.get_credentials(force_refresh=force_refresh)
    try:
        return build("indexing", "v3", credentials=credentials)
    except Exception as e:
        print(f"[Indexing API] Client creation failed: {e}", file=sys.stderr)
        raise
