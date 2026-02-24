"""Tests for Meta Ads creative and image management.

These tests verify image upload, creative creation, and the full
campaign hierarchy including creatives and ads.
"""

import asyncio
import base64
import pytest
import time


# Import the Meta Ads functions and access underlying async functions via .fn
from unified_ads_mcp.meta.creatives import (
    meta_upload_image as _meta_upload_image,
    meta_create_creative as _meta_create_creative,
    meta_update_creative as _meta_update_creative,
    download_image_from_url,  # This is not decorated
)
from unified_ads_mcp.meta.campaigns import (
    meta_create_campaign as _meta_create_campaign,
    meta_update_campaign as _meta_update_campaign,
)
from unified_ads_mcp.meta.adsets import (
    meta_create_adset as _meta_create_adset,
)
from unified_ads_mcp.meta.ads import (
    meta_create_ad as _meta_create_ad,
    meta_get_ad_details as _meta_get_ad_details,
)

# Access the underlying async functions (.fn) from FunctionTool objects
meta_upload_image = _meta_upload_image.fn
meta_create_creative = _meta_create_creative.fn
meta_update_creative = _meta_update_creative.fn
meta_create_campaign = _meta_create_campaign.fn
meta_update_campaign = _meta_update_campaign.fn
meta_create_adset = _meta_create_adset.fn
meta_create_ad = _meta_create_ad.fn
meta_get_ad_details = _meta_get_ad_details.fn


@pytest.fixture(scope="module")
def event_loop():
    """Create an event loop for the test module."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


class TestImageDownload:
    """Test image download utility."""

    @pytest.mark.asyncio
    async def test_download_image_from_url(self):
        """Test downloading an image from a URL."""
        # Use a reliable public image
        url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
        result = await download_image_from_url(url)

        # This might fail if URL is not accessible
        if result is None:
            pytest.skip("Could not download image from URL")

        assert isinstance(result, bytes)
        assert len(result) > 0
        print(f"\nDownloaded {len(result)} bytes")


class TestImageUpload:
    """Test image upload functionality."""

    @pytest.mark.asyncio
    async def test_upload_from_file_path(
        self, meta_access_token, meta_account_id, test_image_path, test_entities
    ):
        """Test uploading image from local file path."""
        result = await meta_upload_image(
            account_id=meta_account_id,
            access_token=meta_access_token,
            file_path=test_image_path,
            name=f"test_upload_{int(time.time())}.jpg",
        )

        assert "error" not in result, f"Upload failed: {result}"
        assert "image_hash" in result
        assert result.get("success") is True

        image_hash = result["image_hash"]
        test_entities["images"].append(image_hash)

        print(f"\nUploaded image from file: {test_image_path}")
        print(f"  Hash: {image_hash}")
        print(f"  Account: {result.get('account_id')}")

    @pytest.mark.asyncio
    async def test_upload_from_base64(
        self, meta_access_token, meta_account_id, test_image_path, test_entities
    ):
        """Test uploading image from base64 data."""
        # Read and encode image
        with open(test_image_path, "rb") as f:
            image_bytes = f.read()
        base64_data = base64.b64encode(image_bytes).decode("utf-8")

        result = await meta_upload_image(
            account_id=meta_account_id,
            access_token=meta_access_token,
            file=base64_data,
            name=f"test_base64_{int(time.time())}.jpg",
        )

        assert "error" not in result, f"Upload failed: {result}"
        assert "image_hash" in result

        image_hash = result["image_hash"]
        test_entities["images"].append(image_hash)

        print("\nUploaded image from base64")
        print(f"  Hash: {image_hash}")

    @pytest.mark.asyncio
    async def test_upload_from_data_url(
        self, meta_access_token, meta_account_id, test_image_path, test_entities
    ):
        """Test uploading image from data URL."""
        # Read and encode as data URL
        with open(test_image_path, "rb") as f:
            image_bytes = f.read()
        base64_data = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{base64_data}"

        result = await meta_upload_image(
            account_id=meta_account_id,
            access_token=meta_access_token,
            file=data_url,
            name=f"test_dataurl_{int(time.time())}.jpg",
        )

        assert "error" not in result, f"Upload failed: {result}"
        assert "image_hash" in result

        image_hash = result["image_hash"]
        test_entities["images"].append(image_hash)

        print("\nUploaded image from data URL")
        print(f"  Hash: {image_hash}")

    @pytest.mark.asyncio
    async def test_upload_nonexistent_file(self, meta_access_token, meta_account_id):
        """Test error handling for nonexistent file."""
        result = await meta_upload_image(
            account_id=meta_account_id,
            access_token=meta_access_token,
            file_path="/nonexistent/path/to/image.jpg",
        )

        assert "error" in result
        assert "not found" in result["error"]["message"].lower()


class TestCreativeCreation:
    """Test creative creation and management."""

    @pytest.fixture
    def page_id(self, meta_config):
        """Get a Facebook Page ID for creative tests."""
        # You need to configure a page_id in meta-ads.yaml for these tests
        page_id = meta_config.get("page_id")
        if not page_id:
            pytest.skip("No page_id configured in meta-ads.yaml")
        return page_id

    @pytest.mark.asyncio
    async def test_create_creative_with_image(
        self, meta_access_token, meta_account_id, test_entities, page_id
    ):
        """Test creating a creative with an uploaded image."""
        if not test_entities.get("images"):
            pytest.skip("No uploaded images available")

        image_hash = test_entities["images"][0]
        timestamp = int(time.time())

        result = await meta_create_creative(
            image_hash=image_hash,
            page_id=page_id,
            name=f"Test Creative {timestamp}",
            message="This is a test ad message created by automated testing.",
            link_url="https://example.com/test",
            account_id=meta_account_id,
            access_token=meta_access_token,
            headline="Test Headline",
            description="Test description for the ad creative",
            call_to_action_type="LEARN_MORE",
        )

        assert "error" not in result, f"Creative creation failed: {result}"
        assert result.get("success") is True
        assert "creative_id" in result

        creative_id = result["creative_id"]
        test_entities["creatives"].append(creative_id)

        print(f"\nCreated creative: {creative_id}")
        print(f"  Details: {result.get('details', {}).get('name')}")


class TestFullCampaignHierarchy:
    """Test creating a complete campaign hierarchy: Campaign → Ad Set → Creative → Ad."""

    @pytest.fixture
    def page_id(self, meta_config):
        """Get a Facebook Page ID for tests."""
        page_id = meta_config.get("page_id")
        if not page_id:
            pytest.skip("No page_id configured in meta-ads.yaml")
        return page_id

    @pytest.mark.asyncio
    async def test_create_full_hierarchy(
        self,
        meta_access_token,
        meta_account_id,
        test_image_path,
        page_id,
        test_entities,
    ):
        """Test creating a complete campaign hierarchy."""
        timestamp = int(time.time())

        # 1. Create Campaign
        print("\n=== Creating Campaign ===")
        campaign_result = await meta_create_campaign(
            name=f"Full Test Campaign {timestamp}",
            objective="OUTCOME_TRAFFIC",
            account_id=meta_account_id,
            access_token=meta_access_token,
            status="PAUSED",
            daily_budget=1000,
        )

        assert "error" not in campaign_result, (
            f"Campaign creation failed: {campaign_result}"
        )
        campaign_id = campaign_result["id"]
        test_entities["campaigns"].append(campaign_id)
        print(f"  Campaign ID: {campaign_id}")

        # 2. Create Ad Set
        print("\n=== Creating Ad Set ===")
        adset_result = await meta_create_adset(
            campaign_id=campaign_id,
            name=f"Full Test Ad Set {timestamp}",
            optimization_goal="LINK_CLICKS",
            billing_event="IMPRESSIONS",
            targeting={
                "age_min": 18,
                "age_max": 65,
                "geo_locations": {"countries": ["CZ"]},
                "targeting_automation": {"advantage_audience": 1},
            },
            account_id=meta_account_id,
            access_token=meta_access_token,
            status="PAUSED",
        )

        assert "error" not in adset_result, f"Ad set creation failed: {adset_result}"
        adset_id = adset_result["id"]
        test_entities["adsets"].append(adset_id)
        print(f"  Ad Set ID: {adset_id}")

        # 3. Upload Image
        print("\n=== Uploading Image ===")
        image_result = await meta_upload_image(
            account_id=meta_account_id,
            access_token=meta_access_token,
            file_path=test_image_path,
            name=f"hierarchy_test_{timestamp}.jpg",
        )

        assert "error" not in image_result, f"Image upload failed: {image_result}"
        image_hash = image_result["image_hash"]
        test_entities["images"].append(image_hash)
        print(f"  Image Hash: {image_hash}")

        # 4. Create Creative
        print("\n=== Creating Creative ===")
        creative_result = await meta_create_creative(
            image_hash=image_hash,
            page_id=page_id,
            name=f"Full Test Creative {timestamp}",
            message="Complete hierarchy test ad.",
            link_url="https://example.com/hierarchy-test",
            account_id=meta_account_id,
            access_token=meta_access_token,
            headline="Hierarchy Test",
            call_to_action_type="LEARN_MORE",
        )

        assert "error" not in creative_result, (
            f"Creative creation failed: {creative_result}"
        )
        creative_id = creative_result["creative_id"]
        test_entities["creatives"].append(creative_id)
        print(f"  Creative ID: {creative_id}")

        # 5. Create Ad
        print("\n=== Creating Ad ===")
        ad_result = await meta_create_ad(
            name=f"Full Test Ad {timestamp}",
            adset_id=adset_id,
            creative_id=creative_id,
            account_id=meta_account_id,
            access_token=meta_access_token,
            status="PAUSED",
        )

        assert "error" not in ad_result, f"Ad creation failed: {ad_result}"
        ad_id = ad_result["id"]
        test_entities["ads"].append(ad_id)
        print(f"  Ad ID: {ad_id}")

        # 6. Verify Ad Details
        print("\n=== Verifying Ad ===")
        ad_details = await meta_get_ad_details(
            ad_id=ad_id, access_token=meta_access_token
        )

        assert "error" not in ad_details
        assert ad_details.get("adset_id") == adset_id
        print(f"  Ad verified with ad set: {ad_details.get('adset_id')}")

        print("\n=== Full Hierarchy Created Successfully ===")
        print(f"  Campaign: {campaign_id}")
        print(f"  Ad Set:   {adset_id}")
        print(f"  Creative: {creative_id}")
        print(f"  Ad:       {ad_id}")


class TestCreativeCleanup:
    """Cleanup test creatives and campaigns."""

    @pytest.mark.asyncio
    async def test_cleanup_test_entities(self, meta_access_token, test_entities):
        """Delete test entities (mark as deleted)."""
        # Delete campaigns (which cascades to ad sets and ads)
        for campaign_id in test_entities.get("campaigns", []):
            result = await meta_update_campaign(
                campaign_id=campaign_id,
                access_token=meta_access_token,
                status="DELETED",
            )

            if "error" not in result:
                print(f"\nDeleted campaign: {campaign_id}")

        print("\nTest entities summary:")
        print(f"  Campaigns: {len(test_entities.get('campaigns', []))}")
        print(f"  Ad Sets: {len(test_entities.get('adsets', []))}")
        print(f"  Creatives: {len(test_entities.get('creatives', []))}")
        print(f"  Ads: {len(test_entities.get('ads', []))}")
        print(f"  Images: {len(test_entities.get('images', []))}")
