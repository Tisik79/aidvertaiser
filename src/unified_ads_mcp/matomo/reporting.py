"""Analytics reporting tools for Matomo."""

from typing import Any, Optional

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import matomo_request, resolve_site_id


@mcp.tool()
def matomo_get_visits_summary(
    site_id: Optional[int] = None,
    period: str = "day",
    date: str = "last7",
) -> Any:
    """Gets visit summary metrics for a Matomo site.

    Args:
        site_id: The site ID. Uses default from config if not provided.
        period: Period type - "day", "week", "month", "year", or "range".
        date: Date or range. Examples:
            - "today", "yesterday"
            - "last7", "last30" (last N periods)
            - "previous7", "previous30" (previous N periods)
            - "2026-01-01,2026-01-31" (date range, requires period="range")
            - "2026-03-01" (specific date)

    Returns:
        dict or list: Visit summary with nb_visits, nb_uniq_visitors,
            nb_actions, bounce_rate, avg_time_on_site, etc.
            Returns dict for single date, or dict of date->metrics for ranges.
    """
    try:
        site_id = resolve_site_id(site_id)
        return matomo_request("VisitsSummary.get", {
            "idSite": site_id,
            "period": period,
            "date": date,
        })
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_page_urls(
    site_id: Optional[int] = None,
    period: str = "day",
    date: str = "last7",
    limit: int = 20,
    flat: bool = True,
) -> Any:
    """Gets page URL analytics (pageviews, time on page, etc.).

    Args:
        site_id: The site ID. Uses default from config if not provided.
        period: Period type - "day", "week", "month", "year", or "range".
        date: Date or range (see matomo_get_visits_summary for format).
        limit: Max results per period (default 20).
        flat: If True, return flat list instead of tree structure.

    Returns:
        Page analytics with label (URL), nb_visits, nb_hits,
            avg_time_on_page, bounce_rate, exit_rate.
    """
    try:
        site_id = resolve_site_id(site_id)
        return matomo_request("Actions.getPageUrls", {
            "idSite": site_id,
            "period": period,
            "date": date,
            "filter_limit": limit,
            "flat": 1 if flat else 0,
        })
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_referrers(
    site_id: Optional[int] = None,
    period: str = "day",
    date: str = "last7",
    limit: int = 20,
) -> Any:
    """Gets referrer/traffic source analytics.

    Args:
        site_id: The site ID. Uses default from config if not provided.
        period: Period type - "day", "week", "month", "year", or "range".
        date: Date or range (see matomo_get_visits_summary for format).
        limit: Max results per period (default 20).

    Returns:
        Referrer data with label (referrer name/URL), nb_visits,
            nb_actions, nb_uniq_visitors.
    """
    try:
        site_id = resolve_site_id(site_id)
        return matomo_request("Referrers.getAll", {
            "idSite": site_id,
            "period": period,
            "date": date,
            "filter_limit": limit,
        })
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_referrer_types(
    site_id: Optional[int] = None,
    period: str = "day",
    date: str = "last7",
) -> Any:
    """Gets traffic breakdown by referrer type (direct, search, social, websites).

    Args:
        site_id: The site ID. Uses default from config if not provided.
        period: Period type - "day", "week", "month", "year", or "range".
        date: Date or range.

    Returns:
        Traffic breakdown by referrer type with nb_visits, nb_actions.
    """
    try:
        site_id = resolve_site_id(site_id)
        return matomo_request("Referrers.getReferrerType", {
            "idSite": site_id,
            "period": period,
            "date": date,
        })
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_devices(
    site_id: Optional[int] = None,
    period: str = "day",
    date: str = "last7",
    limit: int = 20,
) -> Any:
    """Gets device type analytics (desktop, mobile, tablet).

    Args:
        site_id: The site ID. Uses default from config if not provided.
        period: Period type - "day", "week", "month", "year", or "range".
        date: Date or range.
        limit: Max results per period (default 20).

    Returns:
        Device breakdown with label (device type), nb_visits, nb_actions.
    """
    try:
        site_id = resolve_site_id(site_id)
        return matomo_request("DevicesDetection.getType", {
            "idSite": site_id,
            "period": period,
            "date": date,
            "filter_limit": limit,
        })
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_countries(
    site_id: Optional[int] = None,
    period: str = "day",
    date: str = "last7",
    limit: int = 20,
) -> Any:
    """Gets visitor country analytics.

    Args:
        site_id: The site ID. Uses default from config if not provided.
        period: Period type - "day", "week", "month", "year", or "range".
        date: Date or range.
        limit: Max results per period (default 20).

    Returns:
        Country breakdown with label (country name), nb_visits,
            nb_actions, nb_uniq_visitors.
    """
    try:
        site_id = resolve_site_id(site_id)
        return matomo_request("UserCountry.getCountry", {
            "idSite": site_id,
            "period": period,
            "date": date,
            "filter_limit": limit,
        })
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_search_keywords(
    site_id: Optional[int] = None,
    period: str = "day",
    date: str = "last7",
    limit: int = 20,
) -> Any:
    """Gets search engine keyword analytics.

    Args:
        site_id: The site ID. Uses default from config if not provided.
        period: Period type - "day", "week", "month", "year", or "range".
        date: Date or range.
        limit: Max results per period (default 20).

    Returns:
        Search keywords with label (keyword), nb_visits, nb_actions.
    """
    try:
        site_id = resolve_site_id(site_id)
        return matomo_request("Referrers.getKeywords", {
            "idSite": site_id,
            "period": period,
            "date": date,
            "filter_limit": limit,
        })
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_entry_pages(
    site_id: Optional[int] = None,
    period: str = "day",
    date: str = "last7",
    limit: int = 20,
    flat: bool = True,
) -> Any:
    """Gets landing/entry page analytics.

    Args:
        site_id: The site ID. Uses default from config if not provided.
        period: Period type - "day", "week", "month", "year", or "range".
        date: Date or range.
        limit: Max results per period (default 20).
        flat: If True, return flat list instead of tree structure.

    Returns:
        Entry pages with label (URL), entry_nb_visits, entry_bounce_count,
            entry_nb_actions, entry_sum_visit_length.
    """
    try:
        site_id = resolve_site_id(site_id)
        return matomo_request("Actions.getEntryPageUrls", {
            "idSite": site_id,
            "period": period,
            "date": date,
            "filter_limit": limit,
            "flat": 1 if flat else 0,
        })
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_exit_pages(
    site_id: Optional[int] = None,
    period: str = "day",
    date: str = "last7",
    limit: int = 20,
    flat: bool = True,
) -> Any:
    """Gets exit page analytics.

    Args:
        site_id: The site ID. Uses default from config if not provided.
        period: Period type - "day", "week", "month", "year", or "range".
        date: Date or range.
        limit: Max results per period (default 20).
        flat: If True, return flat list instead of tree structure.

    Returns:
        Exit pages with label (URL), exit_nb_visits, nb_visits, exit_rate.
    """
    try:
        site_id = resolve_site_id(site_id)
        return matomo_request("Actions.getExitPageUrls", {
            "idSite": site_id,
            "period": period,
            "date": date,
            "filter_limit": limit,
            "flat": 1 if flat else 0,
        })
    except Exception as e:
        raise ToolError(str(e)) from e
