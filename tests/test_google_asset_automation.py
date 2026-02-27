"""Tests for Google Ads asset automation tools.

Integration tests using real API credentials.
"""

import pytest

from unified_ads_mcp.google.assets import (
    google_get_asset_automation_settings as _get_settings,
    google_update_asset_automation_settings as _update_settings,
    google_list_auto_created_assets as _list_auto,
    google_remove_auto_created_asset as _remove_auto,
)

# Unwrap FunctionTool objects
get_asset_automation_settings = _get_settings.fn
update_asset_automation_settings = _update_settings.fn
list_auto_created_assets = _list_auto.fn
remove_auto_created_asset = _remove_auto.fn


class TestAssetAutomationSettings:
    """Test campaign-level asset automation settings."""

    def _get_search_or_pmax_campaign_id(self) -> str:
        """Helper to get a Search or PMax campaign ID (asset automation only works on these)."""
        from unified_ads_mcp.google.campaigns import google_list_campaigns

        campaigns = google_list_campaigns.fn()
        for c in campaigns:
            if c["status"] in ("ENABLED", "PAUSED") and c["channel_type"] in (
                "SEARCH",
                "PERFORMANCE_MAX",
            ):
                return c["id"]
        pytest.skip("No active Search or Performance Max campaigns found")

    def test_get_asset_automation_settings(self):
        """Read automation settings for a campaign."""
        campaign_id = self._get_search_or_pmax_campaign_id()
        result = get_asset_automation_settings(campaign_id=campaign_id)

        assert result["id"] == campaign_id
        assert "name" in result
        assert "channel_type" in result
        assert isinstance(result["asset_automation_settings"], list)

        print(f"\nCampaign: {result['name']} ({result['channel_type']})")
        if result["asset_automation_settings"]:
            for s in result["asset_automation_settings"]:
                print(f"  {s['type']}: {s['status']}")
        else:
            print("  No automation settings configured")

    def test_update_asset_automation_settings(self):
        """Toggle TEXT_ASSET_AUTOMATION off and back on.

        NOTE: This may fail with OPERATION_NOT_PERMITTED_FOR_CONTEXT on campaigns
        that have AI Max enabled or other account-level restrictions. The API
        supports this operation but not all campaigns/accounts permit it.
        """
        campaign_id = self._get_search_or_pmax_campaign_id()

        # Read current state
        before = get_asset_automation_settings(campaign_id=campaign_id)
        print(f"\nCampaign: {before['name']}")
        print(f"  Current settings: {before['asset_automation_settings']}")

        try:
            # Disable text automation
            result = update_asset_automation_settings(
                campaign_id=campaign_id,
                automation_type="TEXT_ASSET_AUTOMATION",
                enabled=False,
            )
            assert result["result"] == "updated"
            assert result["status"] == "OPTED_OUT"
            print(f"  Disabled TEXT_ASSET_AUTOMATION")

            # Verify
            after = get_asset_automation_settings(campaign_id=campaign_id)
            text_setting = next(
                (
                    s
                    for s in after["asset_automation_settings"]
                    if s["type"] == "TEXT_ASSET_AUTOMATION"
                ),
                None,
            )
            assert text_setting is not None
            assert text_setting["status"] == "OPTED_OUT"

            # Re-enable (restore original state)
            result = update_asset_automation_settings(
                campaign_id=campaign_id,
                automation_type="TEXT_ASSET_AUTOMATION",
                enabled=True,
            )
            assert result["result"] == "updated"
            assert result["status"] == "OPTED_IN"
            print(f"  Re-enabled TEXT_ASSET_AUTOMATION")

        except Exception as e:
            if "OPERATION_NOT_PERMITTED_FOR_CONTEXT" in str(e):
                pytest.skip(
                    "Campaign does not permit asset automation changes via API "
                    "(likely AI Max or account-level restriction)"
                )
            raise


class TestAutoCreatedAssets:
    """Test account-level automatically created assets."""

    def test_list_auto_created_assets_account_level(self):
        """List all auto-created assets at account level."""
        result = list_auto_created_assets()
        assert isinstance(result, list)

        print(f"\nFound {len(result)} auto-created assets (account level)")
        for asset in result[:10]:
            details = asset.get("details", {})
            label = (
                details.get("link_text")
                or details.get("callout_text")
                or details.get("header")
                or details.get("text")
                or "?"
            )
            print(f"  [{asset['field_type']}] {label} ({asset['status']})")

    def test_list_auto_created_sitelinks(self):
        """List only auto-created sitelinks."""
        result = list_auto_created_assets(field_type="SITELINK")
        assert isinstance(result, list)

        print(f"\nFound {len(result)} auto-created sitelinks")
        for asset in result:
            assert asset["field_type"] == "SITELINK"
            details = asset.get("details", {})
            print(
                f"  - {details.get('link_text', '?')}: "
                f"{details.get('description1', '')}"
            )

    def test_list_auto_created_callouts(self):
        """List only auto-created callouts."""
        result = list_auto_created_assets(field_type="CALLOUT")
        assert isinstance(result, list)

        print(f"\nFound {len(result)} auto-created callouts")
        for asset in result:
            assert asset["field_type"] == "CALLOUT"

    def test_list_auto_created_structured_snippets(self):
        """List only auto-created structured snippets."""
        result = list_auto_created_assets(field_type="STRUCTURED_SNIPPET")
        assert isinstance(result, list)

        print(f"\nFound {len(result)} auto-created structured snippets")
        for asset in result:
            assert asset["field_type"] == "STRUCTURED_SNIPPET"

    def test_remove_auto_created_asset_invalid_resource(self):
        """Removing with invalid resource name should fail."""
        with pytest.raises(Exception):
            remove_auto_created_asset(
                resource_name="invalid/resource/name",
            )
