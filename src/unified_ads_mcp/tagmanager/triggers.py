"""Google Tag Manager trigger management tools."""

from typing import Any, Optional

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import get_tagmanager_service, resolve_workspace_path


def _trigger_to_dict(trigger: dict) -> dict[str, Any]:
    """Extract key fields from a GTM trigger response."""
    return {
        "triggerId": trigger.get("triggerId"),
        "name": trigger.get("name"),
        "type": trigger.get("type"),
        "filter": trigger.get("filter", []),
        "customEventFilter": trigger.get("customEventFilter", []),
        "fingerprint": trigger.get("fingerprint"),
        "path": trigger.get("path"),
        "parameter": trigger.get("parameter", []),
    }


@mcp.tool()
def gtm_list_triggers(
    account_id: Optional[str] = None,
    container_id: Optional[str] = None,
    workspace_id: str = "Default Workspace",
) -> list[dict[str, Any]]:
    """Lists all triggers in a GTM workspace.

    Args:
        account_id: GTM account ID. Uses default from config if not provided.
        container_id: GTM container ID. Uses default from config if not provided.
        workspace_id: Workspace ID. Defaults to "Default Workspace".

    Returns:
        list[dict]: List of triggers with triggerId, name, type, filters, and parameters.
    """
    try:
        workspace_path = resolve_workspace_path(account_id, container_id, workspace_id)
        service = get_tagmanager_service()
        result = service.accounts().containers().workspaces().triggers().list(
            parent=workspace_path
        ).execute()
        triggers = result.get("trigger", [])
        return [_trigger_to_dict(t) for t in triggers]
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(f"Failed to list triggers: {e}") from e


@mcp.tool()
def gtm_create_trigger(
    name: str,
    trigger_type: str,
    account_id: Optional[str] = None,
    container_id: Optional[str] = None,
    workspace_id: str = "Default Workspace",
    custom_event_filter: Optional[list[dict[str, Any]]] = None,
    filter: Optional[list[dict[str, Any]]] = None,
    parameter: Optional[list[dict[str, Any]]] = None,
) -> dict[str, Any]:
    """Creates a new trigger in a GTM workspace.

    Common trigger types:
        - "pageview": Page View (fires on page load)
        - "domReady": DOM Ready
        - "windowLoaded": Window Loaded
        - "customEvent": Custom Event (dataLayer.push)
        - "click": Click - All Elements
        - "linkClick": Click - Just Links
        - "formSubmission": Form Submission
        - "timer": Timer
        - "scrollDepth": Scroll Depth
        - "youTubeVideo": YouTube Video
        - "elementVisibility": Element Visibility

    Filters use conditions to restrict when the trigger fires. Each filter
    is a dict with:
        - type: "equals", "contains", "startsWith", "endsWith", "matchRegex", etc.
        - parameter: list of [{"type": "template", "key": "arg0", "value": "{{Page URL}}"},
                               {"type": "template", "key": "arg1", "value": "https://example.com/blog"}]

    Args:
        name: Trigger display name (e.g. "Blog Page Views").
        trigger_type: The trigger type (e.g. "pageview", "customEvent").
        account_id: GTM account ID. Uses default if not provided.
        container_id: GTM container ID. Uses default if not provided.
        workspace_id: Workspace ID. Defaults to "Default Workspace".
        custom_event_filter: Filters for custom event triggers.
        filter: General filters/conditions for the trigger.
        parameter: Additional trigger parameters.

    Returns:
        dict: Created trigger details.
    """
    try:
        workspace_path = resolve_workspace_path(account_id, container_id, workspace_id)
        service = get_tagmanager_service()

        body: dict[str, Any] = {
            "name": name,
            "type": trigger_type,
        }
        if custom_event_filter:
            body["customEventFilter"] = custom_event_filter
        if filter:
            body["filter"] = filter
        if parameter:
            body["parameter"] = parameter

        result = service.accounts().containers().workspaces().triggers().create(
            parent=workspace_path, body=body
        ).execute()
        return _trigger_to_dict(result)
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(f"Failed to create trigger: {e}") from e


@mcp.tool()
def gtm_update_trigger(
    trigger_path: str,
    name: Optional[str] = None,
    custom_event_filter: Optional[list[dict[str, Any]]] = None,
    filter: Optional[list[dict[str, Any]]] = None,
    parameter: Optional[list[dict[str, Any]]] = None,
) -> dict[str, Any]:
    """Updates an existing trigger in a GTM workspace.

    Args:
        trigger_path: Full trigger path
            (e.g. "accounts/123/containers/456/workspaces/789/triggers/101").
        name: New trigger name.
        custom_event_filter: New custom event filters (replaces existing).
        filter: New filters/conditions (replaces existing).
        parameter: New parameters (replaces existing).

    Returns:
        dict: Updated trigger details.
    """
    try:
        service = get_tagmanager_service()

        current = service.accounts().containers().workspaces().triggers().get(
            path=trigger_path
        ).execute()

        if name is not None:
            current["name"] = name
        if custom_event_filter is not None:
            current["customEventFilter"] = custom_event_filter
        if filter is not None:
            current["filter"] = filter
        if parameter is not None:
            current["parameter"] = parameter

        result = service.accounts().containers().workspaces().triggers().update(
            path=trigger_path, body=current
        ).execute()
        return _trigger_to_dict(result)
    except Exception as e:
        raise ToolError(f"Failed to update trigger: {e}") from e


@mcp.tool()
def gtm_delete_trigger(
    trigger_path: str,
) -> dict[str, Any]:
    """Deletes a trigger from a GTM workspace.

    Note: You cannot delete a trigger that is referenced by any tag.
    Remove the trigger from all tags first.

    Args:
        trigger_path: Full trigger path
            (e.g. "accounts/123/containers/456/workspaces/789/triggers/101").

    Returns:
        dict: Deletion confirmation.
    """
    try:
        service = get_tagmanager_service()
        service.accounts().containers().workspaces().triggers().delete(
            path=trigger_path
        ).execute()
        return {"status": "deleted", "path": trigger_path}
    except Exception as e:
        raise ToolError(f"Failed to delete trigger: {e}") from e
