"""Bing Webmaster Tools Link Analysis."""

from typing import Optional

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import bing_request, resolve_site_url


@mcp.tool()
def bing_get_link_counts(site_url: Optional[str] = None) -> dict:
    """Gets total inbound link counts for a site from Bing.

    Returns aggregate counts of external links pointing to the site
    as seen by Bingbot during crawling.

    Args:
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: Total inbound link count data for the site.
    """
    try:
        site_url = resolve_site_url(site_url)
        return bing_request("GetLinkCounts", params={"siteUrl": site_url})
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_get_url_links(
    site_url: Optional[str] = None, page: int = 0
) -> dict:
    """Gets a detailed list of inbound links pointing to pages on a site.

    Returns individual inbound links that Bingbot has discovered pointing
    to pages on this site. Results are paginated -- use the page parameter
    to retrieve additional pages of results.

    Args:
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.
        page: Page number for pagination, starting at 0.

    Returns:
        dict: List of inbound links with source URLs and target pages.
    """
    try:
        site_url = resolve_site_url(site_url)
        return bing_request(
            "GetUrlLinks", params={"siteUrl": site_url, "page": page}
        )
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e
