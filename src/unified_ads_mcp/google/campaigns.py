"""Campaign management tools for Google Ads API.

This module provides MCP tools for managing Google Ads campaigns including
listing, creating, updating, and deleting campaigns.
"""

from typing import Any, Optional

from google.ads.googleads.errors import GoogleAdsException
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import get_google_ads_client, clean_customer_id, format_error, get_default_customer_id, get_enum_name, get_enum_value, micros_to_currency, currency_to_micros


@mcp.tool()
def google_list_accounts() -> list[dict[str, Any]]:
    """Lists all Google Ads customer accounts accessible by the authenticated user.

    These accounts can be used as customer_id or login_customer_id parameters
    in other Google Ads tools.

    Returns:
        list[dict]: List of accessible accounts with id field.

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client()
        customer_service = client.get_service("CustomerService")
        accounts = customer_service.list_accessible_customers().resource_names

        return [
            {"id": account.split("/")[-1]}
            for account in accounts
        ]
    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_list_campaigns(
    customer_id: Optional[str] = None,
    status: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Lists campaigns for a Google Ads customer with performance metrics.

    Args:
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        status: Optional filter by status - ENABLED, PAUSED, or REMOVED.
            If not specified, returns all campaigns.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        list[dict]: List of campaigns with:
            - id: Campaign ID
            - name: Campaign name
            - status: Campaign status (ENABLED, PAUSED, REMOVED)
            - channel_type: Advertising channel (SEARCH, DISPLAY, etc.)
            - budget: Daily budget in account currency
            - start_date: Campaign start date
            - end_date: Campaign end date
            - impressions: Total impressions
            - clicks: Total clicks
            - cost: Total cost in account currency

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
                campaign.id,
                campaign.name,
                campaign.status,
                campaign.advertising_channel_type,
                campaign.campaign_budget,
                campaign.start_date,
                campaign.end_date,
                campaign_budget.amount_micros,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros
            FROM campaign
        """

        if status:
            query += f" WHERE campaign.status = '{status.upper()}'"

        query += " ORDER BY campaign.id"

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        campaigns = []
        for batch in response:
            for row in batch.results:
                campaigns.append({
                    "id": str(row.campaign.id),
                    "name": row.campaign.name,
                    "status": get_enum_name(client, "CampaignStatusEnum", row.campaign.status),
                    "channel_type": get_enum_name(client, "AdvertisingChannelTypeEnum", row.campaign.advertising_channel_type),
                    "budget": micros_to_currency(row.campaign_budget.amount_micros),
                    "start_date": row.campaign.start_date or None,
                    "end_date": row.campaign.end_date or None,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost": micros_to_currency(row.metrics.cost_micros),
                })

        return campaigns

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_get_campaign(
    campaign_id: str,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Gets detailed information about a specific Google Ads campaign.

    Args:
        campaign_id: The campaign ID to retrieve.
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Campaign details including:
            - id: Campaign ID
            - name: Campaign name
            - status: Campaign status
            - channel_type: Advertising channel type
            - channel_sub_type: Advertising channel sub-type
            - budget: Daily budget in account currency
            - budget_delivery_method: Budget delivery method
            - start_date: Campaign start date
            - end_date: Campaign end date
            - target_google_search: Whether targeting Google Search
            - target_search_network: Whether targeting Search Network
            - target_content_network: Whether targeting Display Network
            - impressions: Total impressions
            - clicks: Total clicks
            - cost: Total cost in account currency
            - conversions: Total conversions
            - conversions_value: Total conversion value

    Raises:
        ToolError: If the campaign is not found or API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                campaign.advertising_channel_type,
                campaign.advertising_channel_sub_type,
                campaign.campaign_budget,
                campaign.start_date,
                campaign.end_date,
                campaign.network_settings.target_google_search,
                campaign.network_settings.target_search_network,
                campaign.network_settings.target_content_network,
                campaign_budget.amount_micros,
                campaign_budget.delivery_method,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value
            FROM campaign
            WHERE campaign.id = {campaign_id}
        """

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        for batch in response:
            for row in batch.results:
                return {
                    "id": str(row.campaign.id),
                    "name": row.campaign.name,
                    "status": get_enum_name(client, "CampaignStatusEnum", row.campaign.status),
                    "channel_type": get_enum_name(client, "AdvertisingChannelTypeEnum", row.campaign.advertising_channel_type),
                    "channel_sub_type": get_enum_name(client, "AdvertisingChannelSubTypeEnum", row.campaign.advertising_channel_sub_type),
                    "budget": micros_to_currency(row.campaign_budget.amount_micros),
                    "budget_delivery_method": get_enum_name(client, "BudgetDeliveryMethodEnum", row.campaign_budget.delivery_method),
                    "start_date": row.campaign.start_date or None,
                    "end_date": row.campaign.end_date or None,
                    "target_google_search": row.campaign.network_settings.target_google_search,
                    "target_search_network": row.campaign.network_settings.target_search_network,
                    "target_content_network": row.campaign.network_settings.target_content_network,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost": micros_to_currency(row.metrics.cost_micros),
                    "conversions": row.metrics.conversions,
                    "conversions_value": row.metrics.conversions_value,
                }

        raise ToolError(f"Campaign {campaign_id} not found")

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_create_campaign(
    name: str,
    budget: float,
    customer_id: Optional[str] = None,
    channel_type: str = "SEARCH",
    status: str = "PAUSED",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    target_spend: bool = True,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Creates a new Google Ads campaign with a daily budget.

    Args:
        name: The campaign name.
        budget: Daily budget in account currency (e.g., 10.00 for $10 USD).
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        channel_type: Advertising channel type. Options:
            - SEARCH: Search Network campaigns
            - DISPLAY: Display Network campaigns
            - SHOPPING: Shopping campaigns
            - VIDEO: YouTube video campaigns
            - PERFORMANCE_MAX: Performance Max campaigns
            - DISCOVERY: Discovery campaigns
            - LOCAL: Local campaigns
            - SMART: Smart campaigns
            - HOTEL: Hotel campaigns
        status: Initial campaign status - ENABLED or PAUSED (default).
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.
        target_spend: If True, uses Target Spend bidding to maximize clicks.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Created campaign details:
            - campaign_id: The new campaign ID
            - campaign_resource_name: Full resource name
            - budget_resource_name: Budget resource name
            - status: Creation status

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        # Create budget first
        campaign_budget_service = client.get_service("CampaignBudgetService")
        campaign_budget_operation = client.get_type("CampaignBudgetOperation")
        campaign_budget = campaign_budget_operation.create
        campaign_budget.name = f"{name} Budget"
        campaign_budget.amount_micros = currency_to_micros(budget)
        campaign_budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
        # Performance Max campaigns require non-shared budgets
        if channel_type.upper() == "PERFORMANCE_MAX":
            campaign_budget.explicitly_shared = False

        budget_response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id,
            operations=[campaign_budget_operation],
        )
        budget_resource_name = budget_response.results[0].resource_name

        # Create campaign
        campaign_service = client.get_service("CampaignService")
        campaign_operation = client.get_type("CampaignOperation")
        campaign = campaign_operation.create
        campaign.name = name
        campaign.campaign_budget = budget_resource_name
        campaign.advertising_channel_type = get_enum_value(
            client, "AdvertisingChannelTypeEnum", channel_type
        )
        campaign.status = get_enum_value(client, "CampaignStatusEnum", status)

        # EU accounts require this field
        campaign.contains_eu_political_advertising = get_enum_value(
            client, "EuPoliticalAdvertisingStatusEnum", "DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING"
        )

        if start_date:
            campaign.start_date = start_date.replace("-", "")
        if end_date:
            campaign.end_date = end_date.replace("-", "")

        # Set bidding strategy based on campaign type
        # Performance Max campaigns require maximize_conversions or maximize_conversion_value
        # target_spend is only valid for Search, Display, and some other campaign types
        if channel_type.upper() == "PERFORMANCE_MAX":
            # Performance Max requires maximize_conversions bidding
            campaign.maximize_conversions.target_cpa_micros = 0
        elif target_spend:
            campaign.target_spend.target_spend_micros = 0  # Maximize clicks

        campaign_response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[campaign_operation],
        )

        return {
            "campaign_id": campaign_response.results[0].resource_name.split("/")[-1],
            "campaign_resource_name": campaign_response.results[0].resource_name,
            "budget_resource_name": budget_resource_name,
            "status": "created",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_create_pmax_campaign(
    name: str,
    budget: float,
    business_name: str,
    logo_image_data: str,
    customer_id: Optional[str] = None,
    status: str = "PAUSED",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Creates a Performance Max campaign with brand assets atomically.

    This function creates the campaign, budget, business name asset, logo asset,
    and links them all in a single atomic API call. This is required for accounts
    with Brand Guidelines enabled, which mandate BUSINESS_NAME and LOGO assets
    be linked at campaign creation time.

    Args:
        name: The campaign name.
        budget: Daily budget in account currency (e.g., 10.00 for $10 USD).
        business_name: Business name text (required for Brand Guidelines).
        logo_image_data: Base64 encoded square logo image (1:1 ratio, min 128x128,
            recommended 1200x1200). PNG, JPG, or GIF format.
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        status: Initial campaign status - ENABLED or PAUSED (default).
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Created campaign details:
            - campaign_id: The new campaign ID
            - campaign_resource_name: Full resource name
            - budget_resource_name: Budget resource name
            - business_name_asset_resource_name: Business name asset resource name
            - logo_asset_resource_name: Logo asset resource name
            - status: Creation status

    Raises:
        ToolError: If the API request fails.

    Note:
        After creating the campaign, you need to create an Asset Group with
        headlines, descriptions, and marketing images using google_create_asset_group
        before the campaign can serve ads.
    """
    import base64

    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        # Decode logo image
        try:
            logo_bytes = base64.b64decode(logo_image_data)
        except Exception as e:
            raise ToolError(f"Invalid base64 logo image data: {e}")

        # Services
        ga_service = client.get_service("GoogleAdsService")
        campaign_budget_service = client.get_service("CampaignBudgetService")
        campaign_service = client.get_service("CampaignService")
        asset_service = client.get_service("AssetService")
        campaign_asset_service = client.get_service("CampaignAssetService")

        # Temporary resource IDs for atomic creation
        BUDGET_TEMP_ID = -1
        CAMPAIGN_TEMP_ID = -2
        BUSINESS_NAME_ASSET_TEMP_ID = -3
        LOGO_ASSET_TEMP_ID = -4

        mutate_operations = []

        # 1. Create campaign budget
        budget_op = client.get_type("MutateOperation")
        campaign_budget = budget_op.campaign_budget_operation.create
        campaign_budget.resource_name = campaign_budget_service.campaign_budget_path(
            customer_id, BUDGET_TEMP_ID
        )
        campaign_budget.name = f"{name} Budget"
        campaign_budget.amount_micros = currency_to_micros(budget)
        campaign_budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
        campaign_budget.explicitly_shared = False  # Required for P-Max
        mutate_operations.append(budget_op)

        # 2. Create campaign
        campaign_op = client.get_type("MutateOperation")
        campaign = campaign_op.campaign_operation.create
        campaign.resource_name = campaign_service.campaign_path(
            customer_id, CAMPAIGN_TEMP_ID
        )
        campaign.name = name
        campaign.campaign_budget = campaign_budget_service.campaign_budget_path(
            customer_id, BUDGET_TEMP_ID
        )
        campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
        campaign.status = get_enum_value(client, "CampaignStatusEnum", status)
        # Performance Max requires maximize_conversions bidding
        campaign.maximize_conversions.target_cpa_micros = 0
        # EU accounts require this field
        campaign.contains_eu_political_advertising = get_enum_value(
            client, "EuPoliticalAdvertisingStatusEnum", "DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING"
        )
        if start_date:
            campaign.start_date = start_date.replace("-", "")
        if end_date:
            campaign.end_date = end_date.replace("-", "")
        mutate_operations.append(campaign_op)

        # 3. Create business name text asset
        bn_asset_op = client.get_type("MutateOperation")
        bn_asset = bn_asset_op.asset_operation.create
        bn_asset.resource_name = asset_service.asset_path(
            customer_id, BUSINESS_NAME_ASSET_TEMP_ID
        )
        bn_asset.text_asset.text = business_name
        bn_asset.name = f"{name} - Business Name"
        mutate_operations.append(bn_asset_op)

        # 4. Create logo image asset
        logo_asset_op = client.get_type("MutateOperation")
        logo_asset = logo_asset_op.asset_operation.create
        logo_asset.resource_name = asset_service.asset_path(
            customer_id, LOGO_ASSET_TEMP_ID
        )
        logo_asset.image_asset.data = logo_bytes
        logo_asset.name = f"{name} - Logo"
        mutate_operations.append(logo_asset_op)

        # 5. Link business name asset to campaign
        bn_link_op = client.get_type("MutateOperation")
        bn_campaign_asset = bn_link_op.campaign_asset_operation.create
        bn_campaign_asset.campaign = campaign_service.campaign_path(
            customer_id, CAMPAIGN_TEMP_ID
        )
        bn_campaign_asset.asset = asset_service.asset_path(
            customer_id, BUSINESS_NAME_ASSET_TEMP_ID
        )
        bn_campaign_asset.field_type = client.enums.AssetFieldTypeEnum.BUSINESS_NAME
        mutate_operations.append(bn_link_op)

        # 6. Link logo asset to campaign
        logo_link_op = client.get_type("MutateOperation")
        logo_campaign_asset = logo_link_op.campaign_asset_operation.create
        logo_campaign_asset.campaign = campaign_service.campaign_path(
            customer_id, CAMPAIGN_TEMP_ID
        )
        logo_campaign_asset.asset = asset_service.asset_path(
            customer_id, LOGO_ASSET_TEMP_ID
        )
        logo_campaign_asset.field_type = client.enums.AssetFieldTypeEnum.LOGO
        mutate_operations.append(logo_link_op)

        # Execute atomic bulk mutate
        response = ga_service.mutate(
            customer_id=customer_id,
            mutate_operations=mutate_operations,
        )

        # Extract resource names from response
        result = {
            "status": "created",
        }

        for op_response in response.mutate_operation_responses:
            if op_response.HasField("campaign_budget_result"):
                result["budget_resource_name"] = op_response.campaign_budget_result.resource_name
            elif op_response.HasField("campaign_result"):
                result["campaign_resource_name"] = op_response.campaign_result.resource_name
                result["campaign_id"] = op_response.campaign_result.resource_name.split("/")[-1]
            elif op_response.HasField("asset_result"):
                resource_name = op_response.asset_result.resource_name
                # We can't easily distinguish which asset is which from the response,
                # but we track the order
                if "business_name_asset_resource_name" not in result:
                    result["business_name_asset_resource_name"] = resource_name
                else:
                    result["logo_asset_resource_name"] = resource_name

        return result

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_update_campaign(
    campaign_id: str,
    customer_id: Optional[str] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    target_content_network: Optional[bool] = None,
    target_search_network: Optional[bool] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Updates an existing Google Ads campaign.

    Args:
        campaign_id: The campaign ID to update.
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        name: Optional new campaign name.
        status: Optional new status - ENABLED, PAUSED, or REMOVED.
        start_date: Optional new start date in YYYY-MM-DD format.
        end_date: Optional new end date in YYYY-MM-DD format.
        target_content_network: Optional bool to enable/disable Display Network.
            Set to False to disable Display Network (recommended for Search campaigns).
        target_search_network: Optional bool to enable/disable Search Partners.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Updated campaign details:
            - campaign_resource_name: Full resource name
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

        campaign_service = client.get_service("CampaignService")
        campaign_operation = client.get_type("CampaignOperation")
        campaign = campaign_operation.update
        campaign.resource_name = f"customers/{customer_id}/campaigns/{campaign_id}"

        field_mask = []

        if name is not None:
            campaign.name = name
            field_mask.append("name")

        if status is not None:
            campaign.status = get_enum_value(client, "CampaignStatusEnum", status)
            field_mask.append("status")

        if start_date is not None:
            campaign.start_date = start_date.replace("-", "")
            field_mask.append("start_date")

        if end_date is not None:
            campaign.end_date = end_date.replace("-", "")
            field_mask.append("end_date")

        if target_content_network is not None:
            campaign.network_settings.target_content_network = target_content_network
            field_mask.append("network_settings.target_content_network")

        if target_search_network is not None:
            campaign.network_settings.target_search_network = target_search_network
            field_mask.append("network_settings.target_search_network")

        if not field_mask:
            raise ToolError("No fields to update. Provide at least one field.")

        campaign_operation.update_mask.paths.extend(field_mask)

        response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[campaign_operation],
        )

        return {
            "campaign_resource_name": response.results[0].resource_name,
            "updated_fields": field_mask,
            "status": "updated",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_delete_campaign(
    campaign_id: str,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Removes a Google Ads campaign.

    Note: This sets the campaign status to REMOVED. The campaign data
    is retained and can still be queried but cannot be reactivated.

    Args:
        campaign_id: The campaign ID to remove.
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Removal status:
            - campaign_resource_name: Full resource name
            - status: "removed"

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        campaign_service = client.get_service("CampaignService")
        campaign_operation = client.get_type("CampaignOperation")
        campaign_operation.remove = f"customers/{customer_id}/campaigns/{campaign_id}"

        response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[campaign_operation],
        )

        return {
            "campaign_resource_name": response.results[0].resource_name,
            "status": "removed",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e
