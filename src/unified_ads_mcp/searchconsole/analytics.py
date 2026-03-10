"""Google Search Console Search Analytics Tools."""

from typing import Optional, List

from ..server import mcp
from .client import get_searchconsole_service


@mcp.tool()
async def gsc_search_analytics(
    site_url: str,
    start_date: str,
    end_date: str,
    dimensions: Optional[List[str]] = None,
    search_type: str = "web",
    row_limit: int = 25,
    start_row: int = 0,
    dimension_filter_groups: Optional[List[dict]] = None,
    aggregation_type: str = "auto",
) -> dict:
    """Queries search traffic data from Google Search Console.

    Returns clicks, impressions, CTR, and average position for your site
    in Google Search results. This is the core analytics tool.

    Args:
        site_url: The site URL (e.g., "https://example.com/" or "sc-domain:example.com").
        start_date: Start date in YYYY-MM-DD format (max 16 months back).
        end_date: End date in YYYY-MM-DD format.
        dimensions: List of dimensions to group by. Options:
            - "query": Search queries users typed
            - "page": Pages that appeared in results
            - "country": Country of the searcher (ISO 3166-1 alpha-3)
            - "device": Device type (DESKTOP, MOBILE, TABLET)
            - "date": Date (for time series)
            - "searchAppearance": Special result types (e.g., RICH_RESULT)
        search_type: Type of search results. Options:
            - "web" (default): Web search
            - "image": Image search
            - "video": Video search
            - "news": News search
            - "discover": Google Discover
            - "googleNews": Google News app
        row_limit: Max rows to return (default 25, max 25000).
        start_row: Row offset for pagination (default 0).
        dimension_filter_groups: Optional filters. Example:
            [{"groupType": "and", "filters": [
                {"dimension": "query", "operator": "contains", "expression": "keyword"},
                {"dimension": "country", "operator": "equals", "expression": "CZE"}
            ]}]
            Operators: contains, equals, notContains, notEquals, includingRegex, excludingRegex
        aggregation_type: How to aggregate data. Options:
            - "auto" (default): Best aggregation for dimensions
            - "byProperty": Aggregate by property
            - "byPage": Aggregate by page (count each page URL separately)

    Returns:
        Dictionary with:
            - rows: List of data rows with clicks, impressions, ctr, position
            - responseAggregationType: How data was aggregated

    Example:
        >>> await gsc_search_analytics(
        ...     site_url="https://autocrm.cz/",
        ...     start_date="2026-02-01",
        ...     end_date="2026-03-01",
        ...     dimensions=["query"],
        ...     row_limit=10
        ... )
    """
    service = get_searchconsole_service()

    body = {
        "startDate": start_date,
        "endDate": end_date,
        "searchType": search_type,
        "rowLimit": min(row_limit, 25000),
        "startRow": start_row,
        "aggregationType": aggregation_type,
    }

    if dimensions:
        body["dimensions"] = dimensions

    if dimension_filter_groups:
        body["dimensionFilterGroups"] = dimension_filter_groups

    return service.searchanalytics().query(siteUrl=site_url, body=body).execute()


@mcp.tool()
async def gsc_search_analytics_by_query(
    site_url: str,
    start_date: str,
    end_date: str,
    row_limit: int = 25,
    query_filter: Optional[str] = None,
) -> dict:
    """Gets top search queries for a site (shortcut for common use case).

    Args:
        site_url: The site URL.
        start_date: Start date (YYYY-MM-DD).
        end_date: End date (YYYY-MM-DD).
        row_limit: Max rows (default 25).
        query_filter: Optional filter - only show queries containing this string.

    Returns:
        Dictionary with rows containing query, clicks, impressions, ctr, position.
    """
    service = get_searchconsole_service()

    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": min(row_limit, 25000),
    }

    if query_filter:
        body["dimensionFilterGroups"] = [{
            "groupType": "and",
            "filters": [{
                "dimension": "query",
                "operator": "contains",
                "expression": query_filter,
            }],
        }]

    return service.searchanalytics().query(siteUrl=site_url, body=body).execute()


@mcp.tool()
async def gsc_search_analytics_by_page(
    site_url: str,
    start_date: str,
    end_date: str,
    row_limit: int = 25,
    page_filter: Optional[str] = None,
) -> dict:
    """Gets top pages by search performance (shortcut for common use case).

    Args:
        site_url: The site URL.
        start_date: Start date (YYYY-MM-DD).
        end_date: End date (YYYY-MM-DD).
        row_limit: Max rows (default 25).
        page_filter: Optional filter - only show pages containing this URL string.

    Returns:
        Dictionary with rows containing page URL, clicks, impressions, ctr, position.
    """
    service = get_searchconsole_service()

    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["page"],
        "rowLimit": min(row_limit, 25000),
    }

    if page_filter:
        body["dimensionFilterGroups"] = [{
            "groupType": "and",
            "filters": [{
                "dimension": "page",
                "operator": "contains",
                "expression": page_filter,
            }],
        }]

    return service.searchanalytics().query(siteUrl=site_url, body=body).execute()
