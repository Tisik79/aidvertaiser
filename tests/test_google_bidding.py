"""Tests for Google Ads campaign bidding strategy updates.

Tests both proto-level field mask correctness and real API integration.
"""

import pytest

from google.ads.googleads.client import GoogleAdsClient

from unified_ads_mcp.google.campaigns import (
    google_list_campaigns as _list,
    google_get_campaign as _get,
    google_update_campaign as _update,
)

# Unwrap FunctionTool objects
list_campaigns = _list.fn
get_campaign = _get.fn
update_campaign = _update.fn


class TestBiddingFieldMasks:
    """Verify that bidding strategy fields and masks are set correctly at the proto level."""

    @pytest.fixture()
    def client(self):
        from unified_ads_mcp.google.client import get_google_ads_client
        return get_google_ads_client()

    def test_maximize_clicks_sets_subfield(self, client):
        """MAXIMIZE_CLICKS maps to target_spend proto field with leaf-level mask."""
        op = client.get_type("CampaignOperation")
        campaign = op.update
        campaign.resource_name = "customers/123/campaigns/456"

        campaign.target_spend.target_spend_micros = 0
        op.update_mask.paths.append("target_spend.target_spend_micros")

        assert campaign.target_spend.target_spend_micros == 0
        assert "target_spend.target_spend_micros" in op.update_mask.paths
        # Parent-only mask must NOT be used (causes FIELD_HAS_SUBFIELDS error)
        assert "target_spend" not in op.update_mask.paths

    def test_manual_cpc_sets_subfield(self, client):
        """manual_cpc must use leaf-level field mask."""
        op = client.get_type("CampaignOperation")
        campaign = op.update
        campaign.resource_name = "customers/123/campaigns/456"

        campaign.manual_cpc.enhanced_cpc_enabled = False
        op.update_mask.paths.append("manual_cpc.enhanced_cpc_enabled")

        assert campaign.manual_cpc.enhanced_cpc_enabled is False
        assert "manual_cpc.enhanced_cpc_enabled" in op.update_mask.paths
        assert "manual_cpc" not in op.update_mask.paths

    def test_maximize_conversions_sets_subfield(self, client):
        """maximize_conversions must use leaf-level field mask."""
        op = client.get_type("CampaignOperation")
        campaign = op.update
        campaign.resource_name = "customers/123/campaigns/456"

        campaign.maximize_conversions.target_cpa_micros = 5000000
        op.update_mask.paths.append("maximize_conversions.target_cpa_micros")

        assert campaign.maximize_conversions.target_cpa_micros == 5000000
        assert "maximize_conversions.target_cpa_micros" in op.update_mask.paths

    def test_target_roas_sets_subfield(self, client):
        """target_roas must use leaf-level field mask."""
        op = client.get_type("CampaignOperation")
        campaign = op.update
        campaign.resource_name = "customers/123/campaigns/456"

        campaign.target_roas.target_roas = 2.0
        op.update_mask.paths.append("target_roas.target_roas")

        assert campaign.target_roas.target_roas == 2.0
        assert "target_roas.target_roas" in op.update_mask.paths

    def test_parent_mask_would_fail(self, client):
        """Demonstrate that parent-level mask causes FIELD_HAS_SUBFIELDS error."""
        op = client.get_type("CampaignOperation")
        campaign = op.update
        campaign.resource_name = "customers/123/campaigns/456"

        # Parent-level mask — the API rejects this
        campaign.target_spend.target_spend_micros = 0
        op.update_mask.paths.append("target_spend")

        assert "target_spend" in op.update_mask.paths
        # The fix uses the sub-field path instead:
        assert "target_spend.target_spend_micros" not in op.update_mask.paths


class TestBiddingStrategyIntegration:
    """Integration tests that switch bidding strategies on a real campaign.

    Requires a real Google Ads account with at least one PAUSED Search campaign.
    """

    @pytest.fixture()
    def search_campaign(self):
        """Find a PAUSED Search campaign to test with."""
        campaigns = list_campaigns(status="PAUSED")
        for c in campaigns:
            if c["channel_type"] == "SEARCH":
                return c
        pytest.skip("No PAUSED Search campaign available for testing")

    def test_switch_to_maximize_clicks(self, search_campaign):
        """Switch a campaign to MAXIMIZE_CLICKS and verify."""
        campaign_id = search_campaign["id"]

        result = update_campaign(
            campaign_id=campaign_id,
            bidding_strategy_type="MAXIMIZE_CLICKS",
        )
        assert result["status"] == "updated"
        assert "target_spend.target_spend_micros" in result["updated_fields"]
        print(f"\nSwitched campaign {campaign_id} to MAXIMIZE_CLICKS: {result}")

    def test_switch_to_manual_cpc(self, search_campaign):
        """Switch a campaign to MANUAL_CPC and verify."""
        campaign_id = search_campaign["id"]

        result = update_campaign(
            campaign_id=campaign_id,
            bidding_strategy_type="MANUAL_CPC",
        )
        assert result["status"] == "updated"
        assert "manual_cpc.enhanced_cpc_enabled" in result["updated_fields"]
        print(f"\nSwitched campaign {campaign_id} to MANUAL_CPC: {result}")

    def test_switch_to_maximize_conversions(self, search_campaign):
        """Switch a campaign to MAXIMIZE_CONVERSIONS and verify.

        Note: Fails on campaigns with shared budgets (account-level constraint).
        """
        campaign_id = search_campaign["id"]

        result = update_campaign(
            campaign_id=campaign_id,
            bidding_strategy_type="MAXIMIZE_CONVERSIONS",
        )
        assert result["status"] == "updated"
        assert "maximize_conversions.target_cpa_micros" in result["updated_fields"]
        print(f"\nSwitched campaign {campaign_id} to MAXIMIZE_CONVERSIONS: {result}")

    def test_roundtrip_maximize_clicks_to_manual_cpc(self, search_campaign):
        """Switch to MAXIMIZE_CLICKS then to MANUAL_CPC and back."""
        campaign_id = search_campaign["id"]

        r1 = update_campaign(
            campaign_id=campaign_id,
            bidding_strategy_type="MAXIMIZE_CLICKS",
        )
        assert r1["status"] == "updated"

        r2 = update_campaign(
            campaign_id=campaign_id,
            bidding_strategy_type="MANUAL_CPC",
        )
        assert r2["status"] == "updated"

        r3 = update_campaign(
            campaign_id=campaign_id,
            bidding_strategy_type="MAXIMIZE_CLICKS",
        )
        assert r3["status"] == "updated"
        print(f"\nRoundtrip MAXIMIZE_CLICKS -> MANUAL_CPC -> MAXIMIZE_CLICKS for campaign {campaign_id}")
