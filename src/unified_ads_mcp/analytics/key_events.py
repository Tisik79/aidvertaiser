"""Key event (conversion) management tools for Google Analytics."""

from typing import Any, Optional

from google.api_core.exceptions import GoogleAPICallError
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import get_admin_client, resolve_property_id, format_property_name

from google.analytics.admin_v1beta.types import (
    KeyEvent,
)


def _key_event_to_dict(event) -> dict[str, Any]:
    """Convert a KeyEvent protobuf object to a plain dictionary.

    Args:
        event: A KeyEvent protobuf object from the GA4 Admin API.

    Returns:
        dict: Key event data with id, name, event_name, create_time,
            deletable, custom, and counting_method fields.
    """
    result = {
        "id": event.name.split("/")[-1] if event.name else None,
        "name": event.name,
        "event_name": event.event_name,
        "create_time": event.create_time.isoformat() if event.create_time else None,
        "deletable": event.deletable,
        "custom": event.custom,
    }
    if event.counting_method:
        result["counting_method"] = event.counting_method.name
    return result


@mcp.tool()
def ga4_list_key_events(
    property_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Lists all key events (conversions) for a Google Analytics 4 property.

    Key events are the GA4 equivalent of conversions. They track important
    user interactions like purchases, sign-ups, or form submissions.

    Args:
        property_id: The GA4 property ID (numeric, e.g. "123456789").
            Uses default from config if not provided.

    Returns:
        list[dict]: List of key events with:
            - id: Key event ID
            - name: Full resource name (properties/{id}/keyEvents/{id})
            - event_name: The event name that triggers this key event
            - create_time: When the key event was created (ISO format)
            - deletable: Whether the key event can be deleted
            - custom: Whether this is a custom key event
            - counting_method: ONCE_PER_EVENT or ONCE_PER_SESSION

    Raises:
        ToolError: If the API request fails.
    """
    try:
        property_id = resolve_property_id(property_id)
        client = get_admin_client()
        events = client.list_key_events(
            parent=format_property_name(property_id),
        )
        return [_key_event_to_dict(event) for event in events]
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to list key events: {e.message}") from e


@mcp.tool()
def ga4_create_key_event(
    event_name: str,
    property_id: Optional[str] = None,
    counting_method: str = "ONCE_PER_EVENT",
) -> dict[str, Any]:
    """Creates a new key event (conversion) for a Google Analytics 4 property.

    After creation, any time the specified event is triggered by users,
    it will be counted as a conversion in GA4 reports.

    Args:
        event_name: The event name to mark as a key event
            (e.g. "purchase", "sign_up", "generate_lead").
        property_id: The GA4 property ID (numeric, e.g. "123456789").
            Uses default from config if not provided.
        counting_method: How to count the key event. Options:
            - ONCE_PER_EVENT: Count every occurrence (default, good for purchases)
            - ONCE_PER_SESSION: Count max once per session (good for sign-ups)

    Returns:
        dict: Created key event with id, name, event_name, create_time,
            deletable, custom, and counting_method fields.

    Raises:
        ToolError: If the API request fails.
    """
    try:
        property_id = resolve_property_id(property_id)
        client = get_admin_client()
        key_event = KeyEvent(
            event_name=event_name,
            counting_method=KeyEvent.CountingMethod[counting_method],
        )
        result = client.create_key_event(
            parent=format_property_name(property_id),
            key_event=key_event,
        )
        return _key_event_to_dict(result)
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to create key event: {e.message}") from e


@mcp.tool()
def ga4_update_key_event(
    key_event_name: str,
    counting_method: str,
) -> dict[str, Any]:
    """Updates an existing key event's counting method.

    Args:
        key_event_name: The full resource name of the key event
            (e.g. "properties/123456/keyEvents/789").
        counting_method: New counting method. Options:
            - ONCE_PER_EVENT: Count every occurrence
            - ONCE_PER_SESSION: Count max once per session

    Returns:
        dict: Updated key event with id, name, event_name, create_time,
            deletable, custom, and counting_method fields.

    Raises:
        ToolError: If the API request fails.
    """
    try:
        from google.protobuf.field_mask_pb2 import FieldMask

        client = get_admin_client()
        key_event = KeyEvent(
            name=key_event_name,
            counting_method=KeyEvent.CountingMethod[counting_method],
        )
        result = client.update_key_event(
            key_event=key_event,
            update_mask=FieldMask(paths=["counting_method"]),
        )
        return _key_event_to_dict(result)
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to update key event: {e.message}") from e


@mcp.tool()
def ga4_delete_key_event(
    key_event_name: str,
) -> dict[str, Any]:
    """Deletes a key event (conversion) from a Google Analytics 4 property.

    Once deleted, the event will no longer be counted as a conversion.
    Historical data is retained in reports.

    Args:
        key_event_name: The full resource name of the key event
            (e.g. "properties/123456/keyEvents/789").

    Returns:
        dict: Deletion confirmation with:
            - status: "deleted"
            - name: The resource name of the deleted key event

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_admin_client()
        client.delete_key_event(name=key_event_name)
        return {"status": "deleted", "name": key_event_name}
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to delete key event: {e.message}") from e
