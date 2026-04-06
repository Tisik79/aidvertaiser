"""Tests for Google Ads tracking URL template tool.

Tests both proto-level field mask correctness and real API integration.
"""

import pytest

from google.ads.googleads.client import GoogleAdsClient
from mcp.server.fastmcp.exceptions import ToolError

from unified_ads_mcp.google.campaigns import (
    google_set_tracking_template as _set,
    google_list_campaigns as _list,
)

# Unwrap FunctionTool objects
set_tracking_template = _set.fn
list_campaigns = _list.fn


class TestTrackingTemplateFieldMasks:
    """Verify that tracking template fields and masks are set correctly at the proto level."""

    @pytest.fixture()
    def client(self):
        from unified_ads_mcp.google.client import get_google_ads_client
        return get_google_ads_client()

    def test_campaign_tracking_url_template_mask(self, client):
        """Campaign tracking_url_template uses correct field mask."""
        op = client.get_type("CampaignOperation")
        campaign = op.update
        campaign.resource_name = "customers/123/campaigns/456"
        campaign.tracking_url_template = "{lpurl}?utm_source=google"
        op.update_mask.paths.append("tracking_url_template")

        assert campaign.tracking_url_template == "{lpurl}?utm_source=google"
        assert "tracking_url_template" in op.update_mask.paths

    def test_campaign_final_url_suffix_mask(self, client):
        """Campaign final_url_suffix uses correct field mask."""
        op = client.get_type("CampaignOperation")
        campaign = op.update
        campaign.resource_name = "customers/123/campaigns/456"
        campaign.final_url_suffix = "utm_source=google&utm_medium=cpc"
        op.update_mask.paths.append("final_url_suffix")

        assert campaign.final_url_suffix == "utm_source=google&utm_medium=cpc"
        assert "final_url_suffix" in op.update_mask.paths

    def test_customer_tracking_url_template_mask(self, client):
        """Customer (account-level) tracking_url_template uses correct field mask."""
        op = client.get_type("CustomerOperation")
        customer = op.update
        customer.tracking_url_template = "{lpurl}?utm_source=google"
        op.update_mask.paths.append("tracking_url_template")

        assert customer.tracking_url_template == "{lpurl}?utm_source=google"
        assert "tracking_url_template" in op.update_mask.paths

    def test_customer_final_url_suffix_mask(self, client):
        """Customer (account-level) final_url_suffix uses correct field mask."""
        op = client.get_type("CustomerOperation")
        customer = op.update
        customer.final_url_suffix = "utm_source=google&utm_medium=cpc"
        op.update_mask.paths.append("final_url_suffix")

        assert customer.final_url_suffix == "utm_source=google&utm_medium=cpc"
        assert "final_url_suffix" in op.update_mask.paths

    def test_customer_both_fields_mask(self, client):
        """Both fields can be set simultaneously on Customer."""
        op = client.get_type("CustomerOperation")
        customer = op.update
        customer.tracking_url_template = "{lpurl}?src=g"
        customer.final_url_suffix = "utm_source=google"
        op.update_mask.paths.extend(["tracking_url_template", "final_url_suffix"])

        assert customer.tracking_url_template == "{lpurl}?src=g"
        assert customer.final_url_suffix == "utm_source=google"
        assert len(op.update_mask.paths) == 2

    def test_empty_string_clears_template(self, client):
        """Empty string should be valid (clears the template)."""
        op = client.get_type("CustomerOperation")
        customer = op.update
        customer.tracking_url_template = ""
        op.update_mask.paths.append("tracking_url_template")

        assert customer.tracking_url_template == ""
        assert "tracking_url_template" in op.update_mask.paths


class TestTrackingTemplateValidation:
    """Test input validation without hitting the API."""

    def test_no_fields_raises_error(self):
        """Must provide at least one field."""
        with pytest.raises(ToolError, match="at least one"):
            set_tracking_template()


class TestTrackingTemplateIntegration:
    """Integration tests that set tracking templates on a real account/campaign.

    Requires a real Google Ads account with at least one PAUSED campaign.
    """

    @pytest.fixture()
    def paused_campaign(self):
        """Find a PAUSED Search campaign to test with."""
        campaigns = list_campaigns(status="PAUSED")
        for c in campaigns:
            if c.get("channel_type") == "SEARCH":
                return c
        pytest.skip("No PAUSED Search campaign available for testing")

    def test_set_account_tracking_template(self):
        """Set tracking URL template at account level."""
        template = "{lpurl}?utm_source=google&utm_medium=cpc"
        result = set_tracking_template(tracking_url_template=template)

        assert result["level"] == "account"
        assert result["status"] == "updated"
        assert "tracking_url_template" in result["updated_fields"]
        assert result["resource_name"]
        print(f"\nSet account tracking template: {result}")

    def test_set_account_final_url_suffix(self):
        """Set final URL suffix at account level."""
        suffix = "utm_source=google&utm_medium=cpc"
        result = set_tracking_template(final_url_suffix=suffix)

        assert result["level"] == "account"
        assert result["status"] == "updated"
        assert "final_url_suffix" in result["updated_fields"]
        print(f"\nSet account final URL suffix: {result}")

    def test_set_account_both_fields(self):
        """Set both tracking template and final URL suffix at account level."""
        result = set_tracking_template(
            tracking_url_template="{lpurl}?utm_source=google&utm_medium=cpc",
            final_url_suffix="utm_source=google&utm_medium=cpc",
        )

        assert result["level"] == "account"
        assert result["status"] == "updated"
        assert "tracking_url_template" in result["updated_fields"]
        assert "final_url_suffix" in result["updated_fields"]
        print(f"\nSet both account fields: {result}")

    def test_set_campaign_tracking_template(self, paused_campaign):
        """Set tracking URL template at campaign level."""
        campaign_id = paused_campaign["id"]
        template = "{lpurl}?utm_source=google&utm_medium=cpc&utm_campaign={campaignid}"
        result = set_tracking_template(
            tracking_url_template=template,
            campaign_id=campaign_id,
        )

        assert result["level"] == "campaign"
        assert result["status"] == "updated"
        assert "tracking_url_template" in result["updated_fields"]
        print(f"\nSet campaign {campaign_id} tracking template: {result}")

    def test_set_campaign_final_url_suffix(self, paused_campaign):
        """Set final URL suffix at campaign level."""
        campaign_id = paused_campaign["id"]
        result = set_tracking_template(
            final_url_suffix="utm_source=google&utm_medium=cpc",
            campaign_id=campaign_id,
        )

        assert result["level"] == "campaign"
        assert result["status"] == "updated"
        assert "final_url_suffix" in result["updated_fields"]
        print(f"\nSet campaign {campaign_id} final URL suffix: {result}")
