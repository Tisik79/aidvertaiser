"""Unified Ads MCP Server.

This module sets up the FastMCP server that provides unified access to both
Google Ads and Meta Ads platforms.

The server exposes tools with platform-specific prefixes:
    - google_* : Google Ads operations
    - meta_*   : Meta Ads operations

Authentication is handled automatically via browser-based OAuth when needed.
"""

import sys
from fastmcp import FastMCP

# Initialize the MCP server first (must be before tool imports)
mcp = FastMCP(
    name="Unified Ads MCP",
    instructions="""
    Unified MCP server for Google Ads and Meta Ads management.

    TOOL NAMING CONVENTION:
    - Google Ads tools are prefixed with 'google_'
    - Meta Ads tools are prefixed with 'meta_'

    AUTHENTICATION:
    Authentication happens automatically via browser when needed.
    Tokens are cached persistently at ~/.unified-ads-mcp/

    GOOGLE ADS:
    - Configure via GOOGLE_ADS_CREDENTIALS env var or ~/google-ads.yaml
    - Requires developer_token, client_id, client_secret in config
    - Use google_run_query for any GAQL queries

    META ADS:
    - Configure via META_APP_ID and META_APP_SECRET env vars
    - Default app ID: 779761636818489
    - Tokens auto-refresh via browser OAuth when expired

    COMMON WORKFLOWS:
    1. List accounts first to get customer_id/account_id
    2. List campaigns with optional status filter
    3. Create/update campaigns as needed
    4. Run queries/get insights for reporting
    """,
)

# Import tool modules to register them with @mcp.tool() decorators
# These imports MUST come after mcp is defined
from .google import campaigns as google_campaigns  # noqa: E402, F401
from .google import reporting as google_reporting  # noqa: E402, F401
from .google import ad_groups as google_ad_groups  # noqa: E402, F401
from .google import ads as google_ads  # noqa: E402, F401
from .google import keywords as google_keywords  # noqa: E402, F401
from .meta import campaigns as meta_campaigns  # noqa: E402, F401
from .meta import insights as meta_insights  # noqa: E402, F401


def main():
    """Run the MCP server."""
    print("Starting Unified Ads MCP Server...", file=sys.stderr)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
