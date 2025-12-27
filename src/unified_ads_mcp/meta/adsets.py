"""Meta Ads AdSet Management Tools.

This module provides MCP tools for managing Meta Ads ad sets, including
listing, creating, updating, and retrieving ad set details.
"""

import json
from typing import Optional, List, Dict, Any

from ..server import mcp
from .client import (
    make_api_request,
    meta_api_tool,
    ensure_account_prefix,
    get_default_account_id,
)


@mcp.tool()
@meta_api_tool
async def meta_list_adsets(
    account_id: Optional[str] = None,
    access_token: Optional[str] = None,
    campaign_id: Optional[str] = None,
    limit: int = 25,
    after: Optional[str] = None
) -> dict:
    """List ad sets for a Meta Ads account with optional campaign filtering.

    Retrieves ad sets with their configuration including targeting,
    budgets, optimization goals, and billing information.

    Args:
        account_id: Meta Ads account ID (format: act_XXXXXXXXX).
            Uses default from config if not provided.
        access_token: Meta API access token (uses cached token if not provided).
        campaign_id: Optional campaign ID to filter ad sets by campaign.
        limit: Maximum number of ad sets to return (default: 25).
        after: Pagination cursor for next page of results.

    Returns:
        Dictionary containing:
            - data: List of ad set objects with id, name, targeting, etc.
            - paging: Pagination cursors for navigating results.

    Example:
        >>> adsets = await meta_list_adsets("act_123456789", campaign_id="23842588888640185")
        >>> for adset in adsets["data"]:
        ...     print(f"{adset['name']}: {adset['optimization_goal']}")
    """
    account_id = account_id or get_default_account_id()
    if not account_id:
        return {"error": {"message": "account_id is required - configure default_account_id in meta-ads.yaml"}}

    account_id = ensure_account_prefix(account_id)

    # Use campaign endpoint if campaign_id provided, otherwise account endpoint
    if campaign_id:
        endpoint = f"{campaign_id}/adsets"
    else:
        endpoint = f"{account_id}/adsets"

    params = {
        "fields": "id,name,campaign_id,status,effective_status,daily_budget,lifetime_budget,targeting,bid_amount,bid_strategy,optimization_goal,billing_event,start_time,end_time,created_time,updated_time,is_dynamic_creative,frequency_control_specs",
        "limit": limit
    }

    if after:
        params["after"] = after

    data = await make_api_request(endpoint, access_token, params)
    return data


@mcp.tool()
@meta_api_tool
async def meta_get_adset_details(
    adset_id: str,
    access_token: Optional[str] = None
) -> dict:
    """Get detailed information about a specific ad set.

    Retrieves comprehensive ad set details including targeting specifications,
    budgets, optimization goals, and frequency controls.

    Args:
        adset_id: Meta Ads ad set ID.
        access_token: Meta API access token (uses cached token if not provided).

    Returns:
        Dictionary containing ad set details:
            - id: Ad set ID
            - name: Ad set name
            - campaign_id: Parent campaign ID
            - status: Ad set status
            - targeting: Detailed targeting specification
            - optimization_goal: What the ad set is optimizing for
            - billing_event: How you're charged (IMPRESSIONS, LINK_CLICKS, etc.)
            - daily_budget/lifetime_budget: Budget configuration
            - frequency_control_specs: Frequency cap settings
            - destination_type: Where users are directed after clicking
            - promoted_object: Mobile app details if applicable

    Example:
        >>> details = await meta_get_adset_details("23842614006130185")
        >>> print(f"Targeting: {details['targeting']}")
    """
    if not adset_id:
        return {"error": {"message": "adset_id is required"}}

    endpoint = f"{adset_id}"
    params = {
        "fields": "id,name,campaign_id,status,effective_status,frequency_control_specs,daily_budget,lifetime_budget,targeting,bid_amount,bid_strategy,optimization_goal,billing_event,start_time,end_time,created_time,updated_time,attribution_spec,destination_type,promoted_object,pacing_type,budget_remaining,dsa_beneficiary,is_dynamic_creative"
    }

    data = await make_api_request(endpoint, access_token, params)

    # Add note if frequency_control_specs wasn't returned
    if "frequency_control_specs" not in data and "error" not in data:
        data["_meta"] = {
            "note": "No frequency_control_specs in response. Either no caps are set or API didn't include this field."
        }

    return data


@mcp.tool()
@meta_api_tool
async def meta_create_adset(
    campaign_id: str,
    name: str,
    optimization_goal: str,
    billing_event: str,
    targeting: Dict[str, Any],
    account_id: Optional[str] = None,
    access_token: Optional[str] = None,
    status: str = "PAUSED",
    daily_budget: Optional[int] = None,
    lifetime_budget: Optional[int] = None,
    bid_amount: Optional[int] = None,
    bid_strategy: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    destination_type: Optional[str] = None,
    promoted_object: Optional[Dict[str, Any]] = None,
    is_dynamic_creative: Optional[bool] = None
) -> dict:
    """Create a new ad set in a Meta Ads campaign.

    Creates an ad set with the specified targeting and optimization settings.
    New ad sets are created in PAUSED status by default for review.

    Args:
        campaign_id: Parent campaign ID (required).
        name: Ad set name (required).
        account_id: Meta Ads account ID (format: act_XXXXXXXXX).
            Uses default from config if not provided.
        optimization_goal: What to optimize for (required). Options:
            - LINK_CLICKS: Click optimization
            - REACH: Maximize reach
            - IMPRESSIONS: Maximize impressions
            - CONVERSIONS: Optimize for conversions
            - LANDING_PAGE_VIEWS: Optimize for landing page views
            - LEAD_GENERATION: Lead form submissions
            - APP_INSTALLS: App installation optimization
        billing_event: How you're charged (required). Options:
            - IMPRESSIONS: Pay per impression (CPM)
            - LINK_CLICKS: Pay per click (CPC)
            - APP_INSTALLS: Pay per install
        targeting: Targeting specification (required). Example:
            {
                "age_min": 25,
                "age_max": 65,
                "geo_locations": {"countries": ["US"]},
                "targeting_automation": {"advantage_audience": 1}
            }
        access_token: Meta API access token (uses cached token if not provided).
        status: Initial status (default: PAUSED).
        daily_budget: Daily budget in cents (e.g., 1000 = $10.00).
        lifetime_budget: Lifetime budget in cents.
        bid_amount: Bid amount in cents.
        bid_strategy: Bid strategy (e.g., 'LOWEST_COST', 'LOWEST_COST_WITH_BID_CAP').
        start_time: Start time in ISO 8601 format (e.g., '2025-01-15T12:00:00-0500').
        end_time: End time in ISO 8601 format.
        destination_type: Where users go after clicking. Options:
            - ON_AD: Interaction happens on the ad (leads)
            - APP_STORE: App store page
            - WEBSITE: Website destination
        promoted_object: Mobile app details for app campaigns:
            {"application_id": "123456", "object_store_url": "https://apps.apple.com/..."}
        is_dynamic_creative: Enable Dynamic Creative optimization.

    Returns:
        Dictionary containing:
            - id: Created ad set ID
            - success: True if created successfully

    Example:
        >>> result = await meta_create_adset(
        ...     account_id="act_123456789",
        ...     campaign_id="23842588888640185",
        ...     name="US Adults 25-55",
        ...     optimization_goal="LINK_CLICKS",
        ...     billing_event="IMPRESSIONS",
        ...     targeting={
        ...         "age_min": 25,
        ...         "age_max": 55,
        ...         "geo_locations": {"countries": ["US"]},
        ...         "genders": [1, 2]
        ...     },
        ...     daily_budget=2500  # $25/day
        ... )
    """
    account_id = account_id or get_default_account_id()
    if not account_id:
        return {"error": {"message": "account_id is required - configure default_account_id in meta-ads.yaml"}}
    if not campaign_id:
        return {"error": {"message": "campaign_id is required"}}
    if not name:
        return {"error": {"message": "name is required"}}
    if not optimization_goal:
        return {"error": {"message": "optimization_goal is required"}}
    if not billing_event:
        return {"error": {"message": "billing_event is required"}}
    if not targeting:
        return {"error": {"message": "targeting is required"}}

    account_id = ensure_account_prefix(account_id)

    # Validate mobile app campaigns
    if optimization_goal == "APP_INSTALLS":
        if not promoted_object:
            return {
                "error": {
                    "message": "promoted_object is required for APP_INSTALLS optimization",
                    "required_fields": ["application_id", "object_store_url"]
                }
            }
        if "application_id" not in promoted_object or "object_store_url" not in promoted_object:
            return {
                "error": {
                    "message": "promoted_object must include application_id and object_store_url",
                    "example": {
                        "application_id": "123456789012345",
                        "object_store_url": "https://apps.apple.com/app/id123456789"
                    }
                }
            }

    endpoint = f"{account_id}/adsets"

    params = {
        "name": name,
        "campaign_id": campaign_id,
        "status": status,
        "optimization_goal": optimization_goal,
        "billing_event": billing_event,
        "targeting": json.dumps(targeting)
    }

    if daily_budget is not None:
        params["daily_budget"] = str(daily_budget)

    if lifetime_budget is not None:
        params["lifetime_budget"] = str(lifetime_budget)

    if bid_amount is not None:
        params["bid_amount"] = str(bid_amount)

    if bid_strategy:
        params["bid_strategy"] = bid_strategy

    if start_time:
        params["start_time"] = start_time

    if end_time:
        params["end_time"] = end_time

    if destination_type:
        params["destination_type"] = destination_type

    if promoted_object:
        params["promoted_object"] = json.dumps(promoted_object)

    if is_dynamic_creative is not None:
        params["is_dynamic_creative"] = "true" if is_dynamic_creative else "false"

    try:
        data = await make_api_request(endpoint, access_token, params, method="POST")
        return data
    except Exception as e:
        return {
            "error": {
                "message": "Failed to create ad set",
                "details": str(e)
            }
        }


@mcp.tool()
@meta_api_tool
async def meta_update_adset(
    adset_id: str,
    access_token: Optional[str] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    daily_budget: Optional[int] = None,
    lifetime_budget: Optional[int] = None,
    targeting: Optional[Dict[str, Any]] = None,
    bid_amount: Optional[int] = None,
    bid_strategy: Optional[str] = None,
    optimization_goal: Optional[str] = None,
    frequency_control_specs: Optional[List[Dict[str, Any]]] = None,
    is_dynamic_creative: Optional[bool] = None
) -> dict:
    """Update an existing ad set's settings.

    Updates specified fields of an ad set. Only provided parameters
    will be updated; others remain unchanged.

    Args:
        adset_id: Meta Ads ad set ID (required).
        access_token: Meta API access token (uses cached token if not provided).
        name: New ad set name.
        status: New status. Options: ACTIVE, PAUSED, DELETED.
        daily_budget: New daily budget in cents.
        lifetime_budget: New lifetime budget in cents.
        targeting: New targeting specification (replaces existing).
        bid_amount: New bid amount in cents.
        bid_strategy: New bid strategy.
        optimization_goal: New optimization goal.
        frequency_control_specs: Frequency cap settings. Example:
            [{"event": "IMPRESSIONS", "interval_days": 7, "max_frequency": 3}]
        is_dynamic_creative: Enable/disable Dynamic Creative.

    Returns:
        Dictionary containing:
            - success: True if update was successful

    Example:
        >>> result = await meta_update_adset(
        ...     adset_id="23842614006130185",
        ...     status="ACTIVE",
        ...     daily_budget=5000,  # Increase to $50/day
        ...     frequency_control_specs=[{
        ...         "event": "IMPRESSIONS",
        ...         "interval_days": 7,
        ...         "max_frequency": 5
        ...     }]
        ... )
    """
    if not adset_id:
        return {"error": {"message": "adset_id is required"}}

    params = {}

    if name is not None:
        params["name"] = name

    if status is not None:
        params["status"] = status

    if daily_budget is not None:
        params["daily_budget"] = str(daily_budget)

    if lifetime_budget is not None:
        params["lifetime_budget"] = str(lifetime_budget)

    if targeting is not None:
        params["targeting"] = json.dumps(targeting) if isinstance(targeting, dict) else targeting

    if bid_amount is not None:
        params["bid_amount"] = str(bid_amount)

    if bid_strategy is not None:
        params["bid_strategy"] = bid_strategy

    if optimization_goal is not None:
        params["optimization_goal"] = optimization_goal

    if frequency_control_specs is not None:
        params["frequency_control_specs"] = frequency_control_specs

    if is_dynamic_creative is not None:
        params["is_dynamic_creative"] = "true" if is_dynamic_creative else "false"

    if not params:
        return {"error": {"message": "No update parameters provided"}}

    endpoint = f"{adset_id}"

    try:
        data = await make_api_request(endpoint, access_token, params, method="POST")
        return data
    except Exception as e:
        return {
            "error": {
                "message": f"Failed to update ad set {adset_id}",
                "details": str(e)
            }
        }
