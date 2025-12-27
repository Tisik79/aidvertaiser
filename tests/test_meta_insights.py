"""Tests for Meta Ads insights, reporting, and targeting.

These tests verify performance data retrieval, targeting search,
and audience estimation functionality.
"""

import asyncio
import pytest


# Import the Meta Ads functions and access underlying async functions via .fn
from unified_ads_mcp.meta.insights import (
    meta_get_insights as _meta_get_insights,
    meta_get_login_link as _meta_get_login_link,
)
from unified_ads_mcp.meta.targeting import (
    meta_search_interests as _meta_search_interests,
    meta_get_interest_suggestions as _meta_get_interest_suggestions,
    meta_search_geo_locations as _meta_search_geo_locations,
    meta_search_behaviors as _meta_search_behaviors,
    meta_estimate_audience_size as _meta_estimate_audience_size,
)
from unified_ads_mcp.meta.campaigns import (
    meta_list_campaigns as _meta_list_campaigns,
)

# Access the underlying async functions (.fn) from FunctionTool objects
meta_get_insights = _meta_get_insights.fn
meta_get_login_link = _meta_get_login_link.fn
meta_search_interests = _meta_search_interests.fn
meta_get_interest_suggestions = _meta_get_interest_suggestions.fn
meta_search_geo_locations = _meta_search_geo_locations.fn
meta_search_behaviors = _meta_search_behaviors.fn
meta_estimate_audience_size = _meta_estimate_audience_size.fn
meta_list_campaigns = _meta_list_campaigns.fn


@pytest.fixture(scope="module")
def event_loop():
    """Create an event loop for the test module."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


class TestInsights:
    """Test performance insights retrieval."""

    @pytest.mark.asyncio
    async def test_get_account_insights(self, meta_access_token, meta_account_id):
        """Test getting account-level insights."""
        result = await meta_get_insights(
            object_id=meta_account_id,
            access_token=meta_access_token,
            time_range="last_30d",
            level="account"
        )

        assert "error" not in result, f"Insights failed: {result}"

        if "data" in result and result["data"]:
            data = result["data"][0]
            print(f"\nAccount Insights (Last 30 Days):")
            print(f"  Impressions: {data.get('impressions', 'N/A')}")
            print(f"  Clicks: {data.get('clicks', 'N/A')}")
            print(f"  Spend: {data.get('spend', 'N/A')}")
            print(f"  CTR: {data.get('ctr', 'N/A')}")
        else:
            print("\nNo insights data available")

    @pytest.mark.asyncio
    async def test_get_campaign_insights(self, meta_access_token, meta_account_id):
        """Test getting campaign-level insights."""
        # First get a campaign
        campaigns = await meta_list_campaigns(
            account_id=meta_account_id,
            access_token=meta_access_token,
            limit=1
        )

        if not campaigns.get("data"):
            pytest.skip("No campaigns available")

        campaign_id = campaigns["data"][0]["id"]

        result = await meta_get_insights(
            object_id=campaign_id,
            access_token=meta_access_token,
            time_range="last_7d",
            level="campaign"
        )

        assert "error" not in result, f"Insights failed: {result}"

        print(f"\nCampaign Insights for {campaign_id}:")
        if "data" in result and result["data"]:
            for row in result["data"][:3]:
                print(f"  Spend: {row.get('spend', 'N/A')}, Clicks: {row.get('clicks', 'N/A')}")

    @pytest.mark.asyncio
    async def test_get_insights_with_breakdown(self, meta_access_token, meta_account_id):
        """Test getting insights with age breakdown."""
        result = await meta_get_insights(
            object_id=meta_account_id,
            access_token=meta_access_token,
            time_range="last_30d",
            level="account",
            breakdown="age"
        )

        assert "error" not in result, f"Insights failed: {result}"

        print(f"\nAccount Insights by Age:")
        if "data" in result:
            for row in result["data"][:5]:
                print(f"  Age {row.get('age', 'N/A')}: {row.get('impressions', 0)} impressions")

    @pytest.mark.asyncio
    async def test_get_insights_custom_date_range(self, meta_access_token, meta_account_id):
        """Test getting insights with custom date range."""
        result = await meta_get_insights(
            object_id=meta_account_id,
            access_token=meta_access_token,
            time_range={"since": "2024-01-01", "until": "2024-12-31"},
            level="account"
        )

        assert "error" not in result, f"Insights failed: {result}"

        print(f"\nAccount Insights (2024):")
        if "data" in result and result["data"]:
            data = result["data"][0]
            print(f"  Total Spend: {data.get('spend', 'N/A')}")
            print(f"  Total Impressions: {data.get('impressions', 'N/A')}")


class TestInterestSearch:
    """Test interest targeting search."""

    @pytest.mark.asyncio
    async def test_search_interests(self, meta_access_token):
        """Test searching for interests."""
        result = await meta_search_interests(
            query="fitness",
            access_token=meta_access_token,
            limit=10
        )

        assert "error" not in result, f"Search failed: {result}"
        assert "data" in result

        interests = result["data"]
        print(f"\nFound {len(interests)} interests for 'fitness':")
        for interest in interests[:5]:
            print(f"  - {interest.get('name')} (ID: {interest.get('id')})")

    @pytest.mark.asyncio
    async def test_search_interests_food(self, meta_access_token):
        """Test searching for food-related interests."""
        result = await meta_search_interests(
            query="cooking",
            access_token=meta_access_token,
            limit=10
        )

        assert "error" not in result
        assert "data" in result

        interests = result["data"]
        print(f"\nFound {len(interests)} interests for 'cooking':")
        for interest in interests[:5]:
            print(f"  - {interest.get('name')}")

    @pytest.mark.asyncio
    async def test_get_interest_suggestions(self, meta_access_token):
        """Test getting interest suggestions."""
        result = await meta_get_interest_suggestions(
            interest_list=["Running", "Marathon", "Fitness"],
            access_token=meta_access_token,
            limit=10
        )

        assert "error" not in result, f"Suggestions failed: {result}"

        if "data" in result:
            suggestions = result["data"]
            print(f"\nSuggested interests based on Running/Marathon/Fitness:")
            for suggestion in suggestions[:5]:
                print(f"  - {suggestion.get('name')}")


class TestGeoSearch:
    """Test geographic location search."""

    @pytest.mark.asyncio
    async def test_search_countries(self, meta_access_token):
        """Test searching for countries."""
        result = await meta_search_geo_locations(
            query="Czech",
            access_token=meta_access_token,
            location_types=["country"]
        )

        assert "error" not in result, f"Search failed: {result}"
        assert "data" in result

        locations = result["data"]
        print(f"\nFound {len(locations)} locations for 'Czech':")
        for loc in locations[:5]:
            print(f"  - {loc.get('name')} ({loc.get('type')}): key={loc.get('key')}")

    @pytest.mark.asyncio
    async def test_search_cities(self, meta_access_token):
        """Test searching for cities."""
        result = await meta_search_geo_locations(
            query="Prague",
            access_token=meta_access_token,
            location_types=["city"]
        )

        assert "error" not in result
        assert "data" in result

        locations = result["data"]
        print(f"\nFound {len(locations)} cities for 'Prague':")
        for loc in locations[:5]:
            print(f"  - {loc.get('name')} ({loc.get('country_code')})")

    @pytest.mark.asyncio
    async def test_search_all_location_types(self, meta_access_token):
        """Test searching without location type filter."""
        result = await meta_search_geo_locations(
            query="New York",
            access_token=meta_access_token
        )

        assert "error" not in result
        assert "data" in result

        locations = result["data"]
        print(f"\nFound {len(locations)} locations for 'New York':")
        for loc in locations[:5]:
            print(f"  - {loc.get('name')} ({loc.get('type')})")


class TestBehaviorSearch:
    """Test behavior targeting search."""

    @pytest.mark.asyncio
    async def test_search_behaviors(self, meta_access_token):
        """Test getting available behaviors."""
        result = await meta_search_behaviors(
            access_token=meta_access_token,
            limit=20
        )

        assert "error" not in result, f"Search failed: {result}"
        assert "data" in result

        behaviors = result["data"]
        print(f"\nFound {len(behaviors)} behaviors:")
        for behavior in behaviors[:10]:
            print(f"  - {behavior.get('name')}")


class TestAudienceEstimation:
    """Test audience size estimation."""

    @pytest.mark.asyncio
    async def test_estimate_audience_czech(self, meta_access_token, meta_account_id):
        """Test audience estimation for Czech Republic."""
        result = await meta_estimate_audience_size(
            targeting={
                "age_min": 25,
                "age_max": 55,
                "geo_locations": {"countries": ["CZ"]}
            },
            account_id=meta_account_id,
            access_token=meta_access_token
        )

        assert "error" not in result, f"Estimation failed: {result}"

        print(f"\nAudience Estimate (CZ, 25-55):")
        print(f"  Estimated Size: {result.get('estimated_audience_size', 'N/A'):,}")
        if "estimate_details" in result:
            details = result["estimate_details"]
            print(f"  Lower Bound: {details.get('users_lower_bound', 'N/A'):,}")
            print(f"  Upper Bound: {details.get('users_upper_bound', 'N/A'):,}")

    @pytest.mark.asyncio
    async def test_estimate_audience_with_interests(self, meta_access_token, meta_account_id):
        """Test audience estimation with interest targeting."""
        # First find a fitness interest
        interests = await meta_search_interests(
            query="fitness",
            access_token=meta_access_token,
            limit=1
        )

        if not interests.get("data"):
            pytest.skip("No interests found")

        interest = interests["data"][0]

        result = await meta_estimate_audience_size(
            targeting={
                "age_min": 18,
                "age_max": 45,
                "geo_locations": {"countries": ["CZ"]},
                "flexible_spec": [
                    {"interests": [{"id": interest["id"], "name": interest["name"]}]}
                ]
            },
            account_id=meta_account_id,
            access_token=meta_access_token
        )

        assert "error" not in result, f"Estimation failed: {result}"

        print(f"\nAudience Estimate (CZ, 18-45, {interest['name']}):")
        print(f"  Estimated Size: {result.get('estimated_audience_size', 'N/A'):,}")

    @pytest.mark.asyncio
    async def test_estimate_audience_missing_location(self, meta_access_token, meta_account_id):
        """Test that missing location returns error."""
        result = await meta_estimate_audience_size(
            targeting={
                "age_min": 25,
                "age_max": 55
                # Missing geo_locations
            },
            account_id=meta_account_id,
            access_token=meta_access_token
        )

        assert "error" in result
        assert "location" in result["error"]["message"].lower()


class TestLoginLink:
    """Test login link generation."""

    @pytest.mark.asyncio
    async def test_get_login_link(self, meta_access_token):
        """Test getting login link."""
        result = await meta_get_login_link(access_token=meta_access_token)

        # This may return error if META_APP_ID is not set
        if "error" in result:
            print(f"\nLogin link requires META_APP_ID: {result['error']['message']}")
        else:
            print(f"\nLogin URL: {result.get('auth_url', 'N/A')[:80]}...")
            print(f"  Scopes: {result.get('scopes_requested', [])}")
