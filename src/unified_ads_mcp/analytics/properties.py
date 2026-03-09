"""Property management tools for Google Analytics."""

from typing import Any, Optional
from google.api_core.exceptions import GoogleAPICallError
from google.analytics.admin_v1beta.types import (
    ListPropertiesRequest,
    Property,
    IndustryCategory,
)
from google.protobuf.field_mask_pb2 import FieldMask
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import get_admin_client, resolve_property_id, format_property_name


def _property_to_dict(prop) -> dict[str, Any]:
    """Convert a Property protobuf message to a dictionary.

    Args:
        prop: A google.analytics.admin_v1beta.types.Property instance.

    Returns:
        A JSON-serializable dictionary with property fields.
    """
    return {
        "id": prop.name.split("/")[-1] if prop.name else None,
        "name": prop.name,
        "display_name": prop.display_name,
        "property_type": prop.property_type.name if prop.property_type else None,
        "time_zone": prop.time_zone,
        "currency_code": prop.currency_code,
        "industry_category": prop.industry_category.name if prop.industry_category else None,
        "service_level": prop.service_level.name if prop.service_level else None,
        "account": prop.account,
        "parent": prop.parent,
        "create_time": prop.create_time.isoformat() if prop.create_time else None,
        "update_time": prop.update_time.isoformat() if prop.update_time else None,
    }


@mcp.tool()
def ga4_list_properties(account_id: str) -> list[dict[str, Any]]:
    """Lists all GA4 properties for a given account.

    Args:
        account_id: The Google Analytics account ID (digits only).

    Returns:
        list[dict]: List of properties with id, name, display_name, property_type,
            time_zone, currency_code, industry_category, service_level, account,
            create_time, and update_time.

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_admin_client()
        request = ListPropertiesRequest(
            filter=f"parent:accounts/{account_id}"
        )
        properties = list(client.list_properties(request))
        return [_property_to_dict(prop) for prop in properties]
    except GoogleAPICallError as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def ga4_get_property(property_id: Optional[str] = None) -> dict[str, Any]:
    """Gets detailed information about a specific GA4 property.

    Args:
        property_id: The GA4 property ID (digits only). Uses default from
            config if not provided.

    Returns:
        dict: Property details including id, name, display_name, property_type,
            time_zone, currency_code, industry_category, service_level, account,
            create_time, and update_time.

    Raises:
        ToolError: If the property is not found or the API request fails.
    """
    try:
        property_id = resolve_property_id(property_id)
        client = get_admin_client()
        prop = client.get_property(name=format_property_name(property_id))
        return _property_to_dict(prop)
    except ValueError as e:
        raise ToolError(str(e)) from e
    except GoogleAPICallError as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def ga4_create_property(
    account_id: str,
    display_name: str,
    time_zone: str,
    currency_code: str = "USD",
    industry_category: Optional[str] = None,
) -> dict[str, Any]:
    """Creates a new GA4 property under an account.

    Args:
        account_id: The Google Analytics account ID (digits only).
        display_name: The display name for the property (max 100 UTF-16 code units).
        time_zone: IANA time zone string (e.g., "America/Los_Angeles", "Europe/Prague").
        currency_code: ISO 4217 currency code (e.g., "USD", "EUR", "CZK"). Defaults to "USD".
        industry_category: Optional industry category. Valid values include:
            AUTOMOTIVE, BUSINESS_AND_INDUSTRIAL_MARKETS, FINANCE, HEALTHCARE,
            TECHNOLOGY, TRAVEL, OTHER, ARTS_AND_ENTERTAINMENT, BEAUTY_AND_FITNESS,
            BOOKS_AND_LITERATURE, FOOD_AND_DRINK, GAMES, HOBBIES_AND_LEISURE,
            HOME_AND_GARDEN, INTERNET_AND_TELECOM, LAW_AND_GOVERNMENT,
            NEWS, ONLINE_COMMUNITIES, PEOPLE_AND_SOCIETY, PETS_AND_ANIMALS,
            REAL_ESTATE, REFERENCE, SCIENCE, SHOPPING, SPORTS, JOBS_AND_EDUCATION.

    Returns:
        dict: The created property details including id, name, display_name,
            property_type, time_zone, currency_code, industry_category,
            service_level, account, create_time, and update_time.

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_admin_client()
        prop = Property(
            parent=f"accounts/{account_id}",
            display_name=display_name,
            time_zone=time_zone,
            currency_code=currency_code,
        )
        if industry_category:
            prop.industry_category = IndustryCategory[industry_category]
        created = client.create_property(property=prop)
        return _property_to_dict(created)
    except KeyError as e:
        raise ToolError(f"Invalid industry_category: {e}") from e
    except GoogleAPICallError as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def ga4_update_property(
    property_id: Optional[str] = None,
    display_name: Optional[str] = None,
    time_zone: Optional[str] = None,
    currency_code: Optional[str] = None,
    industry_category: Optional[str] = None,
) -> dict[str, Any]:
    """Updates an existing GA4 property.

    Only the fields that are provided will be updated. At least one field
    must be specified.

    Args:
        property_id: The GA4 property ID (digits only). Uses default from
            config if not provided.
        display_name: Optional new display name for the property.
        time_zone: Optional new IANA time zone string.
        currency_code: Optional new ISO 4217 currency code.
        industry_category: Optional new industry category (see ga4_create_property
            for valid values).

    Returns:
        dict: The updated property details including id, name, display_name,
            property_type, time_zone, currency_code, industry_category,
            service_level, account, create_time, and update_time.

    Raises:
        ToolError: If no fields to update or the API request fails.
    """
    try:
        property_id = resolve_property_id(property_id)
        client = get_admin_client()

        prop = Property(name=format_property_name(property_id))
        update_fields = []

        if display_name is not None:
            prop.display_name = display_name
            update_fields.append("display_name")

        if time_zone is not None:
            prop.time_zone = time_zone
            update_fields.append("time_zone")

        if currency_code is not None:
            prop.currency_code = currency_code
            update_fields.append("currency_code")

        if industry_category is not None:
            prop.industry_category = IndustryCategory[industry_category]
            update_fields.append("industry_category")

        if not update_fields:
            raise ToolError(
                "No fields to update. Provide at least one of: "
                "display_name, time_zone, currency_code, industry_category."
            )

        update_mask = FieldMask(paths=update_fields)
        updated = client.update_property(
            property=prop, update_mask=update_mask
        )
        return _property_to_dict(updated)
    except KeyError as e:
        raise ToolError(f"Invalid industry_category: {e}") from e
    except ValueError as e:
        raise ToolError(str(e)) from e
    except GoogleAPICallError as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def ga4_delete_property(property_id: str) -> dict[str, Any]:
    """Soft-deletes a GA4 property (moves it to trash).

    The property can be restored within 35 days using the Google Analytics UI.
    After 35 days, the property and all associated data are permanently deleted.

    Args:
        property_id: The GA4 property ID to delete (digits only).

    Returns:
        dict: Confirmation with the deleted property details including id, name,
            display_name, and a status field set to "deleted".

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_admin_client()
        deleted = client.delete_property(
            name=format_property_name(property_id)
        )
        result = _property_to_dict(deleted)
        result["status"] = "deleted"
        return result
    except GoogleAPICallError as e:
        raise ToolError(str(e)) from e
