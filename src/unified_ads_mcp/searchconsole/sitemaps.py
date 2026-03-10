"""Google Search Console Sitemap Management Tools."""

from typing import Optional

from ..server import mcp
from .client import get_searchconsole_service


@mcp.tool()
async def gsc_list_sitemaps(site_url: str) -> dict:
    """Lists all sitemaps submitted for a site.

    Args:
        site_url: The site URL (e.g., "https://example.com/").

    Returns:
        Dictionary with sitemap list including:
            - path: Sitemap URL
            - lastSubmitted: When it was last submitted
            - isPending: Whether it's still being processed
            - isSitemapsIndex: Whether it's a sitemap index
            - lastDownloaded: When Google last fetched it
            - warnings/errors: Count of issues
    """
    service = get_searchconsole_service()
    return service.sitemaps().list(siteUrl=site_url).execute()


@mcp.tool()
async def gsc_get_sitemap(site_url: str, feedpath: str) -> dict:
    """Gets details for a specific sitemap.

    Args:
        site_url: The site URL.
        feedpath: The full sitemap URL (e.g., "https://example.com/sitemap.xml").

    Returns:
        Dictionary with sitemap details including content type breakdowns.
    """
    service = get_searchconsole_service()
    return service.sitemaps().get(siteUrl=site_url, feedpath=feedpath).execute()


@mcp.tool()
async def gsc_submit_sitemap(site_url: str, feedpath: str) -> dict:
    """Submits a sitemap to Google Search Console.

    Tells Google about your sitemap so it can crawl and index your pages.

    Args:
        site_url: The site URL (e.g., "https://example.com/").
        feedpath: The full sitemap URL (e.g., "https://example.com/sitemap.xml").

    Returns:
        Dictionary with success status.
    """
    service = get_searchconsole_service()
    service.sitemaps().submit(siteUrl=site_url, feedpath=feedpath).execute()
    return {"success": True, "siteUrl": site_url, "feedpath": feedpath}


@mcp.tool()
async def gsc_delete_sitemap(site_url: str, feedpath: str) -> dict:
    """Removes a sitemap from Google Search Console.

    This only removes the sitemap from Search Console tracking -
    Google may still crawl URLs it already knows about.

    Args:
        site_url: The site URL.
        feedpath: The full sitemap URL to remove.

    Returns:
        Dictionary with success status.
    """
    service = get_searchconsole_service()
    service.sitemaps().delete(siteUrl=site_url, feedpath=feedpath).execute()
    return {"success": True, "siteUrl": site_url, "feedpath": feedpath, "message": "Sitemap removed."}
