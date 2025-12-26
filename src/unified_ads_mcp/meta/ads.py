"""Meta Ads Ad Management Tools.

This module provides MCP tools for managing Meta Ads ads, including
listing, creating, updating, and retrieving ad details and creatives.
"""

import json
from typing import Optional, List, Dict, Any

from ..server import mcp
from .client import (
    make_api_request,
    meta_api_tool,
    ensure_account_prefix
)


@mcp.tool()
@meta_api_tool
async def meta_list_ads(
    account_id: str,
    access_token: Optional[str] = None,
    adset_id: Optional[str] = None,
    campaign_id: Optional[str] = None,
    limit: int = 25,
    after: Optional[str] = None
) -> dict:
    """List ads for a Meta Ads account with optional filtering.

    Retrieves ads with their configuration including creative references,
    status, and tracking information.

    Args:
        account_id: Meta Ads account ID (format: act_XXXXXXXXX).
        access_token: Meta API access token (uses cached token if not provided).
        adset_id: Optional ad set ID to filter ads (takes precedence over campaign_id).
        campaign_id: Optional campaign ID to filter ads.
        limit: Maximum number of ads to return (default: 25).
        after: Pagination cursor for next page of results.

    Returns:
        Dictionary containing:
            - data: List of ad objects with id, name, creative, status, etc.
            - paging: Pagination cursors for navigating results.

    Example:
        >>> ads = await meta_list_ads("act_123456789", adset_id="23842614006130185")
        >>> for ad in ads["data"]:
        ...     print(f"{ad['name']}: {ad['status']}")
    """
    if not account_id:
        return {"error": {"message": "account_id is required"}}

    account_id = ensure_account_prefix(account_id)

    # Prioritize adset_id, then campaign_id, then account-level
    if adset_id:
        endpoint = f"{adset_id}/ads"
    elif campaign_id:
        endpoint = f"{campaign_id}/ads"
    else:
        endpoint = f"{account_id}/ads"

    params = {
        "fields": "id,name,adset_id,campaign_id,status,effective_status,creative,created_time,updated_time,bid_amount,conversion_domain,tracking_specs",
        "limit": limit
    }

    if after:
        params["after"] = after

    data = await make_api_request(endpoint, access_token, params)
    return data


@mcp.tool()
@meta_api_tool
async def meta_get_ad_details(
    ad_id: str,
    access_token: Optional[str] = None
) -> dict:
    """Get detailed information about a specific ad.

    Retrieves comprehensive ad details including creative reference,
    status, bid amount, and tracking configuration.

    Args:
        ad_id: Meta Ads ad ID.
        access_token: Meta API access token (uses cached token if not provided).

    Returns:
        Dictionary containing ad details:
            - id: Ad ID
            - name: Ad name
            - adset_id: Parent ad set ID
            - campaign_id: Parent campaign ID
            - status: Ad status
            - effective_status: Effective delivery status
            - creative: Creative reference with ID
            - bid_amount: Bid amount if set
            - tracking_specs: Tracking configuration
            - preview_shareable_link: Link to preview the ad

    Example:
        >>> details = await meta_get_ad_details("23842614006140185")
        >>> print(f"Status: {details['status']}, Creative: {details['creative']['id']}")
    """
    if not ad_id:
        return {"error": {"message": "ad_id is required"}}

    endpoint = f"{ad_id}"
    params = {
        "fields": "id,name,adset_id,campaign_id,status,effective_status,creative,created_time,updated_time,bid_amount,conversion_domain,tracking_specs,preview_shareable_link"
    }

    data = await make_api_request(endpoint, access_token, params)
    return data


@mcp.tool()
@meta_api_tool
async def meta_get_ad_creatives(
    ad_id: str,
    access_token: Optional[str] = None
) -> dict:
    """Get creative details for a specific ad.

    Retrieves the creative content associated with an ad, including
    images, copy, and call-to-action information.

    Args:
        ad_id: Meta Ads ad ID.
        access_token: Meta API access token (uses cached token if not provided).

    Returns:
        Dictionary containing:
            - data: List of creative objects with:
                - id: Creative ID
                - name: Creative name
                - status: Creative status
                - thumbnail_url: Thumbnail image URL
                - image_url: Full image URL
                - image_hash: Image hash for reference
                - object_story_spec: Page post specification
                - asset_feed_spec: Dynamic creative assets

    Example:
        >>> creatives = await meta_get_ad_creatives("23842614006140185")
        >>> for creative in creatives["data"]:
        ...     print(f"{creative['name']}: {creative.get('thumbnail_url')}")
    """
    if not ad_id:
        return {"error": {"message": "ad_id is required"}}

    endpoint = f"{ad_id}/adcreatives"
    params = {
        "fields": "id,name,status,thumbnail_url,image_url,image_hash,object_story_spec,asset_feed_spec,call_to_action_type,link_url"
    }

    data = await make_api_request(endpoint, access_token, params)

    # Extract image URLs for convenience if available
    if "data" in data:
        for creative in data["data"]:
            image_urls = []
            if "image_url" in creative and creative["image_url"]:
                image_urls.append(creative["image_url"])
            if "thumbnail_url" in creative and creative["thumbnail_url"]:
                image_urls.append(creative["thumbnail_url"])
            if "object_story_spec" in creative:
                spec = creative["object_story_spec"]
                if "link_data" in spec and "picture" in spec["link_data"]:
                    image_urls.append(spec["link_data"]["picture"])
            creative["extracted_image_urls"] = image_urls

    return data


@mcp.tool()
@meta_api_tool
async def meta_create_ad(
    account_id: str,
    name: str,
    adset_id: str,
    creative_id: str,
    access_token: Optional[str] = None,
    status: str = "PAUSED",
    bid_amount: Optional[int] = None,
    tracking_specs: Optional[List[Dict[str, Any]]] = None
) -> dict:
    """Create a new ad with an existing creative.

    Creates an ad that uses a previously created creative and places it
    in the specified ad set. New ads are created in PAUSED status by default.

    Args:
        account_id: Meta Ads account ID (format: act_XXXXXXXXX).
        name: Ad name (required).
        adset_id: Ad set ID where this ad will be placed (required).
        creative_id: ID of an existing creative to use (required).
            Use meta_create_creative() to create a creative first.
        access_token: Meta API access token (uses cached token if not provided).
        status: Initial status (default: PAUSED).
        bid_amount: Optional bid amount in cents (overrides ad set bid).
        tracking_specs: Optional tracking specifications for pixel events.
            Example: [{"action.type": "offsite_conversion", "fb_pixel": ["YOUR_PIXEL_ID"]}]

    Returns:
        Dictionary containing:
            - id: Created ad ID

    Note:
        If the creative uses Dynamic Creative features, the parent ad set
        must have is_dynamic_creative=true, otherwise creation will fail.

    Example:
        >>> result = await meta_create_ad(
        ...     account_id="act_123456789",
        ...     name="Summer Sale Ad v1",
        ...     adset_id="23842614006130185",
        ...     creative_id="23842614006150185"
        ... )
        >>> print(f"Created ad: {result['id']}")
    """
    if not account_id:
        return {"error": {"message": "account_id is required"}}
    if not name:
        return {"error": {"message": "name is required"}}
    if not adset_id:
        return {"error": {"message": "adset_id is required"}}
    if not creative_id:
        return {"error": {"message": "creative_id is required"}}

    account_id = ensure_account_prefix(account_id)

    endpoint = f"{account_id}/ads"

    params = {
        "name": name,
        "adset_id": adset_id,
        "creative": json.dumps({"creative_id": creative_id}),
        "status": status
    }

    if bid_amount is not None:
        params["bid_amount"] = str(bid_amount)

    if tracking_specs is not None:
        params["tracking_specs"] = json.dumps(tracking_specs)

    try:
        data = await make_api_request(endpoint, access_token, params, method="POST")
        return data
    except Exception as e:
        return {
            "error": {
                "message": "Failed to create ad",
                "details": str(e)
            }
        }


@mcp.tool()
@meta_api_tool
async def meta_update_ad(
    ad_id: str,
    access_token: Optional[str] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    creative_id: Optional[str] = None,
    bid_amount: Optional[int] = None,
    tracking_specs: Optional[List[Dict[str, Any]]] = None
) -> dict:
    """Update an existing ad's settings.

    Updates specified fields of an ad. Only provided parameters
    will be updated; others remain unchanged.

    Args:
        ad_id: Meta Ads ad ID (required).
        access_token: Meta API access token (uses cached token if not provided).
        name: New ad name.
        status: New status. Options: ACTIVE, PAUSED, DELETED.
        creative_id: ID of a new creative to use (changes the ad's content).
        bid_amount: New bid amount in cents.
        tracking_specs: New tracking specifications.

    Returns:
        Dictionary containing:
            - success: True if update was successful

    Example:
        >>> result = await meta_update_ad(
        ...     ad_id="23842614006140185",
        ...     status="ACTIVE"
        ... )
    """
    if not ad_id:
        return {"error": {"message": "ad_id is required"}}

    params = {}

    if name is not None:
        params["name"] = name

    if status is not None:
        params["status"] = status

    if creative_id is not None:
        params["creative"] = json.dumps({"creative_id": creative_id})

    if bid_amount is not None:
        params["bid_amount"] = str(bid_amount)

    if tracking_specs is not None:
        params["tracking_specs"] = json.dumps(tracking_specs)

    if not params:
        return {"error": {"message": "No update parameters provided"}}

    endpoint = f"{ad_id}"

    try:
        data = await make_api_request(endpoint, access_token, params, method="POST")
        return data
    except Exception as e:
        return {
            "error": {
                "message": f"Failed to update ad {ad_id}",
                "details": str(e)
            }
        }
