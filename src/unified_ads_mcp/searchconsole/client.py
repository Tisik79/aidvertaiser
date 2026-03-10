"""Google Search Console API client factory."""

import sys
from typing import Optional

from googleapiclient.discovery import build

from unified_ads_mcp.auth.google_searchconsole_auth import (
    get_google_searchconsole_auth,
    GoogleSearchConsoleAuth,
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
