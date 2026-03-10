"""Bing Webmaster Tools Sitemap Management."""

from typing import Optional

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import bing_request, resolve_site_url


@mcp.tool()
def bing_list_sitemaps(site_url: Optional[str] = None) -> dict:
    """Lists all sitemaps submitted for a site in Bing Webmaster Tools.

    Returns information about each submitted sitemap including its URL,
    processing status, and last crawled date. Use this to check which
    sitemaps Bing knows about and whether they have been processed
    successfully.

    Args:
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: List of submitted sitemaps, each containing:
            - Url: The sitemap URL
            - LastCrawledDate: When Bing last fetched the sitemap
            - LastSubmittedDate: When the sitemap was last submitted
            - SubmittedVia: How the sitemap was submitted (API, portal, etc.)
            - Status: Processing status (e.g. Success, Pending)
            - UrlCount: Number of URLs found in the sitemap
    """
    try:
        site_url = resolve_site_url(site_url)
        return bing_request("GetFeeds", params={"siteUrl": site_url})
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_submit_sitemap(
    feed_url: str, site_url: Optional[str] = None
) -> dict:
    """Submits a sitemap to Bing Webmaster Tools.

    Tells Bing about your sitemap so it can discover and crawl your pages.
    The sitemap must be a valid XML sitemap or sitemap index accessible at
    the given URL. After submission, Bing will fetch and process the sitemap
    asynchronously -- use bing_list_sitemaps to check processing status.

    Args:
        feed_url: The full URL to the sitemap file
            (e.g. "https://example.com/sitemap.xml").
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: Success confirmation with the submitted sitemap URL.
    """
    try:
        site_url = resolve_site_url(site_url)
        bing_request(
            "SubmitFeed",
            body={"siteUrl": site_url, "feedUrl": feed_url},
            http_method="POST",
        )
        return {
            "success": True,
            "siteUrl": site_url,
            "feedUrl": feed_url,
            "message": "Sitemap submitted. Bing will process it asynchronously.",
        }
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_remove_sitemap(
    feed_url: str, site_url: Optional[str] = None
) -> dict:
    """Removes a sitemap from Bing Webmaster Tools.

    This only removes the sitemap from Bing's tracking. Bing may still
    crawl URLs it already discovered from this sitemap. To completely
    prevent crawling, use robots.txt or noindex directives.

    Args:
        feed_url: The full URL of the sitemap to remove
            (e.g. "https://example.com/sitemap.xml").
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: Success confirmation with the removed sitemap URL.
    """
    try:
        site_url = resolve_site_url(site_url)
        bing_request(
            "RemoveFeed",
            body={"siteUrl": site_url, "feedUrl": feed_url},
            http_method="POST",
        )
        return {
            "success": True,
            "siteUrl": site_url,
            "feedUrl": feed_url,
            "message": "Sitemap removed from Bing Webmaster Tools.",
        }
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e
