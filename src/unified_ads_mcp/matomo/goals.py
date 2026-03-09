"""Goal/conversion management tools for Matomo Analytics."""

from typing import Any, Optional

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import matomo_request, resolve_site_id


@mcp.tool()
def matomo_list_goals(
    site_id: Optional[int] = None,
) -> list[dict[str, Any]]:
    """Lists all goals (conversions) for a Matomo site.

    Args:
        site_id: The site ID. Uses default from config if not provided.

    Returns:
        list[dict]: Goals with idgoal, name, description, match_attribute,
            pattern, pattern_type, revenue, allow_multiple.
    """
    try:
        site_id = resolve_site_id(site_id)
        result = matomo_request("Goals.getGoals", {"idSite": site_id})
        # Matomo returns dict keyed by goal ID, convert to list
        if isinstance(result, dict):
            return list(result.values())
        return result
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_add_goal(
    name: str,
    match_attribute: str = "url",
    pattern: str = "",
    pattern_type: str = "contains",
    case_sensitive: bool = False,
    revenue: float = 0,
    allow_multiple: bool = False,
    description: str = "",
    site_id: Optional[int] = None,
) -> dict[str, Any]:
    """Creates a new goal (conversion) for a Matomo site.

    Args:
        name: Goal name (e.g., "Contact Form Submission").
        match_attribute: What to match. Options:
            - "url": Match page URL
            - "title": Match page title
            - "event_action": Match event action
            - "event_category": Match event category
            - "event_name": Match event name
            - "file": Match downloaded file URL
            - "external_website": Match outbound link URL
            - "manually": Goal triggered via JS tracking API
            - "visit_duration": Match visit duration (seconds)
            - "nb_pageviews": Match number of pageviews per visit
        pattern: Pattern to match (e.g., "thank-you", "contact").
            Not needed for "manually".
        pattern_type: Match type. Options:
            - "contains": Pattern is contained in the attribute
            - "exact": Exact match
            - "regex": Regular expression match
        case_sensitive: Whether pattern matching is case-sensitive.
        revenue: Default revenue value per conversion.
        allow_multiple: Allow multiple conversions per visit.
        description: Optional description.
        site_id: The site ID. Uses default from config if not provided.

    Returns:
        dict: Created goal with idgoal.
    """
    try:
        site_id = resolve_site_id(site_id)
        result = matomo_request("Goals.addGoal", {
            "idSite": site_id,
            "name": name,
            "matchAttribute": match_attribute,
            "pattern": pattern,
            "patternType": pattern_type,
            "caseSensitive": 1 if case_sensitive else 0,
            "revenue": revenue,
            "allowMultipleConversionsPerVisit": 1 if allow_multiple else 0,
            "description": description,
        })
        goal_id = result.get("value") if isinstance(result, dict) else result
        return {"idgoal": goal_id, "name": name, "status": "created"}
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_update_goal(
    goal_id: int,
    name: str,
    match_attribute: str = "url",
    pattern: str = "",
    pattern_type: str = "contains",
    case_sensitive: bool = False,
    revenue: float = 0,
    allow_multiple: bool = False,
    description: str = "",
    site_id: Optional[int] = None,
) -> dict[str, Any]:
    """Updates an existing Matomo goal.

    All fields are required by the API even if unchanged.
    Get current values via matomo_list_goals first.

    Args:
        goal_id: The goal ID to update.
        name: Goal name.
        match_attribute: What to match (see matomo_add_goal for options).
        pattern: Pattern to match.
        pattern_type: Match type ("contains", "exact", "regex").
        case_sensitive: Whether pattern matching is case-sensitive.
        revenue: Default revenue value per conversion.
        allow_multiple: Allow multiple conversions per visit.
        description: Optional description.
        site_id: The site ID. Uses default from config if not provided.

    Returns:
        dict: Update confirmation.
    """
    try:
        site_id = resolve_site_id(site_id)
        matomo_request("Goals.updateGoal", {
            "idSite": site_id,
            "idGoal": goal_id,
            "name": name,
            "matchAttribute": match_attribute,
            "pattern": pattern,
            "patternType": pattern_type,
            "caseSensitive": 1 if case_sensitive else 0,
            "revenue": revenue,
            "allowMultipleConversionsPerVisit": 1 if allow_multiple else 0,
            "description": description,
        })
        return {"idgoal": goal_id, "status": "updated"}
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_delete_goal(
    goal_id: int,
    site_id: Optional[int] = None,
) -> dict[str, Any]:
    """Deletes a goal from a Matomo site.

    Args:
        goal_id: The goal ID to delete.
        site_id: The site ID. Uses default from config if not provided.

    Returns:
        dict: Deletion confirmation.
    """
    try:
        site_id = resolve_site_id(site_id)
        matomo_request("Goals.deleteGoal", {
            "idSite": site_id,
            "idGoal": goal_id,
        })
        return {"idgoal": goal_id, "status": "deleted"}
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_goal_report(
    site_id: Optional[int] = None,
    period: str = "day",
    date: str = "last7",
    goal_id: Optional[int] = None,
) -> Any:
    """Gets goal conversion report data.

    Args:
        site_id: The site ID. Uses default from config if not provided.
        period: Period type - "day", "week", "month", "year", or "range".
        date: Date or range (e.g., "last7", "2026-01-01,2026-01-31").
        goal_id: Optional specific goal ID. If not provided, returns
            data for all goals combined.

    Returns:
        Goal conversion data with nb_conversions, nb_visits_converted,
            revenue, conversion_rate per period.
    """
    try:
        site_id = resolve_site_id(site_id)
        params: dict[str, Any] = {
            "idSite": site_id,
            "period": period,
            "date": date,
        }
        if goal_id is not None:
            params["idGoal"] = goal_id
        return matomo_request("Goals.get", params)
    except Exception as e:
        raise ToolError(str(e)) from e
