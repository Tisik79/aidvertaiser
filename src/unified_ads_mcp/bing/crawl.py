"""Bing Webmaster Tools Crawl Management."""

from typing import Optional

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import bing_request, resolve_site_url


@mcp.tool()
def bing_get_crawl_stats(site_url: Optional[str] = None) -> dict:
    """Gets crawl statistics for a site from Bing Webmaster Tools.

    Returns statistics about how Bingbot has been crawling the site,
    including pages crawled, crawl errors, and crawl activity over time.

    Args:
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: Crawl statistics including pages crawled, crawl errors,
            and crawl activity data.
    """
    try:
        site_url = resolve_site_url(site_url)
        return bing_request("GetCrawlStats", params={"siteUrl": site_url})
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_get_crawl_issues(site_url: Optional[str] = None) -> dict:
    """Gets crawl issues found by Bingbot for a site.

    Returns a list of crawl issues and errors that Bingbot encountered
    while crawling the site, such as HTTP errors, DNS failures, and
    robots.txt blocks.

    Args:
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: List of crawl issues with error types, affected URLs,
            and timestamps.
    """
    try:
        site_url = resolve_site_url(site_url)
        return bing_request("GetCrawlIssues", params={"siteUrl": site_url})
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_get_crawl_settings(site_url: Optional[str] = None) -> dict:
    """Gets the current crawl rate settings for a site.

    Returns the crawl rate configuration that controls how aggressively
    Bingbot crawls the site and whether crawl boost is available.

    Args:
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: Current crawl settings including crawl rate level
            and crawl boost availability.
    """
    try:
        site_url = resolve_site_url(site_url)
        return bing_request("GetCrawlSettings", params={"siteUrl": site_url})
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_save_crawl_settings(
    crawl_boost_available: bool,
    crawl_rate: int,
    site_url: Optional[str] = None,
) -> dict:
    """Saves crawl rate settings for a site in Bing Webmaster Tools.

    Controls how aggressively Bingbot crawls the site. Higher crawl
    rates mean more frequent crawling but also more server load.
    Use bing_get_crawl_settings first to see current values.

    Args:
        crawl_boost_available: Whether to enable crawl boost for
            faster crawling during off-peak hours.
        crawl_rate: Crawl rate level from 1 to 10. Higher values
            mean more aggressive crawling (1 = slowest, 10 = fastest).
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: Success confirmation with the saved settings.
    """
    try:
        site_url = resolve_site_url(site_url)
        bing_request(
            "SaveCrawlSettings",
            body={
                "siteUrl": site_url,
                "crawlBoostAvailable": crawl_boost_available,
                "crawlRate": crawl_rate,
            },
            http_method="POST",
        )
        return {
            "success": True,
            "siteUrl": site_url,
            "crawlRate": crawl_rate,
            "crawlBoostAvailable": crawl_boost_available,
            "message": "Crawl settings saved.",
        }
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e
