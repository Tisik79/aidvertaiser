"""Real-time visitor data tools for Matomo Analytics."""

from typing import Any, Optional

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import matomo_request, resolve_site_id


@mcp.tool()
def matomo_get_live_counters(
    site_id: Optional[int] = None,
    last_minutes: int = 30,
) -> dict[str, Any]:
    """Gets real-time visitor counters (active visitors right now).

    Args:
        site_id: The site ID. Uses default from config if not provided.
        last_minutes: Look back window in minutes (default 30).

    Returns:
        dict: Live counters with visits, actions, visitors, visitsConverted.
    """
    try:
        site_id = resolve_site_id(site_id)
        result = matomo_request("Live.getCounters", {
            "idSite": site_id,
            "lastMinutes": last_minutes,
        })
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return result
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_last_visits(
    site_id: Optional[int] = None,
    count: int = 10,
    filter_limit: int = 10,
) -> list[dict[str, Any]]:
    """Gets details of the most recent visitor sessions.

    Args:
        site_id: The site ID. Uses default from config if not provided.
        count: Number of recent visits to return (default 10).
        filter_limit: Max results (default 10).

    Returns:
        list[dict]: Recent visits with visitor details including:
            - visitorId, visitorType (new/returning)
            - country, city, region
            - browser, operatingSystem, deviceType
            - referrerType, referrerName, referrerUrl
            - actions (list of pages visited)
            - visitDuration, goalConversions
            - firstActionTimestamp, lastActionTimestamp
    """
    try:
        site_id = resolve_site_id(site_id)
        return matomo_request("Live.getLastVisitsDetails", {
            "idSite": site_id,
            "filter_limit": filter_limit,
            "countVisitorsToFetch": count,
        })
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_visitor_profile(
    visitor_id: str,
    site_id: Optional[int] = None,
) -> dict[str, Any]:
    """Gets the full profile of a specific visitor.

    Args:
        visitor_id: The Matomo visitor ID (hex string).
        site_id: The site ID. Uses default from config if not provided.

    Returns:
        dict: Visitor profile with visit history, total visits,
            total actions, total visit duration, devices used,
            countries, referrers, and recent visit details.
    """
    try:
        site_id = resolve_site_id(site_id)
        return matomo_request("Live.getVisitorProfile", {
            "idSite": site_id,
            "visitorId": visitor_id,
        })
    except Exception as e:
        raise ToolError(str(e)) from e
