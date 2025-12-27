"""Tests for Meta Ads campaign management.

These tests simulate MCP requests by calling the underlying Python functions
directly, verifying campaign creation, listing, updating, and ad set management.
"""

import asyncio
import pytest
import time


# Import the Meta Ads functions and access the underlying async functions via .fn
from unified_ads_mcp.meta.campaigns import (
    meta_list_accounts as _meta_list_accounts,
    meta_get_account_info as _meta_get_account_info,
    meta_list_campaigns as _meta_list_campaigns,
    meta_get_campaign_details as _meta_get_campaign_details,
    meta_create_campaign as _meta_create_campaign,
    meta_update_campaign as _meta_update_campaign,
)
from unified_ads_mcp.meta.adsets import (
    meta_list_adsets as _meta_list_adsets,
    meta_get_adset_details as _meta_get_adset_details,
    meta_create_adset as _meta_create_adset,
    meta_update_adset as _meta_update_adset,
)
from unified_ads_mcp.meta.ads import (
    meta_list_ads as _meta_list_ads,
    meta_get_ad_details as _meta_get_ad_details,
    meta_create_ad as _meta_create_ad,
    meta_update_ad as _meta_update_ad,
    meta_get_ad_creatives as _meta_get_ad_creatives,
)

# Access the underlying async functions (.fn) from FunctionTool objects
meta_list_accounts = _meta_list_accounts.fn
meta_get_account_info = _meta_get_account_info.fn
meta_list_campaigns = _meta_list_campaigns.fn
meta_get_campaign_details = _meta_get_campaign_details.fn
meta_create_campaign = _meta_create_campaign.fn
meta_update_campaign = _meta_update_campaign.fn
meta_list_adsets = _meta_list_adsets.fn
meta_get_adset_details = _meta_get_adset_details.fn
meta_create_adset = _meta_create_adset.fn
meta_update_adset = _meta_update_adset.fn
meta_list_ads = _meta_list_ads.fn
meta_get_ad_details = _meta_get_ad_details.fn
meta_create_ad = _meta_create_ad.fn
meta_update_ad = _meta_update_ad.fn
meta_get_ad_creatives = _meta_get_ad_creatives.fn


@pytest.fixture(scope="module")
def event_loop():
    """Create an event loop for the test module."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


class TestAccountListing:
    """Test account listing and info retrieval."""

    @pytest.mark.asyncio
    async def test_list_accounts(self, meta_access_token):
        """Test listing accessible ad accounts."""
        result = await meta_list_accounts(access_token=meta_access_token)

        assert "error" not in result
        assert "data" in result

        accounts = result["data"]
        print(f"\nFound {len(accounts)} accessible accounts")

        for acc in accounts[:5]:
            print(f"  - {acc.get('name')} ({acc.get('id')})")

    @pytest.mark.asyncio
    async def test_get_account_info(self, meta_access_token, meta_account_id):
        """Test getting account details."""
        result = await meta_get_account_info(
            account_id=meta_account_id,
            access_token=meta_access_token
        )

        assert "error" not in result
        assert "id" in result
        assert result["id"] == meta_account_id

        print(f"\nAccount: {result.get('name')}")
        print(f"  Currency: {result.get('currency')}")
        print(f"  Status: {result.get('account_status')}")


class TestCampaignListing:
    """Test campaign listing and filtering."""

    @pytest.mark.asyncio
    async def test_list_all_campaigns(self, meta_access_token, meta_account_id):
        """Test listing all campaigns."""
        result = await meta_list_campaigns(
            account_id=meta_account_id,
            access_token=meta_access_token,
            limit=50
        )

        assert "error" not in result
        assert "data" in result

        campaigns = result["data"]
        print(f"\nFound {len(campaigns)} campaigns")

        for camp in campaigns[:10]:
            print(f"  - {camp.get('name')} ({camp.get('status')})")

    @pytest.mark.asyncio
    async def test_list_paused_campaigns(self, meta_access_token, meta_account_id):
        """Test filtering campaigns by status."""
        result = await meta_list_campaigns(
            account_id=meta_account_id,
            access_token=meta_access_token,
            status="PAUSED"
        )

        assert "error" not in result
        assert "data" in result

        campaigns = result["data"]
        print(f"\nFound {len(campaigns)} PAUSED campaigns")

        # Verify all are PAUSED
        for camp in campaigns:
            assert camp.get("effective_status") == "PAUSED" or camp.get("status") == "PAUSED"


class TestCampaignCreation:
    """Test campaign creation with various configurations."""

    @pytest.mark.asyncio
    async def test_create_traffic_campaign(self, meta_access_token, meta_account_id, test_entities):
        """Test creating a traffic campaign."""
        timestamp = int(time.time())
        campaign_name = f"Test Traffic Campaign {timestamp}"

        result = await meta_create_campaign(
            name=campaign_name,
            objective="OUTCOME_TRAFFIC",
            account_id=meta_account_id,
            access_token=meta_access_token,
            status="PAUSED",
            daily_budget=50000  # 500 CZK/day (Meta minimum is ~50 CZK)
        )

        assert "error" not in result, f"Failed to create campaign: {result}"
        assert "id" in result

        campaign_id = result["id"]
        test_entities["campaigns"].append(campaign_id)

        print(f"\nCreated traffic campaign: {campaign_id}")

        # Verify campaign details
        details = await meta_get_campaign_details(
            campaign_id=campaign_id,
            access_token=meta_access_token
        )

        assert details.get("name") == campaign_name
        assert details.get("objective") == "OUTCOME_TRAFFIC"
        assert details.get("status") == "PAUSED"

    @pytest.mark.asyncio
    async def test_create_leads_campaign(self, meta_access_token, meta_account_id, test_entities):
        """Test creating a leads campaign."""
        timestamp = int(time.time())
        campaign_name = f"Test Leads Campaign {timestamp}"

        result = await meta_create_campaign(
            name=campaign_name,
            objective="OUTCOME_LEADS",
            account_id=meta_account_id,
            access_token=meta_access_token,
            status="PAUSED",
            daily_budget=50000,  # 500 CZK/day
            bid_strategy="LOWEST_COST_WITHOUT_CAP"
        )

        assert "error" not in result, f"Failed to create campaign: {result}"
        assert "id" in result

        campaign_id = result["id"]
        test_entities["campaigns"].append(campaign_id)

        print(f"\nCreated leads campaign: {campaign_id}")

    @pytest.mark.asyncio
    async def test_update_campaign(self, meta_access_token, test_entities):
        """Test updating campaign settings."""
        if not test_entities["campaigns"]:
            pytest.skip("No test campaign available")

        campaign_id = test_entities["campaigns"][0]

        # Update name
        new_name = f"Updated Test Campaign {int(time.time())}"
        result = await meta_update_campaign(
            campaign_id=campaign_id,
            access_token=meta_access_token,
            name=new_name
        )

        assert "error" not in result, f"Failed to update campaign: {result}"

        # Verify update
        details = await meta_get_campaign_details(
            campaign_id=campaign_id,
            access_token=meta_access_token
        )

        assert details.get("name") == new_name
        print(f"\nUpdated campaign name to: {new_name}")


class TestAdSetManagement:
    """Test ad set creation and management."""

    @pytest.mark.asyncio
    async def test_list_adsets(self, meta_access_token, meta_account_id):
        """Test listing ad sets."""
        result = await meta_list_adsets(
            account_id=meta_account_id,
            access_token=meta_access_token,
            limit=25
        )

        assert "error" not in result
        assert "data" in result

        adsets = result["data"]
        print(f"\nFound {len(adsets)} ad sets")

        for adset in adsets[:5]:
            print(f"  - {adset.get('name')} ({adset.get('status')})")

    @pytest.mark.asyncio
    async def test_create_adset(self, meta_access_token, meta_account_id, test_entities):
        """Test creating an ad set with targeting."""
        if not test_entities["campaigns"]:
            pytest.skip("No test campaign available")

        campaign_id = test_entities["campaigns"][0]
        timestamp = int(time.time())

        # Create ad set with Advantage+ targeting
        # Need bid_amount for campaigns with bid cap strategy
        result = await meta_create_adset(
            campaign_id=campaign_id,
            name=f"Test Ad Set {timestamp}",
            optimization_goal="LINK_CLICKS",
            billing_event="IMPRESSIONS",
            targeting={
                "age_min": 18,
                "age_max": 65,
                "geo_locations": {"countries": ["CZ"]},
                "targeting_automation": {"advantage_audience": 1}
            },
            account_id=meta_account_id,
            access_token=meta_access_token,
            status="PAUSED",
            bid_amount=500  # 5 CZK bid cap
        )

        assert "error" not in result, f"Failed to create ad set: {result}"
        assert "id" in result

        adset_id = result["id"]
        test_entities["adsets"].append(adset_id)

        print(f"\nCreated ad set: {adset_id}")

        # Verify details
        details = await meta_get_adset_details(
            adset_id=adset_id,
            access_token=meta_access_token
        )

        assert details.get("status") == "PAUSED"
        print(f"  Targeting: {details.get('targeting')}")


class TestAdManagement:
    """Test ad listing and details."""

    @pytest.mark.asyncio
    async def test_list_ads(self, meta_access_token, meta_account_id):
        """Test listing ads."""
        result = await meta_list_ads(
            account_id=meta_account_id,
            access_token=meta_access_token,
            limit=25
        )

        assert "error" not in result
        assert "data" in result

        ads = result["data"]
        print(f"\nFound {len(ads)} ads")

        for ad in ads[:5]:
            print(f"  - {ad.get('name')} ({ad.get('status')})")

    @pytest.mark.asyncio
    async def test_get_ad_creatives(self, meta_access_token, meta_account_id):
        """Test getting ad creatives."""
        # First get an ad
        ads_result = await meta_list_ads(
            account_id=meta_account_id,
            access_token=meta_access_token,
            limit=5
        )

        if not ads_result.get("data"):
            pytest.skip("No ads available")

        ad_id = ads_result["data"][0]["id"]

        result = await meta_get_ad_creatives(
            ad_id=ad_id,
            access_token=meta_access_token
        )

        assert "error" not in result
        print(f"\nCreatives for ad {ad_id}:")
        if "data" in result:
            for creative in result["data"]:
                print(f"  - {creative.get('id')}: {creative.get('name')}")


class TestCampaignCleanup:
    """Cleanup test campaigns at the end."""

    @pytest.mark.asyncio
    async def test_delete_test_campaigns(self, meta_access_token, test_entities):
        """Delete test campaigns (set status to DELETED)."""
        for campaign_id in test_entities.get("campaigns", []):
            result = await meta_update_campaign(
                campaign_id=campaign_id,
                access_token=meta_access_token,
                status="DELETED"
            )

            if "error" not in result:
                print(f"\nDeleted campaign: {campaign_id}")
            else:
                print(f"\nFailed to delete campaign {campaign_id}: {result}")
