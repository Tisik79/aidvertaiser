"""Label management tools for Google Ads API.

This module provides MCP tools for creating, listing, and assigning
labels to campaigns for organizational purposes (e.g., "holiday-pausable").
"""

from typing import Any, Optional

from google.ads.googleads.errors import GoogleAdsException
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import (
    get_google_ads_client,
    format_error,
    resolve_customer_id,
)


@mcp.tool()
def google_create_label(
    name: str,
    description: Optional[str] = None,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Creates a label for organizing campaigns and other entities.

    Labels help group campaigns for bulk operations (e.g., "holiday-pausable",
    "brand-campaigns", "low-priority").

    Args:
        name: Label name (max 100 chars). Must be unique in the account.
        description: Optional description of the label's purpose.
        customer_id: The Google Ads customer ID. Uses default if not provided.
        login_customer_id: Optional MCC account ID.

    Returns:
        dict: Created label with resource_name and id.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        label_service = client.get_service("LabelService")
        label_op = client.get_type("LabelOperation")
        label = label_op.create
        label.name = name
        if description:
            label.text_label.description = description

        response = label_service.mutate_labels(
            customer_id=customer_id, operations=[label_op]
        )
        resource_name = response.results[0].resource_name
        label_id = resource_name.split("/")[-1]

        return {
            "label_resource_name": resource_name,
            "label_id": label_id,
            "name": name,
            "status": "created",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_list_labels(
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Lists all labels in the Google Ads account.

    Args:
        customer_id: The Google Ads customer ID. Uses default if not provided.
        login_customer_id: Optional MCC account ID.

    Returns:
        list[dict]: Labels with id, name, description, and campaign_count.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query="""
                SELECT label.id, label.name, label.text_label.description,
                       label.resource_name
                FROM label
                ORDER BY label.name
            """,
        )

        labels = []
        for batch in response:
            for row in batch.results:
                labels.append({
                    "id": str(row.label.id),
                    "name": row.label.name,
                    "description": row.label.text_label.description or None,
                    "resource_name": row.label.resource_name,
                })

        return labels

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_delete_label(
    label_id: str,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Deletes a label from the Google Ads account.

    Args:
        label_id: The label ID to delete.
        customer_id: The Google Ads customer ID. Uses default if not provided.
        login_customer_id: Optional MCC account ID.

    Returns:
        dict: Deletion status.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        label_service = client.get_service("LabelService")
        label_op = client.get_type("LabelOperation")
        label_op.remove = f"customers/{customer_id}/labels/{label_id}"

        label_service.mutate_labels(
            customer_id=customer_id, operations=[label_op]
        )

        return {"label_id": label_id, "status": "deleted"}

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_assign_label_to_campaigns(
    label_id: str,
    campaign_ids: list[str],
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Assigns a label to one or more campaigns.

    Args:
        label_id: The label ID to assign.
        campaign_ids: List of campaign IDs to label.
        customer_id: The Google Ads customer ID. Uses default if not provided.
        login_customer_id: Optional MCC account ID.

    Returns:
        dict: Result with assigned_count.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        campaign_label_service = client.get_service("CampaignLabelService")
        ops = []
        for cid in campaign_ids:
            op = client.get_type("CampaignLabelOperation")
            cl = op.create
            cl.campaign = f"customers/{customer_id}/campaigns/{cid}"
            cl.label = f"customers/{customer_id}/labels/{label_id}"
            ops.append(op)

        campaign_label_service.mutate_campaign_labels(
            customer_id=customer_id, operations=ops
        )

        return {
            "label_id": label_id,
            "assigned_count": len(ops),
            "campaign_ids": campaign_ids,
            "status": "assigned",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_remove_label_from_campaigns(
    label_id: str,
    campaign_ids: list[str],
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Removes a label from one or more campaigns.

    Args:
        label_id: The label ID to remove.
        campaign_ids: List of campaign IDs to unlabel.
        customer_id: The Google Ads customer ID. Uses default if not provided.
        login_customer_id: Optional MCC account ID.

    Returns:
        dict: Result with removed_count.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        ga_service = client.get_service("GoogleAdsService")
        campaign_label_service = client.get_service("CampaignLabelService")

        # Find campaign_label resource names for these campaigns
        campaign_ids_str = ", ".join(campaign_ids)
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=f"""
                SELECT campaign_label.resource_name, campaign.id
                FROM campaign_label
                WHERE label.id = {label_id}
                  AND campaign.id IN ({campaign_ids_str})
            """,
        )

        ops = []
        for batch in response:
            for row in batch.results:
                op = client.get_type("CampaignLabelOperation")
                op.remove = row.campaign_label.resource_name
                ops.append(op)

        if ops:
            campaign_label_service.mutate_campaign_labels(
                customer_id=customer_id, operations=ops
            )

        return {
            "label_id": label_id,
            "removed_count": len(ops),
            "campaign_ids": campaign_ids,
            "status": "removed",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_get_campaigns_by_label(
    label_id: str,
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Gets all campaigns that have a specific label.

    Args:
        label_id: The label ID to filter by.
        status: Optional filter by campaign status (ENABLED, PAUSED).
        customer_id: The Google Ads customer ID. Uses default if not provided.
        login_customer_id: Optional MCC account ID.

    Returns:
        list[dict]: Campaigns with id, name, status.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = resolve_customer_id(customer_id)
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT campaign.id, campaign.name, campaign.status
            FROM campaign_label
            WHERE label.id = {label_id}
        """
        if status:
            query += f" AND campaign.status = '{status.upper()}'"

        response = ga_service.search_stream(
            customer_id=customer_id, query=query
        )

        from .client import get_enum_name

        campaigns = []
        for batch in response:
            for row in batch.results:
                campaigns.append({
                    "id": str(row.campaign.id),
                    "name": row.campaign.name,
                    "status": get_enum_name(
                        client, "CampaignStatusEnum", row.campaign.status
                    ),
                })

        return campaigns

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e
