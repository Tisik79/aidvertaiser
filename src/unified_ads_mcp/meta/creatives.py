"""Meta Ads Creative Management Tools.

This module provides MCP tools for managing Meta Ads creatives, including
uploading images, creating creatives, and updating creative content.
"""

import json
import base64
import os
import httpx
from typing import Optional, List, Dict, Any

from ..server import mcp
from .client import (
    make_api_request,
    meta_api_tool,
    ensure_account_prefix,
    get_default_account_id,
)


async def download_image_from_url(url: str) -> Optional[bytes]:
    """Download an image from a URL.

    Args:
        url: URL of the image to download.

    Returns:
        Image bytes or None if download failed.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0, follow_redirects=True)
            response.raise_for_status()
            return response.content
    except Exception:
        return None


@mcp.tool()
@meta_api_tool
async def meta_upload_image(
    account_id: Optional[str] = None,
    access_token: Optional[str] = None,
    image_url: Optional[str] = None,
    file: Optional[str] = None,
    file_path: Optional[str] = None,
    name: Optional[str] = None
) -> dict:
    """Upload an image to use in Meta Ads creatives.

    Uploads an image to the ad account's image library. The returned
    image hash can be used when creating creatives.

    Args:
        account_id: Meta Ads account ID (format: act_XXXXXXXXX).
            Uses default from config if not provided.
        access_token: Meta API access token (uses cached token if not provided).
        image_url: Direct URL to an image to fetch and upload.
        file: Base64-encoded image data or data URL
            (e.g., "data:image/png;base64,iVBORw0KG...").
        file_path: Local file path to an image (e.g., "/home/user/image.jpg").
        name: Optional name for the image (default: auto-generated).

    Returns:
        Dictionary containing:
            - success: True if upload successful
            - image_hash: Hash of the uploaded image (use this in creatives)
            - account_id: Account the image was uploaded to
            - name: Image name
            - images: Full image data including URL

    Note:
        Provide ONE of: image_url, file (base64), or file_path.

    Example:
        >>> result = await meta_upload_image(
        ...     account_id="act_123456789",
        ...     file_path="/home/user/images/product.jpg",
        ...     name="Product Image"
        ... )
        >>> image_hash = result["image_hash"]
        >>> # Now use image_hash in meta_create_creative()
    """
    account_id = account_id or get_default_account_id()
    if not account_id:
        return {"error": {"message": "account_id is required - configure default_account_id in meta-ads.yaml"}}

    if not file and not image_url and not file_path:
        return {"error": {"message": "Provide one of: 'file' (base64/data URL), 'image_url', or 'file_path'"}}

    account_id = ensure_account_prefix(account_id)

    try:
        encoded_image = ""
        inferred_name = name or ""

        if file_path:
            # Handle local file path
            if not os.path.isfile(file_path):
                return {
                    "error": {
                        "message": f"File not found: {file_path}",
                        "suggestions": [
                            "Check that the file path is correct",
                            "Ensure the file exists and is readable"
                        ]
                    }
                }

            try:
                with open(file_path, "rb") as f:
                    image_bytes = f.read()
                encoded_image = base64.b64encode(image_bytes).decode("utf-8")

                # Infer name from filename
                if not inferred_name:
                    inferred_name = os.path.basename(file_path)
            except Exception as e:
                return {
                    "error": {
                        "message": f"Failed to read file: {file_path}",
                        "details": str(e)
                    }
                }

        elif file:
            # Handle data URL or raw base64
            if file.startswith("data:") and "base64," in file:
                header, base64_payload = file.split("base64,", 1)
                encoded_image = base64_payload.strip()

                # Infer extension from MIME type
                if not inferred_name:
                    mime_type = header[5:].split(";")[0].strip()
                    ext_map = {
                        "image/png": ".png",
                        "image/jpeg": ".jpg",
                        "image/jpg": ".jpg",
                        "image/webp": ".webp",
                        "image/gif": ".gif"
                    }
                    ext = ext_map.get(mime_type, ".png")
                    inferred_name = f"upload{ext}"
            else:
                # Raw base64
                encoded_image = file.strip()
                if not inferred_name:
                    inferred_name = "upload.png"
        else:
            # Download from URL
            image_bytes = await download_image_from_url(image_url)

            if not image_bytes:
                return {
                    "error": {
                        "message": "Could not download image from URL",
                        "image_url": image_url,
                        "suggestions": [
                            "Ensure the URL is publicly accessible",
                            "Check that the URL points directly to an image file"
                        ]
                    }
                }

            encoded_image = base64.b64encode(image_bytes).decode("utf-8")

            # Infer name from URL
            if not inferred_name:
                try:
                    path_no_query = image_url.split("?")[0]
                    filename = os.path.basename(path_no_query)
                    inferred_name = filename if filename else "upload.jpg"
                except Exception:
                    inferred_name = "upload.jpg"

        final_name = name or inferred_name or "upload.png"

        endpoint = f"{account_id}/adimages"
        params = {
            "bytes": encoded_image,
            "name": final_name
        }

        data = await make_api_request(endpoint, access_token, params, method="POST")

        # Normalize response
        if isinstance(data, dict) and "images" in data and isinstance(data["images"], dict):
            images_dict = data["images"]
            images_list = []
            for hash_key, info in images_dict.items():
                normalized = {
                    "hash": info.get("hash") or hash_key,
                    "url": info.get("url"),
                    "width": info.get("width"),
                    "height": info.get("height"),
                    "name": info.get("name")
                }
                normalized = {k: v for k, v in normalized.items() if v is not None}
                images_list.append(normalized)

            images_list.sort(key=lambda i: i.get("hash", ""))
            primary_hash = images_list[0].get("hash") if images_list else None

            return {
                "success": True,
                "account_id": account_id,
                "name": final_name,
                "image_hash": primary_hash,
                "images": images_list
            }

        if isinstance(data, dict) and "error" in data:
            return data

        return {
            "success": True,
            "account_id": account_id,
            "name": final_name,
            "raw_response": data
        }

    except Exception as e:
        return {
            "error": {
                "message": "Failed to upload image",
                "details": str(e)
            }
        }


@mcp.tool()
@meta_api_tool
async def meta_create_creative(
    image_hash: str,
    page_id: str,
    name: str,
    message: str,
    link_url: str,
    account_id: Optional[str] = None,
    access_token: Optional[str] = None,
    headline: Optional[str] = None,
    description: Optional[str] = None,
    call_to_action_type: Optional[str] = None,
    instagram_actor_id: Optional[str] = None
) -> dict:
    """Create a new ad creative using an uploaded image.

    Creates a creative that can be used in ads. The creative combines
    an image with copy, headline, and call-to-action.

    Args:
        image_hash: Hash of the uploaded image (from meta_upload_image).
        page_id: Facebook Page ID for the ad (required).
        name: Creative name (required).
        message: Primary ad copy/text (required).
        link_url: Destination URL when users click the ad (required).
        account_id: Meta Ads account ID (format: act_XXXXXXXXX).
            Uses default from config if not provided.
        access_token: Meta API access token (uses cached token if not provided).
        headline: Ad headline (appears below the image).
        description: Ad description (appears below headline).
        call_to_action_type: CTA button type. Options:
            - LEARN_MORE
            - SHOP_NOW
            - SIGN_UP
            - SUBSCRIBE
            - DOWNLOAD
            - GET_OFFER
            - CONTACT_US
            - BOOK_NOW
            - WATCH_MORE
        instagram_actor_id: Instagram account ID for Instagram placements.

    Returns:
        Dictionary containing:
            - success: True if created successfully
            - creative_id: ID of the created creative
            - details: Full creative details

    Example:
        >>> # First upload an image
        >>> image = await meta_upload_image(
        ...     account_id="act_123456789",
        ...     image_url="https://example.com/hero.jpg"
        ... )
        >>>
        >>> # Then create the creative
        >>> creative = await meta_create_creative(
        ...     account_id="act_123456789",
        ...     image_hash=image["image_hash"],
        ...     page_id="123456789012345",
        ...     name="Summer Sale Creative",
        ...     message="Don't miss our biggest sale of the year!",
        ...     link_url="https://example.com/summer-sale",
        ...     headline="50% Off Everything",
        ...     call_to_action_type="SHOP_NOW"
        ... )
        >>> creative_id = creative["creative_id"]
    """
    account_id = account_id or get_default_account_id()
    if not account_id:
        return {"error": {"message": "account_id is required - configure default_account_id in meta-ads.yaml"}}
    if not image_hash:
        return {"error": {"message": "image_hash is required"}}
    if not page_id:
        return {"error": {"message": "page_id is required"}}
    if not name:
        return {"error": {"message": "name is required"}}
    if not message:
        return {"error": {"message": "message is required"}}
    if not link_url:
        return {"error": {"message": "link_url is required"}}

    account_id = ensure_account_prefix(account_id)

    # Build the creative data
    creative_data = {
        "name": name,
        "object_story_spec": {
            "page_id": page_id,
            "link_data": {
                "image_hash": image_hash,
                "link": link_url,
                "message": message
            }
        }
    }

    if headline:
        creative_data["object_story_spec"]["link_data"]["name"] = headline

    if description:
        creative_data["object_story_spec"]["link_data"]["description"] = description

    if call_to_action_type:
        creative_data["object_story_spec"]["link_data"]["call_to_action"] = {
            "type": call_to_action_type
        }

    if instagram_actor_id:
        creative_data["instagram_actor_id"] = instagram_actor_id

    endpoint = f"{account_id}/adcreatives"

    try:
        data = await make_api_request(endpoint, access_token, creative_data, method="POST")

        if "id" in data:
            creative_id = data["id"]
            # Get full creative details
            detail_endpoint = f"{creative_id}"
            detail_params = {
                "fields": "id,name,status,thumbnail_url,image_url,image_hash,object_story_spec,link_url"
            }
            details = await make_api_request(detail_endpoint, access_token, detail_params)

            return {
                "success": True,
                "creative_id": creative_id,
                "details": details
            }

        return data

    except Exception as e:
        return {
            "error": {
                "message": "Failed to create creative",
                "details": str(e)
            }
        }


@mcp.tool()
@meta_api_tool
async def meta_update_creative(
    creative_id: str,
    access_token: Optional[str] = None,
    name: Optional[str] = None,
    message: Optional[str] = None,
    headline: Optional[str] = None,
    description: Optional[str] = None,
    call_to_action_type: Optional[str] = None
) -> dict:
    """Update an existing creative's content.

    Updates specified fields of a creative. Only provided parameters
    will be updated; others remain unchanged.

    Note: Some fields like image_hash cannot be updated. To change
    the image, create a new creative.

    Args:
        creative_id: Meta Ads creative ID (required).
        access_token: Meta API access token (uses cached token if not provided).
        name: New creative name.
        message: New ad copy/text.
        headline: New headline.
        description: New description.
        call_to_action_type: New CTA button type.

    Returns:
        Dictionary containing:
            - success: True if update was successful
            - creative_id: ID of the updated creative
            - details: Updated creative details

    Example:
        >>> result = await meta_update_creative(
        ...     creative_id="23842614006150185",
        ...     headline="70% Off - Extended!",
        ...     message="Sale extended through Sunday!"
        ... )
    """
    if not creative_id:
        return {"error": {"message": "creative_id is required"}}

    update_data = {}

    if name is not None:
        update_data["name"] = name

    # For updating link_data fields, we need to use object_story_spec
    link_data_updates = {}
    if message is not None:
        link_data_updates["message"] = message
    if headline is not None:
        link_data_updates["name"] = headline  # API uses "name" for headline
    if description is not None:
        link_data_updates["description"] = description
    if call_to_action_type is not None:
        link_data_updates["call_to_action"] = {"type": call_to_action_type}

    if link_data_updates:
        update_data["object_story_spec"] = {"link_data": link_data_updates}

    if not update_data:
        return {"error": {"message": "No update parameters provided"}}

    endpoint = f"{creative_id}"

    try:
        data = await make_api_request(endpoint, access_token, update_data, method="POST")

        if "success" in data or "id" in data:
            # Get updated details
            detail_params = {
                "fields": "id,name,status,thumbnail_url,image_url,image_hash,object_story_spec,link_url"
            }
            details = await make_api_request(endpoint, access_token, detail_params)

            return {
                "success": True,
                "creative_id": creative_id,
                "details": details
            }

        return data

    except Exception as e:
        return {
            "error": {
                "message": f"Failed to update creative {creative_id}",
                "details": str(e)
            }
        }
