"""Bing Webmaster Tools Search Analytics."""

from typing import Optional

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import bing_request, resolve_site_url


@mcp.tool()
def bing_get_rank_and_traffic_stats(site_url: Optional[str] = None) -> dict:
    """Gets overall search traffic and ranking stats from Bing.

    Returns weekly traffic data showing how the site performs in Bing search
    results over time. This is the main overview endpoint, similar to the
    "Search Performance" dashboard in Bing Webmaster Tools. Data is
    aggregated by week.

    Use this for a high-level view of search performance trends. For
    per-query or per-page breakdowns, use bing_get_query_stats or
    bing_get_page_stats instead.

    Args:
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: Weekly traffic data, each entry containing:
            - Date: The week start date
            - Clicks: Number of clicks from Bing search results
            - Impressions: Number of times pages appeared in search results
            - AvgClickPosition: Average position when users clicked
            - AvgImpressionPosition: Average position in search results
            - CrawledPages: Number of pages Bing crawled that week
    """
    try:
        site_url = resolve_site_url(site_url)
        return bing_request(
            "GetRankAndTrafficStats", params={"siteUrl": site_url}
        )
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_get_query_stats(site_url: Optional[str] = None) -> dict:
    """Gets search query performance stats from Bing.

    Returns the search queries that drove traffic to the site from Bing
    search results, along with click and impression metrics for each query.
    This is similar to Google Search Console's "search analytics by query"
    report.

    Use this to understand what users are searching for when they find
    the site, which queries drive the most clicks, and where the site
    ranks for specific search terms.

    Args:
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: Query performance data, each entry containing:
            - Query: The search query text
            - Date: The data period
            - Clicks: Number of clicks from this query
            - Impressions: Number of times the site appeared for this query
            - AvgClickPosition: Average position when users clicked
            - AvgImpressionPosition: Average position in search results
    """
    try:
        site_url = resolve_site_url(site_url)
        return bing_request(
            "GetQueryStats", params={"siteUrl": site_url}
        )
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_get_page_stats(site_url: Optional[str] = None) -> dict:
    """Gets page-level search performance stats from Bing.

    Returns which pages on the site appear in Bing search results and
    how they perform, with click and impression metrics for each page.
    This is similar to Google Search Console's "search analytics by page"
    report.

    Use this to identify the best-performing pages, find pages with
    high impressions but low clicks (optimization opportunities), and
    track page-level ranking trends.

    Args:
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: Page performance data, each entry containing:
            - Query: The page URL
            - Date: The data period
            - Clicks: Number of clicks to this page from search
            - Impressions: Number of times this page appeared in results
            - AvgClickPosition: Average position when users clicked
            - AvgImpressionPosition: Average position in search results
    """
    try:
        site_url = resolve_site_url(site_url)
        return bing_request(
            "GetPageStats", params={"siteUrl": site_url}
        )
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e
