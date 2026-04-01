"""Bing Webmaster Tools URL Submission."""

import json
from typing import Any, Optional


def _coerce_list(value: Any) -> list[str]:
    """Coerce a value to list[str]. Handles JSON strings from MCP transport."""
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        value = value.strip()
        if value.startswith("["):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return [str(v) for v in parsed]
            except json.JSONDecodeError:
                pass
        return [v.strip() for v in value.split(",") if v.strip()]
    raise ValueError(f"Cannot coerce {type(value).__name__} to list[str]")

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import bing_request, resolve_site_url


@mcp.tool()
def bing_submit_url(url: str, site_url: Optional[str] = None) -> dict:
    """Submits a single URL to Bing for crawling and indexing.

    Use this to notify Bing about new or updated pages so they get
    crawled and indexed faster.

    Args:
        url: The full page URL to submit for indexing
            (e.g. "https://example.com/new-page").
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: Success confirmation with the submitted URL.
    """
    try:
        site_url = resolve_site_url(site_url)
        bing_request(
            "SubmitUrl",
            body={"siteUrl": site_url, "url": url},
            http_method="POST",
        )
        return {
            "success": True,
            "siteUrl": site_url,
            "url": url,
            "message": "URL submitted for crawling.",
        }
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_submit_url_batch(
    url_list: Any, site_url: Optional[str] = None
) -> dict:
    """Submits a batch of URLs to Bing for crawling and indexing.

    More efficient than submitting URLs one by one. Maximum 500 URLs
    per batch request. Use bing_get_url_submission_quota to check
    remaining daily and monthly quota before submitting.

    Args:
        url_list: List of full page URLs to submit (max 500).
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: Success confirmation with count of submitted URLs.
    """
    url_list = _coerce_list(url_list)

    try:
        if len(url_list) > 500:
            raise ToolError(
                f"Batch size {len(url_list)} exceeds maximum of 500 URLs. "
                "Split into multiple batches of 500 or fewer."
            )
        if not url_list:
            raise ToolError("url_list must contain at least one URL.")

        site_url = resolve_site_url(site_url)
        bing_request(
            "SubmitUrlBatch",
            body={"siteUrl": site_url, "urlList": url_list},
            http_method="POST",
        )
        return {
            "success": True,
            "siteUrl": site_url,
            "urlCount": len(url_list),
            "message": f"{len(url_list)} URLs submitted for crawling.",
        }
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_get_url_submission_quota(site_url: Optional[str] = None) -> dict:
    """Gets the URL submission quota for a site in Bing Webmaster Tools.

    Check this before submitting URLs to see how many daily and monthly
    submissions remain. Quota varies by site age and traffic volume,
    up to 10,000 URLs per day.

    Args:
        site_url: The verified site URL in Bing Webmaster Tools
            (e.g. "https://example.com"). Uses default from config
            if not provided.

    Returns:
        dict: Quota information including daily and monthly remaining
            submissions.
    """
    try:
        site_url = resolve_site_url(site_url)
        result = bing_request(
            "GetUrlSubmissionQuota",
            params={"siteUrl": site_url},
        )
        return result
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e
