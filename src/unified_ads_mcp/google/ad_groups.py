"""Ad Group management tools for Google Ads API.

This module provides MCP tools for managing Google Ads ad groups including
listing, creating, updating, and deleting ad groups within campaigns.
"""

from typing import Any, Optional

from google.ads.googleads.errors import GoogleAdsException
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import get_google_ads_client, clean_customer_id, format_error, get_default_customer_id, get_enum_name, get_enum_value, micros_to_currency, currency_to_micros


@mcp.tool()
def google_list_ad_groups(
    customer_id: Optional[str] = None,
    campaign_id: Optional[str] = None,
    status: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Lists ad groups for a Google Ads customer with performance metrics.

    Args:
        customer_id: The Google Ads customer ID (digits only, no dashes).
        campaign_id: Optional campaign ID to filter ad groups by campaign.
        status: Optional filter by status - ENABLED, PAUSED, or REMOVED.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        list[dict]: List of ad groups with:
            - id: Ad group ID
            - name: Ad group name
            - status: Ad group status
            - campaign_id: Parent campaign ID
            - campaign_name: Parent campaign name
            - cpc_bid: CPC bid in account currency
            - impressions: Total impressions
            - clicks: Total clicks
            - cost: Total cost in account currency
            - conversions: Total conversions

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = """
            SELECT
                ad_group.id,
                ad_group.name,
                ad_group.status,
                ad_group.cpc_bid_micros,
                ad_group.type,
                campaign.id,
                campaign.name,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions
            FROM ad_group
        """

        conditions = []
        if campaign_id:
            conditions.append(f"campaign.id = {campaign_id}")
        if status:
            conditions.append(f"ad_group.status = '{status.upper()}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY ad_group.id"

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        ad_groups = []
        for batch in response:
            for row in batch.results:
                ad_groups.append({
                    "id": str(row.ad_group.id),
                    "name": row.ad_group.name,
                    "status": get_enum_name(client, "AdGroupStatusEnum", row.ad_group.status),
                    "type": get_enum_name(client, "AdGroupTypeEnum", row.ad_group.type_),
                    "cpc_bid": micros_to_currency(row.ad_group.cpc_bid_micros),
                    "campaign_id": str(row.campaign.id),
                    "campaign_name": row.campaign.name,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost": micros_to_currency(row.metrics.cost_micros),
                    "conversions": row.metrics.conversions,
                })

        return ad_groups

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_get_ad_group(
    ad_group_id: str,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Gets detailed information about a specific ad group.

    Args:
        ad_group_id: The ad group ID to retrieve.
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Ad group details including:
            - id: Ad group ID
            - name: Ad group name
            - status: Ad group status
            - type: Ad group type
            - cpc_bid: CPC bid in account currency
            - cpm_bid: CPM bid in account currency
            - campaign_id: Parent campaign ID
            - campaign_name: Parent campaign name
            - impressions: Total impressions
            - clicks: Total clicks
            - cost: Total cost in account currency
            - conversions: Total conversions
            - average_cpc: Average CPC in account currency

    Raises:
        ToolError: If the ad group is not found or API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = f"""
            SELECT
                ad_group.id,
                ad_group.name,
                ad_group.status,
                ad_group.type,
                ad_group.cpc_bid_micros,
                ad_group.cpm_bid_micros,
                ad_group.effective_target_cpa_micros,
                ad_group.target_roas,
                campaign.id,
                campaign.name,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.average_cpc
            FROM ad_group
            WHERE ad_group.id = {ad_group_id}
        """

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        for batch in response:
            for row in batch.results:
                return {
                    "id": str(row.ad_group.id),
                    "name": row.ad_group.name,
                    "status": get_enum_name(client, "AdGroupStatusEnum", row.ad_group.status),
                    "type": get_enum_name(client, "AdGroupTypeEnum", row.ad_group.type_),
                    "cpc_bid": micros_to_currency(row.ad_group.cpc_bid_micros),
                    "cpm_bid": micros_to_currency(row.ad_group.cpm_bid_micros),
                    "effective_target_cpa": micros_to_currency(row.ad_group.effective_target_cpa_micros),
                    "target_roas": row.ad_group.target_roas,
                    "campaign_id": str(row.campaign.id),
                    "campaign_name": row.campaign.name,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost": micros_to_currency(row.metrics.cost_micros),
                    "conversions": row.metrics.conversions,
                    "average_cpc": micros_to_currency(row.metrics.average_cpc),
                }

        raise ToolError(f"Ad group {ad_group_id} not found")

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_create_ad_group(
    campaign_id: str,
    name: str,
    cpc_bid: float,
    customer_id: Optional[str] = None,
    status: str = "ENABLED",
    ad_group_type: str = "SEARCH_STANDARD",
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Creates a new ad group within a campaign.

    Args:
        campaign_id: The parent campaign ID.
        name: The ad group name.
        cpc_bid: Default CPC bid in account currency (e.g., 1.50 for $1.50).
        customer_id: The Google Ads customer ID. Uses default from config if not provided.
        status: Initial status - ENABLED (default) or PAUSED.
        ad_group_type: Ad group type. Options:
            - SEARCH_STANDARD: Standard Search ad group
            - DISPLAY_STANDARD: Standard Display ad group
            - SHOPPING_PRODUCT_ADS: Shopping product ads
            - VIDEO_TRUE_VIEW_IN_STREAM: TrueView in-stream video ads
            - VIDEO_BUMPER: Bumper video ads
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Created ad group details:
            - ad_group_id: The new ad group ID
            - ad_group_resource_name: Full resource name
            - status: Creation status

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        ad_group_service = client.get_service("AdGroupService")
        ad_group_operation = client.get_type("AdGroupOperation")
        ad_group = ad_group_operation.create

        ad_group.name = name
        ad_group.campaign = f"customers/{customer_id}/campaigns/{campaign_id}"
        ad_group.status = get_enum_value(client, "AdGroupStatusEnum", status)
        ad_group.type_ = get_enum_value(client, "AdGroupTypeEnum", ad_group_type)
        ad_group.cpc_bid_micros = currency_to_micros(cpc_bid)

        response = ad_group_service.mutate_ad_groups(
            customer_id=customer_id,
            operations=[ad_group_operation],
        )

        return {
            "ad_group_id": response.results[0].resource_name.split("/")[-1],
            "ad_group_resource_name": response.results[0].resource_name,
            "status": "created",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_update_ad_group(
    ad_group_id: str,
    customer_id: Optional[str] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    cpc_bid: Optional[float] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Updates an existing ad group.

    Args:
        ad_group_id: The ad group ID to update.
        customer_id: The Google Ads customer ID. Uses default from config if not provided.
        name: Optional new ad group name.
        status: Optional new status - ENABLED, PAUSED, or REMOVED.
        cpc_bid: Optional new CPC bid in account currency (e.g., 1.50 for $1.50).
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Updated ad group details:
            - ad_group_resource_name: Full resource name
            - updated_fields: List of fields that were updated
            - status: Update status

    Raises:
        ToolError: If no fields to update or API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        ad_group_service = client.get_service("AdGroupService")
        ad_group_operation = client.get_type("AdGroupOperation")
        ad_group = ad_group_operation.update
        ad_group.resource_name = f"customers/{customer_id}/adGroups/{ad_group_id}"

        field_mask = []

        if name is not None:
            ad_group.name = name
            field_mask.append("name")

        if status is not None:
            ad_group.status = get_enum_value(client, "AdGroupStatusEnum", status)
            field_mask.append("status")

        if cpc_bid is not None:
            ad_group.cpc_bid_micros = currency_to_micros(cpc_bid)
            field_mask.append("cpc_bid_micros")

        if not field_mask:
            raise ToolError("No fields to update. Provide at least one field.")

        ad_group_operation.update_mask.paths.extend(field_mask)

        response = ad_group_service.mutate_ad_groups(
            customer_id=customer_id,
            operations=[ad_group_operation],
        )

        return {
            "ad_group_resource_name": response.results[0].resource_name,
            "updated_fields": field_mask,
            "status": "updated",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_delete_ad_group(
    ad_group_id: str,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Removes an ad group.

    Note: This sets the ad group status to REMOVED. The ad group data
    is retained and can still be queried but cannot be reactivated.

    Args:
        ad_group_id: The ad group ID to remove.
        customer_id: The Google Ads customer ID. Uses default from config if not provided.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Removal status:
            - ad_group_resource_name: Full resource name
            - status: "removed"

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        ad_group_service = client.get_service("AdGroupService")
        ad_group_operation = client.get_type("AdGroupOperation")
        ad_group_operation.remove = f"customers/{customer_id}/adGroups/{ad_group_id}"

        response = ad_group_service.mutate_ad_groups(
            customer_id=customer_id,
            operations=[ad_group_operation],
        )

        return {
            "ad_group_resource_name": response.results[0].resource_name,
            "status": "removed",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e
