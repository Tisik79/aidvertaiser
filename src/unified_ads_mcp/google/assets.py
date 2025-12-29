"""Asset management tools for Google Ads API.

This module provides MCP tools for managing Google Ads assets including
text assets (headlines, descriptions), image assets, and asset linking
for Performance Max campaigns.
"""

import base64
import os
from typing import Any, Optional

from google.ads.googleads.errors import GoogleAdsException
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import (
    get_google_ads_client,
    clean_customer_id,
    format_error,
    get_default_customer_id,
    get_enum_name,
    get_enum_value,
)


@mcp.tool()
def google_list_assets(
    customer_id: Optional[str] = None,
    asset_type: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Lists assets for a Google Ads customer.

    Args:
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        asset_type: Optional filter by asset type. Options:
            - TEXT: Text assets (headlines, descriptions)
            - IMAGE: Image assets
            - MEDIA_BUNDLE: Media bundle assets
            - YOUTUBE_VIDEO: YouTube video assets
            - CALL_TO_ACTION: Call to action assets
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        list[dict]: List of assets with:
            - id: Asset ID
            - resource_name: Full resource name
            - type: Asset type
            - name: Asset name (if set)
            - text: Text content (for TEXT assets)
            - image_url: Image URL (for IMAGE assets)

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        ga_service = client.get_service("GoogleAdsService")

        query = """
            SELECT
                asset.id,
                asset.resource_name,
                asset.type,
                asset.name,
                asset.text_asset.text,
                asset.image_asset.full_size.url,
                asset.image_asset.file_size,
                asset.youtube_video_asset.youtube_video_id
            FROM asset
        """

        if asset_type:
            query += f" WHERE asset.type = '{asset_type.upper()}'"

        query += " ORDER BY asset.id LIMIT 100"

        response = ga_service.search(customer_id=customer_id, query=query)

        assets = []
        for row in response:
            asset = row.asset
            asset_data = {
                "id": str(asset.id),
                "resource_name": asset.resource_name,
                "type": get_enum_name(client, "AssetTypeEnum", asset.type),
                "name": asset.name if asset.name else None,
            }

            # Add type-specific fields
            if asset.text_asset.text:
                asset_data["text"] = asset.text_asset.text
            if asset.image_asset.full_size.url:
                asset_data["image_url"] = asset.image_asset.full_size.url
                asset_data["file_size"] = asset.image_asset.file_size
            if asset.youtube_video_asset.youtube_video_id:
                asset_data["youtube_video_id"] = asset.youtube_video_asset.youtube_video_id

            assets.append(asset_data)

        return assets

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_create_text_asset(
    text: str,
    customer_id: Optional[str] = None,
    name: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Creates a text asset (for headlines, descriptions, etc.).

    Args:
        text: The text content for the asset.
            - Headlines: max 30 characters
            - Descriptions: max 90 characters
        customer_id: The Google Ads customer ID.
            Uses default from config if not provided.
        name: Optional name for the asset.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Created asset details:
            - asset_id: The new asset ID
            - resource_name: Full resource name
            - text: The text content

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        asset_service = client.get_service("AssetService")

        # Create the text asset
        asset_operation = client.get_type("AssetOperation")
        asset = asset_operation.create
        asset.text_asset.text = text
        if name:
            asset.name = name

        # Execute the mutation
        response = asset_service.mutate_assets(
            customer_id=customer_id,
            operations=[asset_operation],
        )

        created_resource = response.results[0].resource_name
        asset_id = created_resource.split("/")[-1]

        return {
            "asset_id": asset_id,
            "resource_name": created_resource,
            "text": text,
            "status": "created",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_create_image_asset(
    image_data: str,
    customer_id: Optional[str] = None,
    name: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Creates an image asset from base64 encoded data.

    Args:
        image_data: Base64 encoded image data (PNG, JPG, or GIF).
        customer_id: The Google Ads customer ID.
            Uses default from config if not provided.
        name: Optional name for the asset.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Created asset details:
            - asset_id: The new asset ID
            - resource_name: Full resource name
            - status: Creation status

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        asset_service = client.get_service("AssetService")

        # Decode base64 image data
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            raise ToolError(f"Invalid base64 image data: {e}")

        # Create the image asset
        asset_operation = client.get_type("AssetOperation")
        asset = asset_operation.create
        asset.image_asset.data = image_bytes
        if name:
            asset.name = name

        # Execute the mutation
        response = asset_service.mutate_assets(
            customer_id=customer_id,
            operations=[asset_operation],
        )

        created_resource = response.results[0].resource_name
        asset_id = created_resource.split("/")[-1]

        return {
            "asset_id": asset_id,
            "resource_name": created_resource,
            "status": "created",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_create_text_assets_batch(
    headlines: list[str],
    descriptions: list[str],
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Creates multiple text assets in a single batch operation.

    This is useful for creating all assets needed for a Performance Max
    campaign at once.

    Args:
        headlines: List of headline texts (3-15 headlines, max 30 chars each).
        descriptions: List of description texts (2-5 descriptions, max 90 chars each).
        customer_id: The Google Ads customer ID.
            Uses default from config if not provided.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Created assets details:
            - headline_assets: List of created headline asset resource names
            - description_assets: List of created description asset resource names
            - status: Creation status

    Raises:
        ToolError: If the API request fails or validation fails.
    """
    try:
        # Validate inputs
        if len(headlines) < 3:
            raise ToolError("At least 3 headlines are required")
        if len(headlines) > 15:
            raise ToolError("Maximum 15 headlines allowed")
        if len(descriptions) < 2:
            raise ToolError("At least 2 descriptions are required")
        if len(descriptions) > 5:
            raise ToolError("Maximum 5 descriptions allowed")

        for i, h in enumerate(headlines):
            if len(h) > 30:
                raise ToolError(f"Headline {i+1} exceeds 30 characters: '{h}'")

        for i, d in enumerate(descriptions):
            if len(d) > 90:
                raise ToolError(f"Description {i+1} exceeds 90 characters")

        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        asset_service = client.get_service("AssetService")

        # Create operations for all assets
        operations = []

        # Headlines
        for headline in headlines:
            op = client.get_type("AssetOperation")
            op.create.text_asset.text = headline
            operations.append(op)

        # Descriptions
        for description in descriptions:
            op = client.get_type("AssetOperation")
            op.create.text_asset.text = description
            operations.append(op)

        # Execute batch mutation
        response = asset_service.mutate_assets(
            customer_id=customer_id,
            operations=operations,
        )

        # Split results into headlines and descriptions
        headline_count = len(headlines)
        headline_assets = [
            r.resource_name for r in response.results[:headline_count]
        ]
        description_assets = [
            r.resource_name for r in response.results[headline_count:]
        ]

        return {
            "headline_assets": headline_assets,
            "description_assets": description_assets,
            "headlines_created": len(headline_assets),
            "descriptions_created": len(description_assets),
            "status": "created",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_link_asset_to_campaign(
    campaign_id: str,
    asset_resource_name: str,
    field_type: str,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Links an asset to a campaign (for brand guidelines, etc.).

    This is used to link BUSINESS_NAME and LOGO assets at the campaign level,
    which is required for Performance Max campaigns since API v21.

    Args:
        campaign_id: The campaign ID to link the asset to.
        asset_resource_name: The full resource name of the asset.
        field_type: The field type for the asset. Options:
            - BUSINESS_NAME: Business name text asset
            - LOGO: Logo image asset
            - MARKETING_IMAGE: Marketing image
            - SQUARE_MARKETING_IMAGE: Square marketing image
            - HEADLINE: Headline text
            - DESCRIPTION: Description text
        customer_id: The Google Ads customer ID.
            Uses default from config if not provided.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Link result:
            - campaign_asset_resource_name: The created link resource name
            - status: Link status

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        campaign_asset_service = client.get_service("CampaignAssetService")
        campaign_service = client.get_service("CampaignService")

        # Get campaign resource name
        campaign_resource = campaign_service.campaign_path(customer_id, campaign_id)

        # Create campaign asset link
        operation = client.get_type("CampaignAssetOperation")
        campaign_asset = operation.create
        campaign_asset.campaign = campaign_resource
        campaign_asset.asset = asset_resource_name
        campaign_asset.field_type = get_enum_value(
            client, "AssetFieldTypeEnum", field_type.upper()
        )

        response = campaign_asset_service.mutate_campaign_assets(
            customer_id=customer_id,
            operations=[operation],
        )

        return {
            "campaign_asset_resource_name": response.results[0].resource_name,
            "status": "linked",
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e
