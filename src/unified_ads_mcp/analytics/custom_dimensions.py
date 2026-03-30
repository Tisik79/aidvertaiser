"""Custom dimension management tools for Google Analytics."""

from typing import Any, Optional

from google.api_core.exceptions import GoogleAPICallError
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import get_admin_client, resolve_property_id, format_property_name

from google.analytics.admin_v1beta.types import CustomDimension


def _custom_dimension_to_dict(dim) -> dict[str, Any]:
    """Convert a CustomDimension protobuf object to a plain dictionary."""
    return {
        "name": dim.name,
        "parameter_name": dim.parameter_name,
        "display_name": dim.display_name,
        "description": dim.description,
        "scope": dim.scope.name if dim.scope else None,
        "disallow_ads_personalization": dim.disallow_ads_personalization,
    }


@mcp.tool()
def ga4_list_custom_dimensions(
    property_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Lists all custom dimensions for a Google Analytics 4 property.

    Custom dimensions let you segment and analyze data by custom criteria
    like page type, content category, or user role.

    Args:
        property_id: The GA4 property ID (numeric, e.g. "123456789").
            Uses default from config if not provided.

    Returns:
        list[dict]: List of custom dimensions with:
            - name: Full resource name (properties/{id}/customDimensions/{id})
            - parameter_name: The event parameter name (e.g. "page_type")
            - display_name: Human-readable name shown in GA4 UI
            - description: Optional description
            - scope: EVENT, USER, or ITEM
            - disallow_ads_personalization: Whether ads personalization is disabled

    Raises:
        ToolError: If the API request fails.
    """
    try:
        property_id = resolve_property_id(property_id)
        client = get_admin_client()
        dimensions = client.list_custom_dimensions(
            parent=format_property_name(property_id),
        )
        return [_custom_dimension_to_dict(dim) for dim in dimensions]
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to list custom dimensions: {e.message}") from e


@mcp.tool()
def ga4_create_custom_dimension(
    parameter_name: str,
    display_name: str,
    scope: str = "EVENT",
    description: str = "",
    property_id: Optional[str] = None,
) -> dict[str, Any]:
    """Creates a custom dimension for a Google Analytics 4 property.

    Custom dimensions let you segment traffic by custom criteria without
    touching website code. The event parameter must already be sent by
    your tracking code or GTM.

    Common examples:
        - page_type (EVENT scope): "blog", "product", "landing_page", "case_study"
        - user_role (USER scope): "free", "premium", "enterprise"
        - item_category (ITEM scope): for ecommerce item-level dimensions

    Args:
        parameter_name: The event parameter name to register as a dimension.
            Must match what your tracking code sends (e.g. "page_type").
            Max 24 characters for event-scoped, 24 for user-scoped.
        display_name: Human-readable name shown in GA4 reports
            (e.g. "Page Type"). Max 82 characters.
        scope: Dimension scope. Options:
            - EVENT: Applies to individual events (default, most common)
            - USER: Applies to the user across all events
            - ITEM: Applies to ecommerce items
        description: Optional description (max 150 characters).
        property_id: The GA4 property ID. Uses default from config if not provided.

    Returns:
        dict: Created custom dimension with name, parameter_name, display_name,
            description, scope, and disallow_ads_personalization fields.

    Raises:
        ToolError: If the API request fails.
    """
    try:
        property_id = resolve_property_id(property_id)
        client = get_admin_client()

        custom_dimension = CustomDimension(
            parameter_name=parameter_name,
            display_name=display_name,
            description=description,
            scope=CustomDimension.DimensionScope[scope],
        )

        result = client.create_custom_dimension(
            parent=format_property_name(property_id),
            custom_dimension=custom_dimension,
        )
        return _custom_dimension_to_dict(result)
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to create custom dimension: {e.message}") from e


@mcp.tool()
def ga4_update_custom_dimension(
    custom_dimension_name: str,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
) -> dict[str, Any]:
    """Updates an existing custom dimension's display name or description.

    Note: parameter_name and scope cannot be changed after creation.

    Args:
        custom_dimension_name: Full resource name
            (e.g. "properties/123456/customDimensions/789").
        display_name: New display name (max 82 characters).
        description: New description (max 150 characters).

    Returns:
        dict: Updated custom dimension.

    Raises:
        ToolError: If the API request fails or no fields to update.
    """
    update_paths = []
    if display_name is not None:
        update_paths.append("display_name")
    if description is not None:
        update_paths.append("description")

    if not update_paths:
        raise ToolError("At least one of display_name or description must be provided.")

    try:
        from google.protobuf.field_mask_pb2 import FieldMask

        client = get_admin_client()

        kwargs: dict[str, Any] = {"name": custom_dimension_name}
        if display_name is not None:
            kwargs["display_name"] = display_name
        if description is not None:
            kwargs["description"] = description

        dim = CustomDimension(**kwargs)

        result = client.update_custom_dimension(
            custom_dimension=dim,
            update_mask=FieldMask(paths=update_paths),
        )
        return _custom_dimension_to_dict(result)
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to update custom dimension: {e.message}") from e


@mcp.tool()
def ga4_archive_custom_dimension(
    custom_dimension_name: str,
) -> dict[str, Any]:
    """Archives (soft-deletes) a custom dimension from a GA4 property.

    Archived dimensions are hidden from reports but historical data
    is retained. This cannot be undone.

    Args:
        custom_dimension_name: Full resource name
            (e.g. "properties/123456/customDimensions/789").

    Returns:
        dict: Confirmation with status and name.

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_admin_client()
        client.archive_custom_dimension(name=custom_dimension_name)
        return {"status": "archived", "name": custom_dimension_name}
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to archive custom dimension: {e.message}") from e
