"""Google Search Console URL Inspection Tool."""

from ..server import mcp
from .client import get_searchconsole_service


@mcp.tool()
async def gsc_inspect_url(
    site_url: str,
    inspection_url: str,
) -> dict:
    """Inspects a URL's index status in Google Search.

    Returns detailed information about how Google sees a specific URL,
    including indexing status, crawl info, and any issues.

    Args:
        site_url: The Search Console property (e.g., "https://example.com/").
        inspection_url: The full URL to inspect (e.g., "https://example.com/about").

    Returns:
        Dictionary with:
            - inspectionResult.indexStatusResult: Index status, crawl time, coverage state
            - inspectionResult.mobileUsabilityResult: Mobile-friendliness
            - inspectionResult.richResultsResult: Rich results eligibility
    """
    service = get_searchconsole_service()

    body = {
        "inspectionUrl": inspection_url,
        "siteUrl": site_url,
    }

    return service.urlInspection().index().inspect(body=body).execute()
