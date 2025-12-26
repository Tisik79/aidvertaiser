"""Meta Ads Targeting Search Tools.

This module provides MCP tools for searching and discovering targeting options
for Meta Ads, including interests, behaviors, demographics, and geo locations.
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
async def meta_search_interests(
    query: str,
    access_token: Optional[str] = None,
    limit: int = 25
) -> dict:
    """Search for interest targeting options by keyword.

    Searches the Meta interest database to find interests that can be
    used for ad targeting. Returns interests with audience size estimates.

    Args:
        query: Search term for interests (e.g., "cooking", "travel", "fitness").
        access_token: Meta API access token (uses cached token if not provided).
        limit: Maximum number of results to return (default: 25).

    Returns:
        Dictionary containing:
            - data: List of interest objects with:
                - id: Interest ID (use this in targeting spec)
                - name: Interest name
                - audience_size: Estimated audience size
                - path: Category path (e.g., "Interests > Food and drink")
                - topic: Related topic

    Example:
        >>> interests = await meta_search_interests("organic food")
        >>> for interest in interests["data"]:
        ...     print(f"{interest['name']} (ID: {interest['id']}, Size: {interest.get('audience_size', 'N/A')})")
    """
    if not query:
        return {"error": {"message": "query is required"}}

    endpoint = "search"
    params = {
        "type": "adinterest",
        "q": query,
        "limit": limit
    }

    data = await make_api_request(endpoint, access_token, params)
    return data


@mcp.tool()
@meta_api_tool
async def meta_get_interest_suggestions(
    interest_list: List[str],
    access_token: Optional[str] = None,
    limit: int = 25
) -> dict:
    """Get interest suggestions based on existing interests.

    Returns related interests that are similar to the provided interests.
    Useful for expanding targeting to related audiences.

    Args:
        interest_list: List of interest names to get suggestions for
            (e.g., ["Basketball", "Soccer", "Tennis"]).
        access_token: Meta API access token (uses cached token if not provided).
        limit: Maximum number of suggestions to return (default: 25).

    Returns:
        Dictionary containing:
            - data: List of suggested interest objects with:
                - id: Interest ID
                - name: Interest name
                - audience_size: Estimated audience size
                - description: Interest description

    Example:
        >>> suggestions = await meta_get_interest_suggestions(["Running", "Marathon"])
        >>> for interest in suggestions["data"]:
        ...     print(f"Suggested: {interest['name']}")
    """
    if not interest_list:
        return {"error": {"message": "interest_list is required"}}

    endpoint = "search"
    params = {
        "type": "adinterestsuggestion",
        "interest_list": json.dumps(interest_list),
        "limit": limit
    }

    data = await make_api_request(endpoint, access_token, params)
    return data


@mcp.tool()
@meta_api_tool
async def meta_search_geo_locations(
    query: str,
    access_token: Optional[str] = None,
    location_types: Optional[List[str]] = None,
    limit: int = 25
) -> dict:
    """Search for geographic targeting locations.

    Searches for countries, regions, cities, postal codes, and other
    geographic locations that can be used for ad targeting.

    Args:
        query: Search term for locations (e.g., "New York", "California", "Japan").
        access_token: Meta API access token (uses cached token if not provided).
        location_types: Types of locations to search. Options:
            - country: Countries
            - region: States/provinces
            - city: Cities
            - zip: Postal codes
            - geo_market: Designated Market Areas (DMAs)
            - electoral_district: Electoral districts
            If not specified, searches all types.
        limit: Maximum number of results to return (default: 25).

    Returns:
        Dictionary containing:
            - data: List of location objects with:
                - key: Location key (use this in targeting spec)
                - name: Location name
                - type: Location type
                - country_code: Country code
                - region: Parent region (if applicable)
                - supports_region: Whether region targeting is supported
                - supports_city: Whether city targeting is supported

    Example:
        >>> locations = await meta_search_geo_locations("New York", location_types=["city"])
        >>> for loc in locations["data"]:
        ...     print(f"{loc['name']} ({loc['type']}): key={loc['key']}")
    """
    if not query:
        return {"error": {"message": "query is required"}}

    endpoint = "search"
    params = {
        "type": "adgeolocation",
        "q": query,
        "limit": limit
    }

    if location_types:
        params["location_types"] = json.dumps(location_types)

    data = await make_api_request(endpoint, access_token, params)
    return data


@mcp.tool()
@meta_api_tool
async def meta_search_behaviors(
    access_token: Optional[str] = None,
    limit: int = 50
) -> dict:
    """Get available behavior targeting options.

    Returns all behavior targeting categories that can be used to
    target users based on their behaviors and activities.

    Args:
        access_token: Meta API access token (uses cached token if not provided).
        limit: Maximum number of results to return (default: 50).

    Returns:
        Dictionary containing:
            - data: List of behavior objects with:
                - id: Behavior ID (use this in targeting spec)
                - name: Behavior name
                - audience_size_lower_bound: Minimum audience size
                - audience_size_upper_bound: Maximum audience size
                - path: Category path
                - description: Behavior description

    Example:
        >>> behaviors = await meta_search_behaviors()
        >>> for behavior in behaviors["data"]:
        ...     print(f"{behavior['name']}: {behavior.get('description', 'N/A')}")
    """
    endpoint = "search"
    params = {
        "type": "adTargetingCategory",
        "class": "behaviors",
        "limit": limit
    }

    data = await make_api_request(endpoint, access_token, params)
    return data


@mcp.tool()
@meta_api_tool
async def meta_estimate_audience_size(
    account_id: str,
    targeting: Dict[str, Any],
    access_token: Optional[str] = None,
    optimization_goal: str = "REACH"
) -> dict:
    """Estimate audience size for targeting specifications.

    Uses Meta's reach estimate API to calculate the potential audience
    size for a given targeting configuration.

    Args:
        account_id: Meta Ads account ID (format: act_XXXXXXXXX).
        targeting: Complete targeting specification. Example:
            {
                "age_min": 25,
                "age_max": 65,
                "genders": [1, 2],  # 1=Male, 2=Female
                "geo_locations": {
                    "countries": ["US"],
                    "regions": [{"key": "3847"}],  # California
                    "cities": [{"key": "2420379"}]  # San Francisco
                },
                "flexible_spec": [
                    {"interests": [{"id": "6003139266461", "name": "Fitness"}]}
                ],
                "targeting_automation": {"advantage_audience": 1}  # Enable Advantage+
            }
        access_token: Meta API access token (uses cached token if not provided).
        optimization_goal: Optimization goal for estimation. Options:
            - REACH: Maximize reach
            - LINK_CLICKS: Click optimization
            - IMPRESSIONS: Impression optimization
            - CONVERSIONS: Conversion optimization

    Returns:
        Dictionary containing:
            - success: True if estimation succeeded
            - estimated_audience_size: Midpoint estimate
            - estimate_details:
                - users_lower_bound: Minimum audience size
                - users_upper_bound: Maximum audience size
                - estimate_ready: Whether estimate is ready
            - targeting: The targeting spec used
            - account_id: Account used for estimation

    Example:
        >>> estimate = await meta_estimate_audience_size(
        ...     account_id="act_123456789",
        ...     targeting={
        ...         "age_min": 25,
        ...         "age_max": 45,
        ...         "geo_locations": {"countries": ["US"]},
        ...         "flexible_spec": [
        ...             {"interests": [{"id": "6003139266461", "name": "Fitness"}]}
        ...         ]
        ...     }
        ... )
        >>> print(f"Estimated reach: {estimate['estimated_audience_size']:,}")
    """
    if not account_id:
        return {"error": {"message": "account_id is required"}}
    if not targeting:
        return {
            "error": {
                "message": "targeting is required",
                "example": {
                    "age_min": 25,
                    "age_max": 65,
                    "geo_locations": {"countries": ["US"]},
                    "flexible_spec": [
                        {"interests": [{"id": "6003139266461"}]}
                    ]
                }
            }
        }

    account_id = ensure_account_prefix(account_id)

    # Validate that targeting has at least one location or custom audience
    geo = targeting.get("geo_locations", {})
    has_location = any(
        isinstance(geo.get(k), list) and len(geo.get(k)) > 0
        for k in ["countries", "regions", "cities", "zips", "geo_markets", "country_groups"]
    )
    has_custom_audience = bool(targeting.get("custom_audiences"))

    if not has_location and not has_custom_audience:
        return {
            "error": {
                "message": "Missing target audience location",
                "details": "Add geo_locations with countries/regions/cities or include custom_audiences",
                "example": {
                    "geo_locations": {"countries": ["US"]},
                    "age_min": 25,
                    "age_max": 65
                }
            }
        }

    endpoint = f"{account_id}/reachestimate"
    params = {
        "targeting_spec": targeting
    }

    try:
        data = await make_api_request(endpoint, access_token, params, method="GET")

        if "error" in data:
            return data

        # Format the response
        if "data" in data:
            response_data = data["data"]

            # Handle dict structure with bounds
            if isinstance(response_data, dict):
                lower = response_data.get("users_lower_bound")
                upper = response_data.get("users_upper_bound")
                estimate_ready = response_data.get("estimate_ready")

                midpoint = None
                if isinstance(lower, (int, float)) and isinstance(upper, (int, float)):
                    midpoint = int((lower + upper) / 2)

                return {
                    "success": True,
                    "account_id": account_id,
                    "targeting": targeting,
                    "optimization_goal": optimization_goal,
                    "estimated_audience_size": midpoint or 0,
                    "estimate_details": {
                        "users_lower_bound": lower,
                        "users_upper_bound": upper,
                        "estimate_ready": estimate_ready
                    }
                }

            # Handle list structure
            if isinstance(response_data, list) and len(response_data) > 0:
                estimate_data = response_data[0]
                return {
                    "success": True,
                    "account_id": account_id,
                    "targeting": targeting,
                    "optimization_goal": optimization_goal,
                    "estimated_audience_size": estimate_data.get("estimate_mau", 0),
                    "estimate_details": {
                        "monthly_active_users": estimate_data.get("estimate_mau", 0),
                        "daily_outcomes_curve": estimate_data.get("estimate_dau", []),
                        "unsupported_targeting": estimate_data.get("unsupported_targeting", [])
                    }
                }

        return {
            "error": {
                "message": "No estimation data returned from Meta API",
                "raw_response": data
            }
        }

    except Exception as e:
        return {
            "error": {
                "message": f"Failed to get audience estimation: {str(e)}",
                "details": "Check targeting parameters and account permissions"
            }
        }
