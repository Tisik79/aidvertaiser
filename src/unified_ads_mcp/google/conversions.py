"""Conversion management tools for Google Ads API.

This module provides MCP tools for managing conversion actions, uploading
offline conversions, and configuring campaign conversion goals.
"""

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

from google.ads.googleads.errors import GoogleAdsException
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import (
    get_google_ads_client,
    format_error,
    resolve_customer_id,
    get_enum_name,
    get_enum_value,
)


@mcp.tool()
def google_list_conversion_actions(
    customer_id: Optional[str] = None,
    status: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Lists all conversion actions for a Google Ads customer.

    Conversion actions define what counts as a conversion (e.g., purchase,
    lead form submission, phone call). Each campaign optimizes toward one
    or more of these actions.

    Args:
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        status: Optional filter by status - ENABLED, REMOVED, or HIDDEN.
        login_customer_id: Optional MCC account ID.

    Returns:
        list[dict]: List of conversion actions with:
            - id: Conversion action ID
            - name: Conversion action name
            - type: Type (WEBPAGE, PHONE_CALL, UPLOAD, etc.)
            - category: Category (PURCHASE, SUBMIT_LEAD_FORM, SIGNUP, etc.)
            - status: Status (ENABLED, REMOVED, HIDDEN)
            - counting_type: ONE_PER_CLICK or MANY_PER_CLICK
            - attribution_model: Attribution model type
            - value_settings: Default value and currency
            - tag_snippets: Tracking tag info (if website type)
            - click_through_lookback_window_days: Lookback window
            - view_through_lookback_window_days: View-through window
            - include_in_conversions_metric: Whether included in "Conversions"

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = """
            SELECT
                conversion_action.id,
                conversion_action.name,
                conversion_action.type,
                conversion_action.category,
                conversion_action.status,
                conversion_action.counting_type,
                conversion_action.attribution_model_settings.attribution_model,
                conversion_action.attribution_model_settings.data_driven_model_status,
                conversion_action.value_settings.default_value,
                conversion_action.value_settings.default_currency_code,
                conversion_action.value_settings.always_use_default_value,
                conversion_action.click_through_lookback_window_days,
                conversion_action.view_through_lookback_window_days,
                conversion_action.include_in_conversions_metric,
                conversion_action.tag_snippets,
                conversion_action.phone_call_duration_seconds,
                conversion_action.origin
            FROM conversion_action
        """

        if status:
            query += f" WHERE conversion_action.status = '{status.upper()}'"

        query += " ORDER BY conversion_action.id"

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        actions = []
        for batch in response:
            for row in batch.results:
                ca = row.conversion_action
                action_data = {
                    "id": str(ca.id),
                    "name": ca.name,
                    "type": get_enum_name(client, "ConversionActionTypeEnum", ca.type_),
                    "category": get_enum_name(
                        client,
                        "ConversionActionCategoryEnum",
                        ca.category,
                    ),
                    "status": get_enum_name(
                        client,
                        "ConversionActionStatusEnum",
                        ca.status,
                    ),
                    "counting_type": get_enum_name(
                        client,
                        "ConversionActionCountingTypeEnum",
                        ca.counting_type,
                    ),
                    "attribution_model": get_enum_name(
                        client,
                        "AttributionModelEnum",
                        ca.attribution_model_settings.attribution_model,
                    ),
                    "default_value": ca.value_settings.default_value,
                    "default_currency": ca.value_settings.default_currency_code,
                    "always_use_default_value": ca.value_settings.always_use_default_value,
                    "click_through_lookback_days": ca.click_through_lookback_window_days,
                    "view_through_lookback_days": ca.view_through_lookback_window_days,
                    "include_in_conversions": ca.include_in_conversions_metric,
                    "origin": get_enum_name(client, "ConversionOriginEnum", ca.origin),
                }

                if ca.phone_call_duration_seconds:
                    action_data["phone_call_duration_seconds"] = (
                        ca.phone_call_duration_seconds
                    )

                actions.append(action_data)

        return actions

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_get_conversion_action(
    conversion_action_id: str,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Gets detailed information about a specific conversion action.

    Args:
        conversion_action_id: The conversion action ID.
        customer_id: The Google Ads customer ID.
            Uses default from config if not provided.
        login_customer_id: Optional MCC account ID.

    Returns:
        dict: Conversion action details including all configuration fields
            and tag snippet information for website conversions.

    Raises:
        ToolError: If not found or API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = f"""
            SELECT
                conversion_action.id,
                conversion_action.name,
                conversion_action.type,
                conversion_action.category,
                conversion_action.status,
                conversion_action.counting_type,
                conversion_action.attribution_model_settings.attribution_model,
                conversion_action.attribution_model_settings.data_driven_model_status,
                conversion_action.value_settings.default_value,
                conversion_action.value_settings.default_currency_code,
                conversion_action.value_settings.always_use_default_value,
                conversion_action.click_through_lookback_window_days,
                conversion_action.view_through_lookback_window_days,
                conversion_action.include_in_conversions_metric,
                conversion_action.tag_snippets,
                conversion_action.phone_call_duration_seconds,
                conversion_action.origin,
                conversion_action.primary_for_goal
            FROM conversion_action
            WHERE conversion_action.id = {conversion_action_id}
        """

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        for batch in response:
            for row in batch.results:
                ca = row.conversion_action
                result = {
                    "id": str(ca.id),
                    "name": ca.name,
                    "resource_name": ca.resource_name,
                    "type": get_enum_name(client, "ConversionActionTypeEnum", ca.type_),
                    "category": get_enum_name(
                        client, "ConversionActionCategoryEnum", ca.category
                    ),
                    "status": get_enum_name(
                        client, "ConversionActionStatusEnum", ca.status
                    ),
                    "counting_type": get_enum_name(
                        client,
                        "ConversionActionCountingTypeEnum",
                        ca.counting_type,
                    ),
                    "attribution_model": get_enum_name(
                        client,
                        "AttributionModelEnum",
                        ca.attribution_model_settings.attribution_model,
                    ),
                    "default_value": ca.value_settings.default_value,
                    "default_currency": ca.value_settings.default_currency_code,
                    "always_use_default_value": ca.value_settings.always_use_default_value,
                    "click_through_lookback_days": ca.click_through_lookback_window_days,
                    "view_through_lookback_days": ca.view_through_lookback_window_days,
                    "include_in_conversions": ca.include_in_conversions_metric,
                    "primary_for_goal": ca.primary_for_goal,
                    "origin": get_enum_name(client, "ConversionOriginEnum", ca.origin),
                }

                # Extract tag snippets if available
                if ca.tag_snippets:
                    result["tag_snippets"] = []
                    for snippet in ca.tag_snippets:
                        result["tag_snippets"].append(
                            {
                                "type": get_enum_name(
                                    client,
                                    "TrackingCodeTypeEnum",
                                    snippet.type_,
                                ),
                                "page_format": get_enum_name(
                                    client,
                                    "TrackingCodePageFormatEnum",
                                    snippet.page_format,
                                ),
                                "global_site_tag": snippet.global_site_tag,
                                "event_snippet": snippet.event_snippet,
                            }
                        )

                return result

        raise ToolError(f"Conversion action {conversion_action_id} not found")

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_create_conversion_action(
    name: str,
    type: str = "WEBPAGE",
    category: str = "DEFAULT",
    customer_id: Optional[str] = None,
    counting_type: str = "ONE_PER_CLICK",
    default_value: Optional[float] = None,
    default_currency: Optional[str] = None,
    always_use_default_value: bool = False,
    click_through_lookback_days: int = 30,
    view_through_lookback_days: int = 1,
    attribution_model: str = "GOOGLE_SEARCH_ATTRIBUTION_DATA_DRIVEN",
    include_in_conversions: bool = True,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Creates a new conversion action.

    A conversion action defines what event counts as a conversion.
    After creation, use the returned tag_snippets to add tracking
    code to your website (for WEBPAGE type).

    Args:
        name: Conversion action name (e.g., "Lead Form Submission").
        type: Conversion type. Options:
            - WEBPAGE: Website conversion (default, generates tracking tag)
            - PHONE_CALL: Phone call conversion
            - UPLOAD: Offline/imported conversion (for CRM uploads)
            - UPLOAD_CALLS: Imported phone call conversion
        category: Conversion category. Options:
            - DEFAULT, PURCHASE, ADD_TO_CART, BEGIN_CHECKOUT,
              SIGNUP, SUBSCRIBE_PAID, PAGE_VIEW,
              CONTACT, SUBMIT_LEAD_FORM, BOOK_APPOINTMENT,
              REQUEST_QUOTE, GET_DIRECTIONS, DOWNLOAD,
              QUALIFIED_LEAD, CONVERTED_LEAD, IMPORTED_LEAD
        customer_id: Google Ads customer ID.
            Uses default from config if not provided.
        counting_type: How to count conversions:
            - ONE_PER_CLICK: Count max 1 conversion per click (leads)
            - MANY_PER_CLICK: Count every conversion per click (purchases)
        default_value: Default monetary value per conversion.
        default_currency: Currency code for default value (e.g., "CZK").
        always_use_default_value: If True, always use default value
            instead of transaction-specific values.
        click_through_lookback_days: Days after click to track (1-90, default 30).
        view_through_lookback_days: Days after view to track (1-30, default 1).
        attribution_model: Attribution model. Options:
            - GOOGLE_SEARCH_ATTRIBUTION_DATA_DRIVEN (recommended)
            - GOOGLE_SEARCH_ATTRIBUTION_LAST_CLICK
            - GOOGLE_SEARCH_ATTRIBUTION_FIRST_CLICK
            - GOOGLE_SEARCH_ATTRIBUTION_LINEAR
            - GOOGLE_SEARCH_ATTRIBUTION_TIME_DECAY
            - GOOGLE_SEARCH_ATTRIBUTION_POSITION_BASED
        include_in_conversions: Whether to include in the "Conversions"
            column (affects Smart Bidding).
        login_customer_id: Optional MCC account ID.

    Returns:
        dict: Created conversion action with:
            - id: Conversion action ID
            - resource_name: Full resource name
            - status: "created"

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        conversion_action_service = client.get_service("ConversionActionService")
        conversion_action_operation = client.get_type("ConversionActionOperation")
        conversion_action = conversion_action_operation.create

        conversion_action.name = name
        conversion_action.type_ = get_enum_value(
            client, "ConversionActionTypeEnum", type
        )
        conversion_action.category = get_enum_value(
            client, "ConversionActionCategoryEnum", category
        )
        conversion_action.counting_type = get_enum_value(
            client, "ConversionActionCountingTypeEnum", counting_type
        )
        conversion_action.status = get_enum_value(
            client, "ConversionActionStatusEnum", "ENABLED"
        )

        # Value settings
        if default_value is not None:
            conversion_action.value_settings.default_value = default_value
        if default_currency:
            conversion_action.value_settings.default_currency_code = default_currency
        conversion_action.value_settings.always_use_default_value = (
            always_use_default_value
        )

        # Lookback windows
        conversion_action.click_through_lookback_window_days = (
            click_through_lookback_days
        )
        conversion_action.view_through_lookback_window_days = view_through_lookback_days

        # Attribution model
        conversion_action.attribution_model_settings.attribution_model = get_enum_value(
            client, "AttributionModelEnum", attribution_model
        )

        # Note: include_in_conversions_metric is immutable during creation.
        # Use google_update_conversion_action after creation to change it.

        response = conversion_action_service.mutate_conversion_actions(
            customer_id=customer_id,
            operations=[conversion_action_operation],
        )

        result = response.results[0]
        return {
            "id": result.resource_name.split("/")[-1],
            "resource_name": result.resource_name,
            "status": "created",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_update_conversion_action(
    conversion_action_id: str,
    customer_id: Optional[str] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
    counting_type: Optional[str] = None,
    default_value: Optional[float] = None,
    default_currency: Optional[str] = None,
    always_use_default_value: Optional[bool] = None,
    click_through_lookback_days: Optional[int] = None,
    view_through_lookback_days: Optional[int] = None,
    attribution_model: Optional[str] = None,
    include_in_conversions: Optional[bool] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Updates an existing conversion action.

    Args:
        conversion_action_id: The conversion action ID.
        customer_id: Google Ads customer ID.
            Uses default from config if not provided.
        name: New name.
        status: New status (ENABLED, REMOVED, HIDDEN).
        category: New category.
        counting_type: New counting type (ONE_PER_CLICK, MANY_PER_CLICK).
        default_value: New default value.
        default_currency: New default currency code.
        always_use_default_value: Whether to always use default value.
        click_through_lookback_days: New click-through lookback (1-90).
        view_through_lookback_days: New view-through lookback (1-30).
        attribution_model: New attribution model.
        include_in_conversions: Whether to include in Conversions metric.
        login_customer_id: Optional MCC account ID.

    Returns:
        dict: Updated conversion action info.

    Raises:
        ToolError: If no fields to update or API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        conversion_action_service = client.get_service("ConversionActionService")
        conversion_action_operation = client.get_type("ConversionActionOperation")
        conversion_action = conversion_action_operation.update
        conversion_action.resource_name = (
            f"customers/{customer_id}/conversionActions/{conversion_action_id}"
        )

        field_mask = []

        if name is not None:
            conversion_action.name = name
            field_mask.append("name")
        if status is not None:
            conversion_action.status = get_enum_value(
                client, "ConversionActionStatusEnum", status
            )
            field_mask.append("status")
        if category is not None:
            conversion_action.category = get_enum_value(
                client, "ConversionActionCategoryEnum", category
            )
            field_mask.append("category")
        if counting_type is not None:
            conversion_action.counting_type = get_enum_value(
                client, "ConversionActionCountingTypeEnum", counting_type
            )
            field_mask.append("counting_type")
        if default_value is not None:
            conversion_action.value_settings.default_value = default_value
            field_mask.append("value_settings.default_value")
        if default_currency is not None:
            conversion_action.value_settings.default_currency_code = default_currency
            field_mask.append("value_settings.default_currency_code")
        if always_use_default_value is not None:
            conversion_action.value_settings.always_use_default_value = (
                always_use_default_value
            )
            field_mask.append("value_settings.always_use_default_value")
        if click_through_lookback_days is not None:
            conversion_action.click_through_lookback_window_days = (
                click_through_lookback_days
            )
            field_mask.append("click_through_lookback_window_days")
        if view_through_lookback_days is not None:
            conversion_action.view_through_lookback_window_days = (
                view_through_lookback_days
            )
            field_mask.append("view_through_lookback_window_days")
        if attribution_model is not None:
            conversion_action.attribution_model_settings.attribution_model = (
                get_enum_value(client, "AttributionModelEnum", attribution_model)
            )
            field_mask.append("attribution_model_settings.attribution_model")
        if include_in_conversions is not None:
            # NOTE: include_in_conversions_metric is READ-ONLY since API v15+.
            # Use primary_for_goal instead, and set CustomerConversionGoal.biddable
            # via google_update_customer_conversion_goal.
            conversion_action.primary_for_goal = include_in_conversions
            field_mask.append("primary_for_goal")

        if not field_mask:
            raise ToolError("No fields to update. Provide at least one field.")

        conversion_action_operation.update_mask.paths.extend(field_mask)

        response = conversion_action_service.mutate_conversion_actions(
            customer_id=customer_id,
            operations=[conversion_action_operation],
        )

        return {
            "resource_name": response.results[0].resource_name,
            "updated_fields": field_mask,
            "status": "updated",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_delete_conversion_action(
    conversion_action_id: str,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Removes a conversion action.

    Sets the conversion action status to REMOVED. Historical data
    is retained but no new conversions will be tracked.

    Args:
        conversion_action_id: The conversion action ID to remove.
        customer_id: Google Ads customer ID.
            Uses default from config if not provided.
        login_customer_id: Optional MCC account ID.

    Returns:
        dict: Removal status.

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        conversion_action_service = client.get_service("ConversionActionService")
        conversion_action_operation = client.get_type("ConversionActionOperation")
        conversion_action_operation.remove = (
            f"customers/{customer_id}/conversionActions/{conversion_action_id}"
        )

        response = conversion_action_service.mutate_conversion_actions(
            customer_id=customer_id,
            operations=[conversion_action_operation],
        )

        return {
            "resource_name": response.results[0].resource_name,
            "status": "removed",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_get_conversion_action_performance(
    customer_id: Optional[str] = None,
    date_range: str = "LAST_30_DAYS",
    conversion_action_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Gets performance metrics broken down by conversion action.

    Shows how many conversions each action generated and their value,
    useful for understanding which conversion types drive results.

    Args:
        customer_id: Google Ads customer ID.
            Uses default from config if not provided.
        date_range: Predefined date range (e.g., LAST_30_DAYS).
        conversion_action_id: Optional specific conversion action ID.
        login_customer_id: Optional MCC account ID.

    Returns:
        list[dict]: Performance by conversion action with:
            - conversion_action_id, name, category
            - all_conversions, all_conversions_value
            - conversions, conversions_value
            - view_through_conversions

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = f"""
            SELECT
                segments.conversion_action,
                segments.conversion_action_name,
                segments.conversion_action_category,
                metrics.all_conversions,
                metrics.all_conversions_value,
                metrics.conversions,
                metrics.conversions_value,
                metrics.view_through_conversions
            FROM customer
            WHERE segments.date DURING {date_range}
        """

        if conversion_action_id:
            query += f" AND segments.conversion_action ~ 'conversionActions/{conversion_action_id}'"

        query += " ORDER BY metrics.all_conversions DESC"

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        results = []
        for batch in response:
            for row in batch.results:
                # Extract conversion action ID from resource name
                # Format: customers/123/conversionActions/456
                ca_resource = row.segments.conversion_action
                ca_id = ca_resource.rsplit("/", 1)[-1] if ca_resource else ""
                results.append(
                    {
                        "conversion_action_id": ca_id,
                        "name": row.segments.conversion_action_name,
                        "category": get_enum_name(
                            client,
                            "ConversionActionCategoryEnum",
                            row.segments.conversion_action_category,
                        ),
                        "all_conversions": row.metrics.all_conversions,
                        "all_conversions_value": row.metrics.all_conversions_value,
                        "conversions": row.metrics.conversions,
                        "conversions_value": row.metrics.conversions_value,
                        "view_through_conversions": row.metrics.view_through_conversions,
                    }
                )

        return results

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_upload_offline_conversions(
    conversion_action_id: str,
    conversions: list[dict[str, Any]],
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Uploads offline conversions to Google Ads.

    Use this to import conversions from CRM systems (like EspoCRM)
    back to Google Ads, enabling Smart Bidding to optimize for
    actual business outcomes (e.g., qualified leads, closed deals).

    The conversion_action must be of type UPLOAD (created with
    google_create_conversion_action with type="UPLOAD").

    Args:
        conversion_action_id: ID of the UPLOAD-type conversion action.
        conversions: List of conversion records. Each must contain:
            - gclid: Google Click ID from the original ad click
            - conversion_date_time: When conversion happened
              (format: "2025-01-15 12:30:00+01:00")
            - conversion_value: Optional monetary value
            - currency_code: Optional currency (e.g., "CZK")
            - order_id: Optional unique order/transaction ID
        customer_id: Google Ads customer ID.
            Uses default from config if not provided.
        login_customer_id: Optional MCC account ID.

    Returns:
        dict: Upload results with:
            - total_uploaded: Number of conversions uploaded
            - partial_failure_errors: Any individual failures
            - status: "uploaded" or "partial_failure"

    Raises:
        ToolError: If the API request fails.

    Example:
        >>> google_upload_offline_conversions(
        ...     conversion_action_id="123456789",
        ...     conversions=[
        ...         {
        ...             "gclid": "CjwKCAjw...",
        ...             "conversion_date_time": "2025-01-15 14:30:00+01:00",
        ...             "conversion_value": 5000.0,
        ...             "currency_code": "CZK"
        ...         }
        ...     ]
        ... )
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        conversion_upload_service = client.get_service("ConversionUploadService")
        conversion_action_service = client.get_service("ConversionActionService")

        # Build the conversion action resource name
        conversion_action_resource = conversion_action_service.conversion_action_path(
            customer_id, conversion_action_id
        )

        click_conversions = []
        for conv in conversions:
            click_conversion = client.get_type("ClickConversion")
            click_conversion.conversion_action = conversion_action_resource
            click_conversion.gclid = conv["gclid"]
            click_conversion.conversion_date_time = conv["conversion_date_time"]

            if "conversion_value" in conv:
                click_conversion.conversion_value = conv["conversion_value"]
            if "currency_code" in conv:
                click_conversion.currency_code = conv["currency_code"]
            if "order_id" in conv:
                click_conversion.order_id = conv["order_id"]

            click_conversions.append(click_conversion)

        request = client.get_type("UploadClickConversionsRequest")
        request.customer_id = customer_id
        request.conversions = click_conversions
        request.partial_failure = True

        response = conversion_upload_service.upload_click_conversions(
            request=request,
        )

        errors = []
        if response.partial_failure_error:
            for error in response.partial_failure_error.details:
                errors.append(str(error))

        return {
            "total_uploaded": len(click_conversions),
            "results_count": len(response.results),
            "partial_failure_errors": errors if errors else None,
            "status": "partial_failure" if errors else "uploaded",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_upload_enhanced_conversions(
    conversion_action_id: str,
    conversions: list[dict[str, Any]],
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Uploads enhanced conversions with user identifiers for better matching.

    Enhanced conversions use hashed user data (email, phone, address)
    to improve conversion attribution when GCLID is not available.
    Data is automatically SHA-256 hashed before sending.

    Args:
        conversion_action_id: ID of the conversion action.
        conversions: List of conversion records. Each must contain:
            - conversion_date_time: When conversion happened
              (format: "2025-01-15 12:30:00+01:00")
            - conversion_value: Optional monetary value
            - currency_code: Optional currency code
            - order_id: Optional unique transaction ID
            - user_identifiers: Dict with at least one of:
                - email: User email address (will be hashed)
                - phone: Phone in E.164 format (will be hashed)
                - first_name: First name (will be hashed)
                - last_name: Last name (will be hashed)
                - street_address: Street address (will be hashed)
                - city: City
                - region: State/region
                - postal_code: Postal code
                - country_code: 2-letter country code
            - gclid: Optional Google Click ID (for additional matching)
        customer_id: Google Ads customer ID.
        login_customer_id: Optional MCC account ID.

    Returns:
        dict: Upload results with total_uploaded, errors, status.

    Raises:
        ToolError: If the API request fails.
    """
    import hashlib

    def _hash_value(value: str) -> str:
        """SHA-256 hash a value after normalizing."""
        return hashlib.sha256(value.strip().lower().encode("utf-8")).hexdigest()

    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        conversion_upload_service = client.get_service("ConversionUploadService")
        conversion_action_service = client.get_service("ConversionActionService")

        conversion_action_resource = conversion_action_service.conversion_action_path(
            customer_id, conversion_action_id
        )

        click_conversions = []
        for conv in conversions:
            click_conversion = client.get_type("ClickConversion")
            click_conversion.conversion_action = conversion_action_resource
            click_conversion.conversion_date_time = conv["conversion_date_time"]

            if "conversion_value" in conv:
                click_conversion.conversion_value = conv["conversion_value"]
            if "currency_code" in conv:
                click_conversion.currency_code = conv["currency_code"]
            if "order_id" in conv:
                click_conversion.order_id = conv["order_id"]
            if "gclid" in conv:
                click_conversion.gclid = conv["gclid"]

            # Add user identifiers
            identifiers = conv.get("user_identifiers", {})

            if "email" in identifiers:
                user_id = client.get_type("UserIdentifier")
                user_id.hashed_email = _hash_value(identifiers["email"])
                click_conversion.user_identifiers.append(user_id)

            if "phone" in identifiers:
                user_id = client.get_type("UserIdentifier")
                user_id.hashed_phone_number = _hash_value(identifiers["phone"])
                click_conversion.user_identifiers.append(user_id)

            if any(
                k in identifiers for k in ["first_name", "last_name", "street_address"]
            ):
                user_id = client.get_type("UserIdentifier")
                address_info = user_id.address_info
                if "first_name" in identifiers:
                    address_info.hashed_first_name = _hash_value(
                        identifiers["first_name"]
                    )
                if "last_name" in identifiers:
                    address_info.hashed_last_name = _hash_value(
                        identifiers["last_name"]
                    )
                if "street_address" in identifiers:
                    address_info.hashed_street_address = _hash_value(
                        identifiers["street_address"]
                    )
                if "city" in identifiers:
                    address_info.city = identifiers["city"]
                if "region" in identifiers:
                    address_info.region = identifiers["region"]
                if "postal_code" in identifiers:
                    address_info.postal_code = identifiers["postal_code"]
                if "country_code" in identifiers:
                    address_info.country_code = identifiers["country_code"]
                click_conversion.user_identifiers.append(user_id)

            click_conversions.append(click_conversion)

        request = client.get_type("UploadClickConversionsRequest")
        request.customer_id = customer_id
        request.conversions = click_conversions
        request.partial_failure = True

        response = conversion_upload_service.upload_click_conversions(
            request=request,
        )

        errors = []
        if response.partial_failure_error:
            for error in response.partial_failure_error.details:
                errors.append(str(error))

        return {
            "total_uploaded": len(click_conversions),
            "results_count": len(response.results),
            "partial_failure_errors": errors if errors else None,
            "status": "partial_failure" if errors else "uploaded",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_set_campaign_conversion_goal(
    campaign_id: str,
    conversion_action_ids: Any,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Sets which conversion actions a campaign should optimize for.

    By default, campaigns use account-level conversion goals.
    Use this to override with campaign-specific goals, e.g., to have
    one campaign optimize for leads and another for purchases.

    Args:
        campaign_id: The campaign ID.
        conversion_action_ids: List of conversion action IDs this
            campaign should optimize for.
        customer_id: Google Ads customer ID.
        login_customer_id: Optional MCC account ID.

    Returns:
        dict: Result with campaign_id and configured goals.

    Raises:
        ToolError: If the API request fails.
    """
    conversion_action_ids = _coerce_list(conversion_action_ids)

    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        ga_service = client.get_service("GoogleAdsService")
        conversion_goal_service = client.get_service("CampaignConversionGoalService")
        # First, get current campaign conversion goals to know what exists
        query = f"""
            SELECT
                campaign_conversion_goal.campaign,
                campaign_conversion_goal.category,
                campaign_conversion_goal.origin,
                campaign_conversion_goal.biddable
            FROM campaign_conversion_goal
            WHERE campaign.id = {campaign_id}
        """

        response = ga_service.search_stream(customer_id=customer_id, query=query)

        # Get the conversion action details to know their categories/origins
        action_details = {}
        for action_id in conversion_action_ids:
            action_query = f"""
                SELECT
                    conversion_action.id,
                    conversion_action.category,
                    conversion_action.origin
                FROM conversion_action
                WHERE conversion_action.id = {action_id}
            """
            action_response = ga_service.search_stream(
                customer_id=customer_id, query=action_query
            )
            for batch in action_response:
                for row in batch.results:
                    action_details[str(row.conversion_action.id)] = {
                        "category": row.conversion_action.category,
                        "origin": row.conversion_action.origin,
                    }

        # Build mutate operations to set biddable flags
        operations = []
        existing_goals = {}
        for batch in response:
            for row in batch.results:
                goal = row.campaign_conversion_goal
                key = (goal.category, goal.origin)
                existing_goals[key] = goal

        # Update existing goals: set biddable=True for matching, False for others
        target_keys = set()
        for action_id, details in action_details.items():
            target_keys.add((details["category"], details["origin"]))

        # Build enum name maps for resource name construction
        category_enum = client.enums.ConversionActionCategoryEnum.ConversionActionCategory
        origin_enum = client.enums.ConversionOriginEnum.ConversionOrigin
        category_names = {v.number: v.name for v in category_enum.DESCRIPTOR.values}
        origin_names = {v.number: v.name for v in origin_enum.DESCRIPTOR.values}

        for key, goal in existing_goals.items():
            cat_name = category_names.get(goal.category, str(goal.category))
            origin_name = origin_names.get(goal.origin, str(goal.origin))
            # Skip unresolvable enum values (UNKNOWN/UNSPECIFIED)
            if cat_name in ("UNKNOWN", "UNSPECIFIED") or origin_name in ("UNKNOWN", "UNSPECIFIED"):
                continue
            operation = client.get_type("CampaignConversionGoalOperation")
            update_goal = operation.update
            update_goal.resource_name = (
                f"customers/{customer_id}/campaignConversionGoals/"
                f"{campaign_id}~{cat_name}~{origin_name}"
            )
            update_goal.campaign = f"customers/{customer_id}/campaigns/{campaign_id}"
            update_goal.category = goal.category
            update_goal.origin = goal.origin
            update_goal.biddable = key in target_keys
            operation.update_mask.paths.extend(["biddable"])
            operations.append(operation)

        if operations:
            conversion_goal_service.mutate_campaign_conversion_goals(
                customer_id=customer_id,
                operations=operations,
            )

        return {
            "campaign_id": campaign_id,
            "biddable_goals": [
                {
                    "conversion_action_id": aid,
                    "category": str(details["category"]),
                    "origin": str(details["origin"]),
                }
                for aid, details in action_details.items()
            ],
            "total_goals_updated": len(operations),
            "status": "configured",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_list_customer_conversion_goals(
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Lists all customer conversion goals for the account.

    Customer conversion goals control which conversion action categories
    are used for bidding (Smart Bidding optimization). Each goal is a
    category+origin pair (e.g. SUBMIT_LEAD_FORM~WEBSITE).

    A conversion action is used for bidding when BOTH:
    1. Its category+origin goal has biddable=true (this tool)
    2. The action itself has primary_for_goal=true (google_update_conversion_action)

    Args:
        customer_id: Google Ads customer ID.
        login_customer_id: Optional MCC account ID.

    Returns:
        list[dict]: Goals with category, origin, biddable status.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = """
            SELECT
                customer_conversion_goal.category,
                customer_conversion_goal.origin,
                customer_conversion_goal.biddable
            FROM customer_conversion_goal
        """

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id, query=query,
        )

        results = []
        for batch in response:
            for row in batch.results:
                goal = row.customer_conversion_goal
                cat = get_enum_name(client, "ConversionActionCategoryEnum", goal.category)
                orig = get_enum_name(client, "ConversionOriginEnum", goal.origin)
                results.append({
                    "category": cat,
                    "origin": orig,
                    "biddable": goal.biddable,
                    "resource_name": f"customers/{customer_id}/customerConversionGoals/{cat}~{orig}",
                })

        return results

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_update_customer_conversion_goal(
    category: str,
    origin: str,
    biddable: bool,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Updates a customer conversion goal's biddable status.

    This controls whether conversion actions in a category+origin pair
    are used for Smart Bidding. Use with google_update_conversion_action
    (include_in_conversions=true) to make specific actions primary.

    Common categories: SUBMIT_LEAD_FORM, PURCHASE, SIGNUP, CONTACT,
        PAGE_VIEW, ENGAGEMENT, PHONE_CALL_LEAD, DEFAULT
    Common origins: WEBSITE, APP, GOOGLE_HOSTED, CALL_FROM_ADS

    Args:
        category: Conversion action category (e.g. "SUBMIT_LEAD_FORM").
        origin: Conversion origin (e.g. "WEBSITE").
        biddable: Whether to use this goal for Smart Bidding.
        customer_id: Google Ads customer ID.
        login_customer_id: Optional MCC account ID.

    Returns:
        dict: Updated goal with category, origin, biddable, status.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        service = client.get_service("CustomerConversionGoalService")
        operation = client.get_type("CustomerConversionGoalOperation")
        goal = operation.update

        goal.resource_name = (
            f"customers/{customer_id}/customerConversionGoals/"
            f"{category}~{origin}"
        )
        goal.biddable = biddable
        operation.update_mask.paths.append("biddable")

        response = service.mutate_customer_conversion_goals(
            customer_id=customer_id,
            operations=[operation],
        )

        return {
            "resource_name": response.results[0].resource_name,
            "category": category,
            "origin": origin,
            "biddable": biddable,
            "status": "updated",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e
