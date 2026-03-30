"""Unified Ads MCP Server.

This module sets up the FastMCP server that provides unified access to
Google Ads, Meta Ads, Google Analytics (GA4), Google Search Console,
Matomo Analytics, and Bing Webmaster Tools.

The server exposes tools with platform-specific prefixes:
    - google_* : Google Ads operations
    - meta_*   : Meta Ads operations
    - ga4_*    : Google Analytics operations
    - gsc_*    : Google Search Console operations
    - matomo_* : Matomo Analytics operations
    - bing_*   : Bing Webmaster Tools operations

Authentication is handled via browser OAuth (Google, Meta) or API keys (Matomo, Bing).
"""

import sys
from fastmcp import FastMCP

# Initialize the MCP server first (must be before tool imports)
mcp = FastMCP(
    name="Unified Ads MCP",
    instructions="""
    Unified MCP server for Google Ads, Meta Ads, Google Analytics, Google Search Console, Matomo Analytics, and Bing Webmaster Tools.

    TOOL NAMING CONVENTION:
    - Google Ads tools are prefixed with 'google_'
    - Meta Ads tools are prefixed with 'meta_'
    - Google Analytics tools are prefixed with 'ga4_'
    - Google Search Console tools are prefixed with 'gsc_'
    - Matomo Analytics tools are prefixed with 'matomo_'
    - Bing Webmaster Tools are prefixed with 'bing_'
    - PageSpeed Insights tools are prefixed with 'pagespeed_'
    - Google Tag Manager tools are prefixed with 'gtm_'

    AUTHENTICATION:
    Authentication happens automatically via browser when needed.
    Tokens are cached persistently at ~/.unified-ads-mcp/

    GOOGLE ADS:
    - Configure via GOOGLE_ADS_CREDENTIALS env var or ~/google-ads.yaml
    - Requires developer_token, client_id, client_secret in config
    - Set default_customer_id in config to avoid specifying customer_id on every call
    - When default_customer_id is set, DO NOT list accounts - just use the tools directly
    - Set ONLY_DEFAULT_ACCOUNT=1 to force using the default account and disable account listing tools
    - Use google_run_query for any GAQL queries

    GOOGLE ANALYTICS:
    - Configure via GOOGLE_ANALYTICS_CREDENTIALS env var or ~/google-analytics.yaml
    - Falls back to ~/google-ads.yaml for client_id/client_secret if no analytics config
    - Requires client_id, client_secret in config (same Google Cloud project as Ads)
    - Set default_property_id in config to avoid specifying property_id on every call
    - Use ga4_run_report for standard analytics reports
    - Use ga4_run_realtime_report for live data
    - Use ga4_get_metadata to discover available dimensions and metrics

    MATOMO ANALYTICS:
    - Configure via MATOMO_CREDENTIALS env var or ~/matomo.yaml
    - Requires url (Matomo instance URL) and token_auth (API token) in config
    - Set default_site_id in config to avoid specifying site_id on every call
    - Supports multiple Matomo instances by changing the config
    - Use matomo_get_visits_summary for basic visit metrics
    - Use matomo_get_live_counters for real-time active visitors
    - Use matomo_list_goals to see configured conversions

    META ADS:
    - Configure via META_APP_ID and META_APP_SECRET env vars
    - Set META_DEFAULT_ACCOUNT_ID env var to avoid specifying account_id on every call
    - When default account is set, DO NOT list accounts - just use the tools directly
    - Set ONLY_DEFAULT_ACCOUNT=1 to force using the default account and disable account listing tools
    - Default app ID: 779761636818489
    - Tokens auto-refresh via browser OAuth when expired

    IMPORTANT - DEFAULT ACCOUNTS:
    When a default account is configured, you should NEVER call list_accounts first.
    Just use the tools directly - they will use the default account automatically.
    Only call list_accounts if the user explicitly asks to see their accounts or
    if a tool fails because no account is configured.
    If ONLY_DEFAULT_ACCOUNT is set, account listing tools are disabled and all tools
    will use the configured default account ID.

    BING WEBMASTER TOOLS:
    - Configure via BING_WEBMASTER_CREDENTIALS env var or ~/bing-webmaster.yaml
    - Requires api_key in config (get from Bing Webmaster Tools > Settings > API Access)
    - Set default_site_url in config to avoid specifying site_url on every call
    - No OAuth needed - simple API key authentication
    - Use bing_list_sites to see all registered sites
    - Use bing_get_rank_and_traffic_stats for overall search performance
    - Use bing_get_query_stats / bing_get_page_stats for query/page breakdowns
    - Use bing_list_sitemaps / bing_submit_sitemap for sitemap management
    - Use bing_submit_url / bing_submit_url_batch for URL indexing requests

    GOOGLE SEARCH CONSOLE:
    - Authenticates via browser OAuth (same Google Cloud project as Ads/GA4)
    - Falls back to ~/google-ads.yaml for client_id/client_secret
    - Tokens cached at ~/.unified-ads-mcp/google_searchconsole_token.json
    - Use gsc_list_sites to see all registered sites
    - Use gsc_search_analytics for search traffic data (queries, pages, clicks, impressions)
    - Use gsc_search_analytics_by_query / gsc_search_analytics_by_page for quick lookups
    - Use gsc_inspect_url to check indexing status of a specific URL
    - Use gsc_submit_sitemap to register sitemaps

    PAGESPEED INSIGHTS:
    - No config needed for basic usage (rate-limited without API key)
    - Optionally set PAGESPEED_API_KEY env var or configure ~/pagespeed.yaml
    - With API key: 25,000 requests/day
    - Use pagespeed_analyze for full Lighthouse audit (scores + opportunities)
    - Use pagespeed_compare for mobile vs desktop comparison
    - Use pagespeed_core_web_vitals for Chrome UX Report field data

    GOOGLE INDEXING API:
    - Uses Search Console credentials (same OAuth flow)
    - Requires 'Web Search Indexing API' enabled in Google Cloud Console
    - Use gsc_submit_url_for_indexing to ping Google about new/updated URLs
    - Use gsc_submit_urls_for_indexing for batch submissions
    - Rate limit: ~200 requests/day per property
    - After adding indexing scope, delete cached token to re-authenticate:
      rm ~/.unified-ads-mcp/google_searchconsole_token.json

    GOOGLE TAG MANAGER:
    - Configure via GOOGLE_TAGMANAGER_CREDENTIALS env var or ~/google-tagmanager.yaml
    - Falls back to ~/google-ads.yaml for client_id/client_secret
    - Requires 'Tag Manager API' enabled in Google Cloud Console
    - Set default_account_id and default_container_id in config
    - Use gtm_list_accounts / gtm_list_containers to find IDs
    - Use gtm_list_tags / gtm_create_tag to manage tags
    - Use gtm_list_triggers / gtm_create_trigger to manage triggers
    - Use gtm_create_version / gtm_publish_version to push changes live
    - Always create a version and publish to make changes go live

    COMMON WORKFLOWS:
    1. Use tools directly (they use default account if configured)
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
from .google import conversions as google_conversions  # noqa: E402, F401
from .meta import campaigns as meta_campaigns  # noqa: E402, F401
from .meta import insights as meta_insights  # noqa: E402, F401
from .meta import conversions as meta_conversions  # noqa: E402, F401
from .analytics import accounts as ga4_accounts  # noqa: E402, F401
from .analytics import properties as ga4_properties  # noqa: E402, F401
from .analytics import data_streams as ga4_data_streams  # noqa: E402, F401
from .analytics import reporting as ga4_reporting  # noqa: E402, F401
from .analytics import key_events as ga4_key_events  # noqa: E402, F401
from .searchconsole import sites as gsc_sites  # noqa: E402, F401
from .searchconsole import analytics as gsc_analytics  # noqa: E402, F401
from .searchconsole import sitemaps as gsc_sitemaps  # noqa: E402, F401
from .searchconsole import inspection as gsc_inspection  # noqa: E402, F401
from .searchconsole import verification as gsc_verification  # noqa: E402, F401
from .matomo import sites as matomo_sites  # noqa: E402, F401
from .matomo import reporting as matomo_reporting  # noqa: E402, F401
from .matomo import goals as matomo_goals  # noqa: E402, F401
from .matomo import live as matomo_live  # noqa: E402, F401
from .bing import sites as bing_sites  # noqa: E402, F401
from .bing import submissions as bing_submissions  # noqa: E402, F401
from .bing import sitemaps as bing_sitemaps  # noqa: E402, F401
from .bing import analytics as bing_analytics  # noqa: E402, F401
from .bing import crawl as bing_crawl  # noqa: E402, F401
from .bing import keywords as bing_keywords  # noqa: E402, F401
from .bing import links as bing_links  # noqa: E402, F401
from .pagespeed import insights as pagespeed_insights  # noqa: E402, F401
from .analytics import custom_dimensions as ga4_custom_dimensions  # noqa: E402, F401
from .searchconsole import indexing as gsc_indexing  # noqa: E402, F401
from .tagmanager import tags as gtm_tags  # noqa: E402, F401
from .tagmanager import triggers as gtm_triggers  # noqa: E402, F401
from .tagmanager import versions as gtm_versions  # noqa: E402, F401


def main():
    """Run the MCP server."""
    print("Starting Unified Ads MCP Server...", file=sys.stderr)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
