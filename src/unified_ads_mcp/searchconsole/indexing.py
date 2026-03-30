"""Google Indexing API tools.

Allows submitting URLs for indexing or removal from Google Search.
Uses the Google Indexing API v3 (indexing.googleapis.com).

Note: The Indexing API was originally designed for job postings and
livestream structured data, but works for any URL in your Search
Console property. Google may prioritize URLs with supported structured data.

Requires the "Web Search Indexing API" to be enabled in Google Cloud Console.
"""

from typing import Any

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import get_indexing_service


@mcp.tool()
def gsc_submit_url_for_indexing(
    url: str,
    action: str = "URL_UPDATED",
) -> dict[str, Any]:
    """Submits a URL to Google for indexing or removal.

    Use this after publishing new content, updating existing pages,
    or when URLs have moved (e.g. /slug to /blog/slug). Google will
    prioritize crawling the submitted URL.

    Args:
        url: The fully qualified URL to submit
            (e.g. "https://example.com/blog/my-post").
        action: The notification type:
            - URL_UPDATED: URL is new or has been updated (default)
            - URL_DELETED: URL has been removed

    Returns:
        dict: API response with:
            - url: The submitted URL
            - type: The notification type
            - notifyTime: When Google received the notification (ISO format)

    Raises:
        ToolError: If the API request fails.
    """
    if action not in ("URL_UPDATED", "URL_DELETED"):
        raise ToolError("action must be 'URL_UPDATED' or 'URL_DELETED'")

    try:
        service = get_indexing_service()
        body = {"url": url, "type": action}
        result = service.urlNotifications().publish(body=body).execute()
        return result
    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg:
            raise ToolError(
                f"Permission denied for Indexing API. Ensure:\n"
                f"1. 'Web Search Indexing API' is enabled in Google Cloud Console\n"
                f"2. You have verified ownership of the site in Search Console\n"
                f"3. Re-authenticate with: delete ~/.unified-ads-mcp/google_searchconsole_token.json and retry\n"
                f"Original error: {error_msg}"
            ) from e
        raise ToolError(f"Failed to submit URL for indexing: {error_msg}") from e


@mcp.tool()
def gsc_submit_urls_for_indexing(
    urls: list[str],
    action: str = "URL_UPDATED",
) -> dict[str, Any]:
    """Submits multiple URLs to Google for indexing or removal.

    Sends each URL as a separate notification. Use after bulk content
    updates or URL migrations.

    Rate limits: ~200 requests per day per property.

    Args:
        urls: List of fully qualified URLs to submit.
        action: The notification type for all URLs:
            - URL_UPDATED: URLs are new or updated (default)
            - URL_DELETED: URLs have been removed

    Returns:
        dict: Summary with:
            - submitted: Number of successfully submitted URLs
            - failed: Number of failed submissions
            - results: List of per-URL results with url, status, and error (if any)

    Raises:
        ToolError: If the action is invalid.
    """
    if action not in ("URL_UPDATED", "URL_DELETED"):
        raise ToolError("action must be 'URL_UPDATED' or 'URL_DELETED'")

    service = get_indexing_service()
    results = []
    submitted = 0
    failed = 0

    for url in urls:
        try:
            body = {"url": url, "type": action}
            result = service.urlNotifications().publish(body=body).execute()
            results.append({"url": url, "status": "ok", "notifyTime": result.get("urlNotificationMetadata", {}).get("latestUpdate", {}).get("notifyTime")})
            submitted += 1
        except Exception as e:
            results.append({"url": url, "status": "error", "error": str(e)})
            failed += 1

    return {
        "submitted": submitted,
        "failed": failed,
        "total": len(urls),
        "action": action,
        "results": results,
    }


@mcp.tool()
def gsc_get_indexing_notification_status(
    url: str,
) -> dict[str, Any]:
    """Gets the latest indexing notification status for a URL.

    Shows when Google was last notified about this URL via the Indexing API
    (both update and delete notifications).

    Args:
        url: The fully qualified URL to check
            (e.g. "https://example.com/blog/my-post").

    Returns:
        dict: Notification metadata with latest update and delete timestamps.

    Raises:
        ToolError: If the API request fails.
    """
    try:
        service = get_indexing_service()
        result = service.urlNotifications().getMetadata(url=url).execute()
        return result
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            return {"url": url, "status": "no_notifications", "message": "No indexing notifications found for this URL"}
        raise ToolError(f"Failed to get indexing status: {error_msg}") from e
