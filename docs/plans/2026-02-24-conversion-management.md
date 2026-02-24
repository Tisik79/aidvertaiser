# Conversion Management Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add comprehensive conversion management tools to both Google Ads and Meta Ads modules - covering conversion action CRUD, offline conversion uploads, server-side events (CAPI), custom conversions, pixel management, and campaign conversion goal configuration.

**Architecture:** Two new tool modules (`google/conversions.py` and `meta/conversions.py`) following the existing patterns exactly. Google tools are synchronous using `ConversionActionService` and `ConversionUploadService`. Meta tools are async using the Graph API endpoints for pixels, custom conversions, and the Conversions API (CAPI). Both modules register via `@mcp.tool()` decorators and are imported in `server.py` and their package `__init__.py`.

**Tech Stack:** Python 3.12+, FastMCP 2.14.1, google-ads SDK (ConversionActionService, ConversionUploadService), facebook-business SDK + httpx for Meta Graph API, pytest + pytest-asyncio for tests.

---

## Task 1: Google Ads - Conversion Actions Module

**Files:**
- Create: `src/unified_ads_mcp/google/conversions.py`
- Modify: `src/unified_ads_mcp/google/__init__.py`
- Modify: `src/unified_ads_mcp/server.py`
- Test: `tests/test_google_conversions.py`

### Step 1: Create `google/conversions.py` with conversion action CRUD tools

This module provides 6 tools:
- `google_list_conversion_actions` - list all conversion actions
- `google_get_conversion_action` - get details of a specific conversion action
- `google_create_conversion_action` - create a new conversion action
- `google_update_conversion_action` - update an existing conversion action
- `google_delete_conversion_action` - remove a conversion action
- `google_get_conversion_action_performance` - get conversion metrics by action

```python
"""Conversion management tools for Google Ads API.

This module provides MCP tools for managing conversion actions, uploading
offline conversions, and configuring campaign conversion goals.
"""

from typing import Any, Optional

from google.ads.googleads.errors import GoogleAdsException
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import (
    get_google_ads_client,
    format_error,
    resolve_customer_id,
    get_enum_name,
    get_enum_value,
    micros_to_currency,
    currency_to_micros,
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
            - category: Category (PURCHASE, LEAD, SIGNUP, etc.)
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
                    "type": get_enum_name(
                        client, "ConversionActionTypeEnum", ca.type_
                    ),
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
                    "origin": get_enum_name(
                        client, "ConversionOriginEnum", ca.origin
                    ),
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
                    "type": get_enum_name(
                        client, "ConversionActionTypeEnum", ca.type_
                    ),
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
                    "origin": get_enum_name(
                        client, "ConversionOriginEnum", ca.origin
                    ),
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
              LEAD, SIGNUP, SUBSCRIBE_PAID, PAGE_VIEW,
              CONTACT, SUBMIT_LEAD_FORM, BOOK_APPOINTMENT,
              REQUEST_QUOTE, GET_DIRECTIONS, DOWNLOAD,
              QUALIFIED_LEAD, CONVERTED_LEAD
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
        conversion_action.view_through_lookback_window_days = (
            view_through_lookback_days
        )

        # Attribution model
        conversion_action.attribution_model_settings.attribution_model = (
            get_enum_value(client, "AttributionModelEnum", attribution_model)
        )

        # Include in conversions metric
        conversion_action.include_in_conversions_metric = include_in_conversions

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
            conversion_action.include_in_conversions_metric = include_in_conversions
            field_mask.append("include_in_conversions_metric")

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
            - conversion_action_id, name, type, category
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
                conversion_action.id,
                conversion_action.name,
                conversion_action.type,
                conversion_action.category,
                conversion_action.status,
                metrics.all_conversions,
                metrics.all_conversions_value,
                metrics.conversions,
                metrics.conversions_value,
                metrics.view_through_conversions
            FROM conversion_action
            WHERE segments.date DURING {date_range}
        """

        if conversion_action_id:
            query += f" AND conversion_action.id = {conversion_action_id}"

        query += " ORDER BY metrics.all_conversions DESC"

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        results = []
        for batch in response:
            for row in batch.results:
                results.append(
                    {
                        "conversion_action_id": str(row.conversion_action.id),
                        "name": row.conversion_action.name,
                        "type": get_enum_name(
                            client,
                            "ConversionActionTypeEnum",
                            row.conversion_action.type_,
                        ),
                        "category": get_enum_name(
                            client,
                            "ConversionActionCategoryEnum",
                            row.conversion_action.category,
                        ),
                        "status": get_enum_name(
                            client,
                            "ConversionActionStatusEnum",
                            row.conversion_action.status,
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
```

### Step 2: Add offline conversion upload tool to same file

Append this to `google/conversions.py`:

```python
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
                k in identifiers
                for k in ["first_name", "last_name", "street_address"]
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
    conversion_action_ids: list[str],
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
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        ga_service = client.get_service("GoogleAdsService")
        conversion_goal_service = client.get_service(
            "CampaignConversionGoalService"
        )
        conversion_action_service = client.get_service("ConversionActionService")

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

        response = ga_service.search_stream(
            customer_id=customer_id, query=query
        )

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

        for key, goal in existing_goals.items():
            operation = client.get_type("CampaignConversionGoalOperation")
            update_goal = operation.update
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
```

### Step 3: Register the module in `server.py` and `__init__.py`

**Modify `src/unified_ads_mcp/server.py`** - add after the existing google imports:
```python
from .google import conversions as google_conversions  # noqa: E402, F401
```

**Modify `src/unified_ads_mcp/google/__init__.py`** - add import and __all__ entry:
```python
from unified_ads_mcp.google import conversions
```
Add `"conversions"` to the `__all__` list.

### Step 4: Run lint and tests

```bash
cd ~/Work/Programming/adsmcp
uv run ruff check src/unified_ads_mcp/google/conversions.py
uv run ruff format src/unified_ads_mcp/google/conversions.py
uv run pytest tests/ -v --timeout=60
```

### Step 5: Commit

```bash
git add src/unified_ads_mcp/google/conversions.py src/unified_ads_mcp/google/__init__.py src/unified_ads_mcp/server.py
git commit -m "feat: add Google Ads conversion management tools

Add 9 tools: list/get/create/update/delete conversion actions,
conversion action performance, offline conversion upload,
enhanced conversions upload, campaign conversion goal setting."
```

---

## Task 2: Meta Ads - Conversions Module (Pixels, Custom Conversions, CAPI)

**Files:**
- Create: `src/unified_ads_mcp/meta/conversions.py`
- Modify: `src/unified_ads_mcp/meta/__init__.py`
- Modify: `src/unified_ads_mcp/server.py`
- Test: `tests/test_meta_conversions.py`

### Step 1: Create `meta/conversions.py` with pixel management, custom conversions, and CAPI

```python
"""Meta Ads Conversion Management Tools.

This module provides MCP tools for managing Meta Ads conversions including:
- Pixel management (list, get details)
- Custom conversions (CRUD)
- Conversions API (CAPI) - server-side event sending
- Offline conversion management
"""

import json
import time
import hashlib
from typing import Any, Optional, List, Dict

from ..server import mcp
from .client import (
    make_api_request,
    meta_api_tool,
    ensure_account_prefix,
    resolve_account_id,
)


def _hash_user_data(value: str) -> str:
    """SHA-256 hash user data for Meta CAPI (normalize + lowercase + hash)."""
    return hashlib.sha256(value.strip().lower().encode("utf-8")).hexdigest()


# ── Pixel Management ──


@mcp.tool()
@meta_api_tool
async def meta_list_pixels(
    account_id: Optional[str] = None,
    access_token: Optional[str] = None,
) -> dict:
    """Lists all Meta Pixels for an ad account.

    A Meta Pixel is a piece of JavaScript code that tracks visitor
    activity on your website. Each account can have multiple pixels.

    Args:
        account_id: Meta Ads account ID. Uses default if not provided.
        access_token: Meta API access token.

    Returns:
        Dictionary with pixel data including id, name, code,
        last_fired_time, and is_unavailable status.
    """
    account_id = resolve_account_id(account_id)
    if not account_id:
        return {"error": {"message": "account_id is required"}}
    account_id = ensure_account_prefix(account_id)

    endpoint = f"{account_id}/adspixels"
    params = {
        "fields": "id,name,code,last_fired_time,is_unavailable,creation_time,owner_ad_account,data_use_setting,is_created_by_business",
    }
    return await make_api_request(endpoint, access_token, params)


@mcp.tool()
@meta_api_tool
async def meta_get_pixel(
    pixel_id: str,
    access_token: Optional[str] = None,
) -> dict:
    """Gets detailed information about a specific Meta Pixel.

    Args:
        pixel_id: The Meta Pixel ID.
        access_token: Meta API access token.

    Returns:
        Dictionary with pixel details and recent event statistics.
    """
    endpoint = f"{pixel_id}"
    params = {
        "fields": "id,name,code,last_fired_time,is_unavailable,creation_time,owner_ad_account,data_use_setting",
    }
    return await make_api_request(endpoint, access_token, params)


@mcp.tool()
@meta_api_tool
async def meta_get_pixel_stats(
    pixel_id: str,
    access_token: Optional[str] = None,
    aggregation: str = "event",
) -> dict:
    """Gets event statistics for a Meta Pixel.

    Shows which events the pixel is receiving and their counts,
    useful for verifying tracking is working correctly.

    Args:
        pixel_id: The Meta Pixel ID.
        access_token: Meta API access token.
        aggregation: How to aggregate stats. Options:
            - "event": Group by event name (default)
            - "domain": Group by domain
            - "device_type": Group by device

    Returns:
        Dictionary with event statistics including counts per event type.
    """
    endpoint = f"{pixel_id}/stats"
    params = {"aggregation": aggregation}
    return await make_api_request(endpoint, access_token, params)


# ── Custom Conversions ──


@mcp.tool()
@meta_api_tool
async def meta_list_custom_conversions(
    account_id: Optional[str] = None,
    access_token: Optional[str] = None,
) -> dict:
    """Lists all custom conversions for an ad account.

    Custom conversions let you create conversion rules based on
    URL patterns or event parameters without modifying pixel code.

    Args:
        account_id: Meta Ads account ID. Uses default if not provided.
        access_token: Meta API access token.

    Returns:
        Dictionary with custom conversion data including rules,
        pixel associations, and last_fired_time.
    """
    account_id = resolve_account_id(account_id)
    if not account_id:
        return {"error": {"message": "account_id is required"}}
    account_id = ensure_account_prefix(account_id)

    endpoint = f"{account_id}/customconversions"
    params = {
        "fields": "id,name,description,pixel,rule,default_conversion_value,custom_event_type,event_source_type,first_fired_time,last_fired_time,is_archived,retention_days,creation_time",
    }
    return await make_api_request(endpoint, access_token, params)


@mcp.tool()
@meta_api_tool
async def meta_get_custom_conversion(
    custom_conversion_id: str,
    access_token: Optional[str] = None,
) -> dict:
    """Gets detailed information about a specific custom conversion.

    Args:
        custom_conversion_id: The custom conversion ID.
        access_token: Meta API access token.

    Returns:
        Dictionary with custom conversion details including rule,
        pixel info, and activity data.
    """
    endpoint = f"{custom_conversion_id}"
    params = {
        "fields": "id,name,description,pixel,rule,default_conversion_value,custom_event_type,event_source_type,first_fired_time,last_fired_time,is_archived,retention_days,creation_time",
    }
    return await make_api_request(endpoint, access_token, params)


@mcp.tool()
@meta_api_tool
async def meta_create_custom_conversion(
    name: str,
    pixel_id: str,
    rule: str,
    account_id: Optional[str] = None,
    access_token: Optional[str] = None,
    custom_event_type: str = "OTHER",
    default_conversion_value: Optional[float] = None,
    description: Optional[str] = None,
) -> dict:
    """Creates a new custom conversion rule.

    Custom conversions let you track specific actions without modifying
    your pixel code. Define rules based on URLs or event parameters.

    Args:
        name: Custom conversion name (e.g., "Thank You Page Visit").
        pixel_id: Meta Pixel ID to associate with.
        rule: JSON rule string defining when conversion fires. Examples:
            - URL contains: '{"and":[{"url":{"i_contains":"thank-you"}}]}'
            - URL equals: '{"and":[{"url":{"eq":"https://example.com/thanks"}}]}'
            - Event + URL: '{"and":[{"event":{"eq":"Purchase"}},{"url":{"i_contains":"checkout"}}]}'
        account_id: Meta Ads account ID. Uses default if not provided.
        access_token: Meta API access token.
        custom_event_type: Event type. Options:
            - ADD_PAYMENT_INFO, ADD_TO_CART, ADD_TO_WISHLIST,
              COMPLETE_REGISTRATION, CONTACT, CUSTOMIZE_PRODUCT,
              DONATE, FIND_LOCATION, INITIATED_CHECKOUT, LEAD,
              LISTING_INTERACTION, OTHER, PURCHASE, SCHEDULE,
              SEARCH, START_TRIAL, SUBMIT_APPLICATION, SUBSCRIBE
        default_conversion_value: Default monetary value per conversion.
        description: Optional description.

    Returns:
        Dictionary with created custom conversion ID.
    """
    account_id = resolve_account_id(account_id)
    if not account_id:
        return {"error": {"message": "account_id is required"}}
    account_id = ensure_account_prefix(account_id)

    endpoint = f"{account_id}/customconversions"
    params = {
        "name": name,
        "pixel": pixel_id,
        "rule": rule,
        "custom_event_type": custom_event_type,
    }

    if default_conversion_value is not None:
        params["default_conversion_value"] = str(default_conversion_value)
    if description:
        params["description"] = description

    return await make_api_request(endpoint, access_token, params, method="POST")


@mcp.tool()
@meta_api_tool
async def meta_update_custom_conversion(
    custom_conversion_id: str,
    access_token: Optional[str] = None,
    name: Optional[str] = None,
    default_conversion_value: Optional[float] = None,
    description: Optional[str] = None,
) -> dict:
    """Updates an existing custom conversion.

    Note: The rule and pixel_id cannot be changed after creation.

    Args:
        custom_conversion_id: The custom conversion ID.
        access_token: Meta API access token.
        name: New name.
        default_conversion_value: New default value.
        description: New description.

    Returns:
        Dictionary with success status.
    """
    params = {}
    if name is not None:
        params["name"] = name
    if default_conversion_value is not None:
        params["default_conversion_value"] = str(default_conversion_value)
    if description is not None:
        params["description"] = description

    if not params:
        return {"error": {"message": "No update parameters provided"}}

    endpoint = f"{custom_conversion_id}"
    return await make_api_request(endpoint, access_token, params, method="POST")


@mcp.tool()
@meta_api_tool
async def meta_delete_custom_conversion(
    custom_conversion_id: str,
    access_token: Optional[str] = None,
) -> dict:
    """Deletes (archives) a custom conversion.

    Args:
        custom_conversion_id: The custom conversion ID to delete.
        access_token: Meta API access token.

    Returns:
        Dictionary with success status.
    """
    endpoint = f"{custom_conversion_id}"
    return await make_api_request(endpoint, access_token, method="DELETE")


# ── Conversions API (CAPI) - Server-Side Events ──


@mcp.tool()
@meta_api_tool
async def meta_send_conversion_event(
    pixel_id: str,
    event_name: str,
    access_token: Optional[str] = None,
    event_time: Optional[int] = None,
    event_source_url: Optional[str] = None,
    action_source: str = "website",
    user_data: Optional[Dict[str, str]] = None,
    custom_data: Optional[Dict[str, Any]] = None,
    event_id: Optional[str] = None,
    opt_out: bool = False,
) -> dict:
    """Sends a server-side conversion event via the Conversions API (CAPI).

    The Conversions API lets you send conversion events directly from
    your server, providing more reliable tracking than browser-based
    pixels (not affected by ad blockers or cookie restrictions).

    Best practice: Send events via both Pixel AND CAPI with matching
    event_id for deduplication.

    Args:
        pixel_id: Meta Pixel ID to send the event to.
        event_name: Standard or custom event name. Standard events:
            - AddPaymentInfo, AddToCart, AddToWishlist,
              CompleteRegistration, Contact, CustomizeProduct,
              Donate, FindLocation, InitiateCheckout, Lead,
              PageView, Purchase, Schedule, Search,
              StartTrial, SubmitApplication, Subscribe, ViewContent
        access_token: Meta API access token.
        event_time: Unix timestamp of the event. Defaults to now.
            Events can be sent up to 7 days after they occurred.
        event_source_url: URL where the event happened.
        action_source: Where the event originated. Options:
            - website (default), app, phone_call, chat,
              physical_store, system_generated, email, other
        user_data: User identification data for matching (auto-hashed):
            - em: Email address
            - ph: Phone number (E.164 format)
            - fn: First name
            - ln: Last name
            - ct: City
            - st: State/province (2-letter code)
            - zp: Zip/postal code
            - country: Country (2-letter ISO code)
            - external_id: Your unique user ID
            - client_ip_address: User's IP address (NOT hashed)
            - client_user_agent: User's browser user agent (NOT hashed)
            - fbc: Facebook click ID cookie (_fbc)
            - fbp: Facebook browser ID cookie (_fbp)
        custom_data: Event-specific data:
            - value: Monetary value (required for Purchase)
            - currency: Currency code (required for Purchase)
            - content_name: Product/content name
            - content_ids: List of product IDs
            - content_type: "product" or "product_group"
            - contents: List of product objects
            - num_items: Number of items
            - order_id: Unique order/transaction ID
            - search_string: Search query
            - status: Registration/subscription status
        event_id: Unique event ID for deduplication with browser pixel.
        opt_out: If True, event is used only for attribution, not targeting.

    Returns:
        Dictionary with events_received count and fbtrace_id for debugging.

    Example:
        >>> await meta_send_conversion_event(
        ...     pixel_id="123456789",
        ...     event_name="Purchase",
        ...     user_data={"em": "user@example.com", "ph": "+420123456789"},
        ...     custom_data={"value": 1500.0, "currency": "CZK", "order_id": "ORD-001"}
        ... )
    """
    if not event_time:
        event_time = int(time.time())

    # Build user_data with hashing
    hashed_user_data = {}
    if user_data:
        # Fields that should be hashed
        hash_fields = {"em", "ph", "fn", "ln", "ct", "st", "zp", "country", "external_id"}
        # Fields that should NOT be hashed
        no_hash_fields = {"client_ip_address", "client_user_agent", "fbc", "fbp"}

        for key, value in user_data.items():
            if key in hash_fields and value:
                hashed_user_data[key] = _hash_user_data(value)
            elif key in no_hash_fields and value:
                hashed_user_data[key] = value
            elif value:
                hashed_user_data[key] = value

    event = {
        "event_name": event_name,
        "event_time": event_time,
        "action_source": action_source,
        "user_data": hashed_user_data,
    }

    if event_source_url:
        event["event_source_url"] = event_source_url
    if custom_data:
        event["custom_data"] = custom_data
    if event_id:
        event["event_id"] = event_id
    if opt_out:
        event["opt_out"] = True

    endpoint = f"{pixel_id}/events"
    params = {
        "data": json.dumps([event]),
    }

    return await make_api_request(endpoint, access_token, params, method="POST")


@mcp.tool()
@meta_api_tool
async def meta_send_conversion_events_batch(
    pixel_id: str,
    events: List[Dict[str, Any]],
    access_token: Optional[str] = None,
) -> dict:
    """Sends multiple conversion events in a single batch via CAPI.

    More efficient than sending events one by one. Supports up to
    1000 events per batch. Each event follows the same format as
    meta_send_conversion_event.

    Args:
        pixel_id: Meta Pixel ID.
        events: List of event dictionaries. Each must contain:
            - event_name: Standard or custom event name
            - event_time: Unix timestamp (optional, defaults to now)
            - action_source: Where event originated (default: "website")
            - user_data: Dict of user identifiers (auto-hashed)
            - custom_data: Optional event-specific data
            - event_id: Optional deduplication ID
        access_token: Meta API access token.

    Returns:
        Dictionary with events_received count and fbtrace_id.
    """
    now = int(time.time())
    processed_events = []

    for event in events:
        processed = {
            "event_name": event["event_name"],
            "event_time": event.get("event_time", now),
            "action_source": event.get("action_source", "website"),
        }

        # Hash user data
        user_data = event.get("user_data", {})
        hashed = {}
        hash_fields = {"em", "ph", "fn", "ln", "ct", "st", "zp", "country", "external_id"}
        no_hash_fields = {"client_ip_address", "client_user_agent", "fbc", "fbp"}

        for key, value in user_data.items():
            if key in hash_fields and value:
                hashed[key] = _hash_user_data(value)
            elif key in no_hash_fields and value:
                hashed[key] = value
            elif value:
                hashed[key] = value

        processed["user_data"] = hashed

        if "event_source_url" in event:
            processed["event_source_url"] = event["event_source_url"]
        if "custom_data" in event:
            processed["custom_data"] = event["custom_data"]
        if "event_id" in event:
            processed["event_id"] = event["event_id"]

        processed_events.append(processed)

    endpoint = f"{pixel_id}/events"
    params = {
        "data": json.dumps(processed_events),
    }

    return await make_api_request(endpoint, access_token, params, method="POST")


# ── Offline Conversions ──


@mcp.tool()
@meta_api_tool
async def meta_list_offline_conversion_sets(
    account_id: Optional[str] = None,
    access_token: Optional[str] = None,
) -> dict:
    """Lists offline conversion data sets for an ad account.

    Offline conversion data sets are used to upload offline events
    (store visits, phone sales, CRM data) for attribution.

    Args:
        account_id: Meta Ads account ID. Uses default if not provided.
        access_token: Meta API access token.

    Returns:
        Dictionary with offline conversion set data.
    """
    account_id = resolve_account_id(account_id)
    if not account_id:
        return {"error": {"message": "account_id is required"}}
    account_id = ensure_account_prefix(account_id)

    endpoint = f"{account_id}/offline_conversion_data_sets"
    params = {
        "fields": "id,name,description,creation_time,last_upload_app,last_upload_app_changed_time,event_stats,usage,is_restricted_use,auto_assign_to_new_accounts_only",
    }
    return await make_api_request(endpoint, access_token, params)


@mcp.tool()
@meta_api_tool
async def meta_create_offline_conversion_set(
    name: str,
    account_id: Optional[str] = None,
    access_token: Optional[str] = None,
    description: Optional[str] = None,
    auto_assign_to_new_accounts_only: bool = False,
) -> dict:
    """Creates an offline conversion data set.

    Use this to create a container for uploading offline conversion
    events (CRM data, phone sales, in-store purchases).

    Args:
        name: Name for the offline conversion set.
        account_id: Meta Ads account ID. Uses default if not provided.
        access_token: Meta API access token.
        description: Optional description.
        auto_assign_to_new_accounts_only: If True, only auto-assign
            to newly created ad accounts.

    Returns:
        Dictionary with created offline conversion set ID.
    """
    account_id = resolve_account_id(account_id)
    if not account_id:
        return {"error": {"message": "account_id is required"}}
    account_id = ensure_account_prefix(account_id)

    endpoint = f"{account_id}/offline_conversion_data_sets"
    params = {
        "name": name,
        "auto_assign_to_new_accounts_only": str(auto_assign_to_new_accounts_only).lower(),
    }
    if description:
        params["description"] = description

    return await make_api_request(endpoint, access_token, params, method="POST")


@mcp.tool()
@meta_api_tool
async def meta_upload_offline_conversions(
    offline_set_id: str,
    events: List[Dict[str, Any]],
    access_token: Optional[str] = None,
) -> dict:
    """Uploads offline conversion events to an offline conversion set.

    Use this to push CRM data (leads that became customers, phone
    call outcomes, in-store purchases) back to Meta for attribution.

    Args:
        offline_set_id: The offline conversion data set ID.
        events: List of offline event records. Each must contain:
            - match_keys: Dict of user identifiers for matching:
                - email: Email address (auto-hashed)
                - phone: Phone number (auto-hashed)
                - fn: First name (auto-hashed)
                - ln: Last name (auto-hashed)
                - extern_id: Your unique customer ID
                - lead_id: Meta lead ad ID (if from lead form)
            - event_name: Event type (e.g., "Purchase", "Lead")
            - event_time: Unix timestamp of the event
            - value: Monetary value
            - currency: Currency code (e.g., "CZK")
            - order_id: Optional unique transaction ID
            - custom_data: Optional additional data dict
        access_token: Meta API access token.

    Returns:
        Dictionary with upload status and any errors.

    Example:
        >>> await meta_upload_offline_conversions(
        ...     offline_set_id="123456789",
        ...     events=[{
        ...         "match_keys": {"email": "customer@example.com"},
        ...         "event_name": "Purchase",
        ...         "event_time": 1706000000,
        ...         "value": 5000,
        ...         "currency": "CZK"
        ...     }]
        ... )
    """
    processed_events = []

    for event in events:
        processed = {
            "event_name": event["event_name"],
            "event_time": event["event_time"],
        }

        # Hash match keys
        match_keys = event.get("match_keys", {})
        hashed_keys = {}
        hash_fields = {"email", "phone", "fn", "ln"}

        for key, value in match_keys.items():
            if key in hash_fields and value:
                hashed_keys[key] = _hash_user_data(value)
            elif value:
                hashed_keys[key] = value

        processed["match_keys"] = hashed_keys

        if "value" in event:
            processed["value"] = event["value"]
        if "currency" in event:
            processed["currency"] = event["currency"]
        if "order_id" in event:
            processed["order_id"] = event["order_id"]
        if "custom_data" in event:
            processed["custom_data"] = event["custom_data"]

        processed_events.append(processed)

    endpoint = f"{offline_set_id}/events"
    params = {
        "upload_tag": f"mcp_upload_{int(time.time())}",
        "data": json.dumps(processed_events),
    }

    return await make_api_request(endpoint, access_token, params, method="POST")
```

### Step 2: Register the module

**Modify `src/unified_ads_mcp/server.py`** - add after existing meta imports:
```python
from .meta import conversions as meta_conversions  # noqa: E402, F401
```

**Modify `src/unified_ads_mcp/meta/__init__.py`** - add import and __all__ entry:
```python
from unified_ads_mcp.meta import conversions
```
Add `"conversions"` to the `__all__` list.

### Step 3: Run lint and tests

```bash
cd ~/Work/Programming/adsmcp
uv run ruff check src/unified_ads_mcp/meta/conversions.py
uv run ruff format src/unified_ads_mcp/meta/conversions.py
uv run pytest tests/ -v --timeout=60
```

### Step 4: Commit

```bash
git add src/unified_ads_mcp/meta/conversions.py src/unified_ads_mcp/meta/__init__.py src/unified_ads_mcp/server.py
git commit -m "feat: add Meta Ads conversion management tools

Add 13 tools: pixel list/get/stats, custom conversion CRUD,
CAPI single/batch event sending, offline conversion set CRUD
and event upload."
```

---

## Task 3: Integration Tests

**Files:**
- Create: `tests/test_google_conversions.py`
- Create: `tests/test_meta_conversions.py`

### Step 1: Create Google conversion tests

```python
"""Tests for Google Ads conversion management tools.

Integration tests using real API credentials.
"""

import pytest

from unified_ads_mcp.google.conversions import (
    google_list_conversion_actions as _list,
    google_get_conversion_action as _get,
    google_create_conversion_action as _create,
    google_update_conversion_action as _update,
    google_delete_conversion_action as _delete,
    google_get_conversion_action_performance as _perf,
)

# Unwrap FunctionTool objects
list_conversion_actions = _list.fn
get_conversion_action = _get.fn
create_conversion_action = _create.fn
update_conversion_action = _update.fn
delete_conversion_action = _delete.fn
get_conversion_action_performance = _perf.fn


class TestGoogleConversionActions:
    """Test Google Ads conversion action tools."""

    def test_list_conversion_actions(self):
        """List all conversion actions for the default account."""
        result = list_conversion_actions()
        assert isinstance(result, list)
        print(f"\nFound {len(result)} conversion actions")
        for action in result[:5]:
            print(f"  - {action['name']} ({action['type']}, {action['status']})")

    def test_list_conversion_actions_enabled_only(self):
        """List only enabled conversion actions."""
        result = list_conversion_actions(status="ENABLED")
        assert isinstance(result, list)
        for action in result:
            assert action["status"] == "ENABLED"

    def test_get_conversion_action(self):
        """Get details of a specific conversion action."""
        actions = list_conversion_actions()
        if not actions:
            pytest.skip("No conversion actions found")

        action_id = actions[0]["id"]
        result = get_conversion_action(conversion_action_id=action_id)
        assert result["id"] == action_id
        assert "name" in result
        assert "type" in result

    def test_conversion_action_performance(self):
        """Get performance metrics by conversion action."""
        result = get_conversion_action_performance(date_range="LAST_30_DAYS")
        assert isinstance(result, list)
        print(f"\nConversion action performance ({len(result)} actions with data):")
        for action in result[:5]:
            print(
                f"  - {action['name']}: {action['all_conversions']} conversions"
            )

    def test_create_update_delete_conversion_action(self):
        """Full lifecycle: create, update, delete a conversion action."""
        # Create
        result = create_conversion_action(
            name="MCP Test Conversion - DELETE ME",
            type="WEBPAGE",
            category="LEAD",
            counting_type="ONE_PER_CLICK",
            default_value=100.0,
            default_currency="CZK",
        )
        assert result["status"] == "created"
        action_id = result["id"]
        print(f"\nCreated conversion action: {action_id}")

        # Update
        update_result = update_conversion_action(
            conversion_action_id=action_id,
            name="MCP Test Conversion UPDATED - DELETE ME",
            default_value=200.0,
        )
        assert update_result["status"] == "updated"

        # Delete
        delete_result = delete_conversion_action(
            conversion_action_id=action_id,
        )
        assert delete_result["status"] == "removed"
        print(f"  Deleted conversion action: {action_id}")
```

### Step 2: Create Meta conversion tests

```python
"""Tests for Meta Ads conversion management tools.

Integration tests using real API credentials.
"""

import asyncio
import time
import pytest

from unified_ads_mcp.meta.conversions import (
    meta_list_pixels as _list_pixels,
    meta_get_pixel as _get_pixel,
    meta_get_pixel_stats as _pixel_stats,
    meta_list_custom_conversions as _list_cc,
    meta_get_custom_conversion as _get_cc,
    meta_create_custom_conversion as _create_cc,
    meta_update_custom_conversion as _update_cc,
    meta_delete_custom_conversion as _delete_cc,
    meta_send_conversion_event as _send_event,
    meta_list_offline_conversion_sets as _list_ocs,
)

# Unwrap FunctionTool objects
list_pixels = _list_pixels.fn
get_pixel = _get_pixel.fn
get_pixel_stats = _pixel_stats.fn
list_custom_conversions = _list_cc.fn
get_custom_conversion = _get_cc.fn
create_custom_conversion = _create_cc.fn
update_custom_conversion = _update_cc.fn
delete_custom_conversion = _delete_cc.fn
send_conversion_event = _send_event.fn
list_offline_conversion_sets = _list_ocs.fn


@pytest.fixture(scope="module")
def event_loop():
    """Create an event loop for the test module."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


class TestMetaPixels:
    """Test Meta Pixel management tools."""

    @pytest.mark.asyncio
    async def test_list_pixels(self, meta_access_token, meta_account_id):
        """List all pixels for the account."""
        result = await list_pixels(
            account_id=meta_account_id, access_token=meta_access_token
        )
        assert "error" not in result
        assert "data" in result
        print(f"\nFound {len(result['data'])} pixels")
        for pixel in result["data"]:
            print(f"  - {pixel.get('name')} (ID: {pixel['id']})")

    @pytest.mark.asyncio
    async def test_get_pixel(self, meta_access_token, meta_account_id):
        """Get details of a specific pixel."""
        pixels = await list_pixels(
            account_id=meta_account_id, access_token=meta_access_token
        )
        if not pixels.get("data"):
            pytest.skip("No pixels found")

        pixel_id = pixels["data"][0]["id"]
        result = await get_pixel(pixel_id=pixel_id, access_token=meta_access_token)
        assert "error" not in result
        assert result["id"] == pixel_id

    @pytest.mark.asyncio
    async def test_get_pixel_stats(self, meta_access_token, meta_account_id):
        """Get pixel event statistics."""
        pixels = await list_pixels(
            account_id=meta_account_id, access_token=meta_access_token
        )
        if not pixels.get("data"):
            pytest.skip("No pixels found")

        pixel_id = pixels["data"][0]["id"]
        result = await get_pixel_stats(
            pixel_id=pixel_id, access_token=meta_access_token
        )
        assert "error" not in result
        print(f"\nPixel {pixel_id} stats: {result}")


class TestMetaCustomConversions:
    """Test Meta custom conversion management tools."""

    @pytest.mark.asyncio
    async def test_list_custom_conversions(self, meta_access_token, meta_account_id):
        """List all custom conversions."""
        result = await list_custom_conversions(
            account_id=meta_account_id, access_token=meta_access_token
        )
        assert "error" not in result
        data = result.get("data", [])
        print(f"\nFound {len(data)} custom conversions")

    @pytest.mark.asyncio
    async def test_create_update_delete_custom_conversion(
        self, meta_access_token, meta_account_id
    ):
        """Full lifecycle: create, update, delete a custom conversion."""
        # First get a pixel ID
        pixels = await list_pixels(
            account_id=meta_account_id, access_token=meta_access_token
        )
        if not pixels.get("data"):
            pytest.skip("No pixels found for custom conversion test")

        pixel_id = pixels["data"][0]["id"]

        # Create
        result = await create_custom_conversion(
            name="MCP Test Custom Conv - DELETE ME",
            pixel_id=pixel_id,
            rule='{"and":[{"url":{"i_contains":"mcp-test-page-delete-me"}}]}',
            custom_event_type="OTHER",
            default_conversion_value=100.0,
            account_id=meta_account_id,
            access_token=meta_access_token,
        )
        assert "error" not in result
        cc_id = result.get("id")
        assert cc_id
        print(f"\nCreated custom conversion: {cc_id}")

        # Update
        update_result = await update_custom_conversion(
            custom_conversion_id=cc_id,
            name="MCP Test Custom Conv UPDATED - DELETE ME",
            access_token=meta_access_token,
        )
        assert "error" not in update_result

        # Delete
        delete_result = await delete_custom_conversion(
            custom_conversion_id=cc_id,
            access_token=meta_access_token,
        )
        assert "error" not in delete_result
        print(f"  Deleted custom conversion: {cc_id}")


class TestMetaCAPI:
    """Test Meta Conversions API (CAPI) tools."""

    @pytest.mark.asyncio
    async def test_send_conversion_event(self, meta_access_token, meta_account_id):
        """Send a test conversion event via CAPI."""
        # Get pixel ID
        pixels = await list_pixels(
            account_id=meta_account_id, access_token=meta_access_token
        )
        if not pixels.get("data"):
            pytest.skip("No pixels found for CAPI test")

        pixel_id = pixels["data"][0]["id"]

        result = await send_conversion_event(
            pixel_id=pixel_id,
            event_name="Lead",
            access_token=meta_access_token,
            event_source_url="https://test.example.com/mcp-test",
            user_data={
                "em": "mcp-test@example.com",
                "fn": "Test",
                "ln": "User",
                "country": "CZ",
            },
            custom_data={
                "value": 100.0,
                "currency": "CZK",
            },
            event_id=f"mcp_test_{int(time.time())}",
        )
        assert "error" not in result
        print(f"\nCAPI event sent: {result}")


class TestMetaOfflineConversions:
    """Test Meta offline conversion tools."""

    @pytest.mark.asyncio
    async def test_list_offline_conversion_sets(
        self, meta_access_token, meta_account_id
    ):
        """List offline conversion sets."""
        result = await list_offline_conversion_sets(
            account_id=meta_account_id, access_token=meta_access_token
        )
        assert "error" not in result
        data = result.get("data", [])
        print(f"\nFound {len(data)} offline conversion sets")
```

### Step 3: Run all tests

```bash
cd ~/Work/Programming/adsmcp
uv run pytest tests/ -v --timeout=60 -s
```

### Step 4: Commit tests

```bash
git add tests/test_google_conversions.py tests/test_meta_conversions.py
git commit -m "test: add integration tests for conversion management tools"
```

---

## Task 4: Final Verification and MCP Test

### Step 1: Run full lint check

```bash
cd ~/Work/Programming/adsmcp
uv run ruff check .
uv run ruff format --check .
```

### Step 2: Run full test suite

```bash
uv run pytest tests/ -v --timeout=60
```

### Step 3: Test MCP tool listing (should show new tools)

```bash
cd ~/Work/Programming/adsmcp
(echo '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'; echo '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'; echo '{"jsonrpc":"2.0","method":"tools/list","id":2,"params":{}}'; sleep 5) | ONLY_DEFAULT_ACCOUNT=1 GOOGLE_ADS_CREDENTIALS=~/google-ads.yaml META_ADS_CREDENTIALS=~/meta-ads.yaml uv run python -m unified_ads_mcp 2>/dev/null | python3 -c "import json,sys; [print(t['name']) for line in sys.stdin if (d:=json.loads(line)).get('id')==2 for t in d['result']['tools'] if 'conver' in t['name'].lower() or 'pixel' in t['name'].lower() or 'offline' in t['name'].lower() or 'capi' in t['name'].lower()]"
```

Expected new tools (22 total):
- `google_list_conversion_actions`
- `google_get_conversion_action`
- `google_create_conversion_action`
- `google_update_conversion_action`
- `google_delete_conversion_action`
- `google_get_conversion_action_performance`
- `google_upload_offline_conversions`
- `google_upload_enhanced_conversions`
- `google_set_campaign_conversion_goal`
- `meta_list_pixels`
- `meta_get_pixel`
- `meta_get_pixel_stats`
- `meta_list_custom_conversions`
- `meta_get_custom_conversion`
- `meta_create_custom_conversion`
- `meta_update_custom_conversion`
- `meta_delete_custom_conversion`
- `meta_send_conversion_event`
- `meta_send_conversion_events_batch`
- `meta_list_offline_conversion_sets`
- `meta_create_offline_conversion_set`
- `meta_upload_offline_conversions`

### Step 4: Final commit

```bash
git add -A
git commit -m "docs: add conversion management implementation plan"
```

---

## Summary

| Platform | Module | Tools Added |
|----------|--------|-------------|
| **Google Ads** | `google/conversions.py` | 9 tools: conversion action CRUD + performance, offline upload, enhanced conversions, campaign goals |
| **Meta Ads** | `meta/conversions.py` | 13 tools: pixel mgmt (3), custom conversions (5), CAPI events (2), offline conversions (3) |
| **Tests** | `test_google_conversions.py`, `test_meta_conversions.py` | Full integration test coverage |
| **Total** | | **22 new tools** |
