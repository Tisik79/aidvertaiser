"""Meta Ads Insights and Reporting Tools.

This module provides MCP tools for retrieving performance insights and
reports from Meta Ads campaigns, ad sets, and ads.
"""

import os
import json
from typing import Optional, Union, Dict

from ..server import mcp
from .client import make_api_request, meta_api_tool


@mcp.tool()
@meta_api_tool
async def meta_get_insights(
    object_id: str,
    access_token: Optional[str] = None,
    time_range: Union[str, Dict[str, str]] = "last_30d",
    breakdown: Optional[str] = None,
    level: str = "ad",
    limit: int = 100,
    after: Optional[str] = None,
) -> dict:
    """Get performance insights for a campaign, ad set, ad, or account.

    Retrieves detailed performance metrics including impressions, clicks,
    spend, conversions, and other KPIs with optional breakdowns.

    Args:
        object_id: ID of the object to get insights for. Can be:
            - Account ID (act_XXXXXXXXX)
            - Campaign ID
            - Ad set ID
            - Ad ID
        access_token: Meta API access token (uses cached token if not provided).
        time_range: Time period for the report. Can be:
            - Preset string: 'today', 'yesterday', 'this_month', 'last_month',
              'this_quarter', 'last_quarter', 'maximum', 'last_3d', 'last_7d',
              'last_14d', 'last_28d', 'last_30d', 'last_90d'
            - Custom dict: {"since": "2025-01-01", "until": "2025-01-31"}
        breakdown: Optional breakdown dimension. Options include:
            - Demographic: 'age', 'gender', 'country', 'region', 'dma'
            - Platform: 'device_platform', 'platform_position', 'publisher_platform'
            - Creative: 'image_asset', 'video_asset', 'title_asset', 'body_asset'
            - Time: 'hourly_stats_aggregated_by_advertiser_time_zone'
        level: Aggregation level. Options: 'ad', 'adset', 'campaign', 'account'.
        limit: Maximum results per page (default: 100).
        after: Pagination cursor for next page.

    Returns:
        Dictionary containing:
            - data: List of insight objects with metrics:
                - impressions: Number of impressions
                - clicks: Number of clicks
                - spend: Amount spent
                - cpc: Cost per click
                - cpm: Cost per 1000 impressions
                - ctr: Click-through rate
                - reach: Unique users reached
                - frequency: Average impressions per user
                - actions: Conversion actions
                - conversions: Number of conversions
            - paging: Pagination cursors

    Example:
        >>> # Get last 7 days of campaign performance
        >>> insights = await meta_get_insights(
        ...     object_id="23842588888640185",
        ...     time_range="last_7d",
        ...     level="campaign"
        ... )
        >>> for row in insights["data"]:
        ...     print(f"Spend: ${float(row['spend']):.2f}, Clicks: {row['clicks']}")

        >>> # Get performance breakdown by age
        >>> insights = await meta_get_insights(
        ...     object_id="act_123456789",
        ...     time_range={"since": "2025-01-01", "until": "2025-01-31"},
        ...     breakdown="age",
        ...     level="account"
        ... )
    """
    if not object_id:
        return {"error": {"message": "object_id is required"}}

    endpoint = f"{object_id}/insights"
    params = {
        "fields": "account_id,account_name,campaign_id,campaign_name,adset_id,adset_name,ad_id,ad_name,impressions,clicks,spend,cpc,cpm,ctr,reach,frequency,actions,action_values,conversions,unique_clicks,cost_per_action_type,cost_per_conversion",
        "level": level,
        "limit": limit,
    }

    # Handle time range
    if isinstance(time_range, dict):
        if "since" in time_range and "until" in time_range:
            params["time_range"] = json.dumps(time_range)
        else:
            return {
                "error": {
                    "message": "Custom time_range must have 'since' and 'until' keys",
                    "example": {"since": "2025-01-01", "until": "2025-01-31"},
                }
            }
    else:
        params["date_preset"] = time_range

    if breakdown:
        params["breakdowns"] = breakdown

    if after:
        params["after"] = after

    data = await make_api_request(endpoint, access_token, params)
    return data


@mcp.tool()
@meta_api_tool
async def meta_get_login_link(access_token: Optional[str] = None) -> dict:
    """Get a login link for Meta Ads authentication.

    Returns the OAuth authentication URL for connecting to Meta Ads.
    Use this when you need to authenticate or re-authenticate.

    Args:
        access_token: Not used but included for consistency.

    Returns:
        Dictionary containing:
            - auth_url: OAuth login URL for Meta Ads
            - instructions: Steps to complete authentication
            - app_id_configured: Whether META_APP_ID is set

    Example:
        >>> result = await meta_get_login_link()
        >>> print(f"Login at: {result['auth_url']}")
    """
    app_id = os.environ.get("META_APP_ID", "")
    redirect_uri = os.environ.get(
        "META_REDIRECT_URI", "https://localhost:8080/callback"
    )

    if not app_id:
        return {
            "error": {
                "message": "META_APP_ID environment variable not set",
                "instructions": [
                    "1. Go to https://developers.facebook.com/apps/",
                    "2. Create or select an app",
                    "3. Copy the App ID",
                    "4. Set META_APP_ID environment variable",
                ],
            }
        }

    # Build OAuth URL
    scopes = [
        "ads_management",
        "ads_read",
        "business_management",
        "pages_read_engagement",
        "pages_show_list",
    ]

    auth_url = (
        f"https://www.facebook.com/v22.0/dialog/oauth"
        f"?client_id={app_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={','.join(scopes)}"
        f"&response_type=code"
    )

    return {
        "auth_url": auth_url,
        "app_id_configured": bool(app_id),
        "instructions": [
            "1. Click or open the auth_url in a browser",
            "2. Log in with your Facebook account",
            "3. Grant the requested permissions",
            "4. You will be redirected with an authorization code",
            "5. Exchange the code for an access token",
        ],
        "scopes_requested": scopes,
        "note": "After authentication, set META_ACCESS_TOKEN environment variable with your token",
    }
