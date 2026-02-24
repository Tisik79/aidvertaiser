"""Tests for Meta Ads conversion management tools.

Integration tests using real API credentials.
"""

import asyncio
import time
import pytest

from unified_ads_mcp.meta.conversions import (
    meta_list_pixels as _list_pixels,
    meta_get_pixel as _get_pixel,
    meta_get_pixel_stats as _pixel_stats,
    meta_list_custom_conversions as _list_cc,
    meta_get_custom_conversion as _get_cc,
    meta_create_custom_conversion as _create_cc,
    meta_update_custom_conversion as _update_cc,
    meta_delete_custom_conversion as _delete_cc,
    meta_send_conversion_event as _send_event,
    meta_list_offline_conversion_sets as _list_ocs,
)

# Unwrap FunctionTool objects
list_pixels = _list_pixels.fn
get_pixel = _get_pixel.fn
get_pixel_stats = _pixel_stats.fn
list_custom_conversions = _list_cc.fn
get_custom_conversion = _get_cc.fn
create_custom_conversion = _create_cc.fn
update_custom_conversion = _update_cc.fn
delete_custom_conversion = _delete_cc.fn
send_conversion_event = _send_event.fn
list_offline_conversion_sets = _list_ocs.fn


def _skip_on_permission_error(result: dict, feature: str = "this feature"):
    """Skip the test if the API returns a permission or unsupported-field error."""
    if "error" in result:
        msg = str(result["error"].get("message", ""))
        details = result["error"].get("details", {}).get("error", {})
        code = details.get("code", 0)
        detail_msg = details.get("message", "")
        # 403 / code 200 = permission denied; code 100 = nonexisting field
        if "403" in msg or code == 200 or code == 100:
            pytest.skip(
                f"Skipping: account lacks permission for {feature} ({detail_msg})"
            )


@pytest.fixture(scope="module")
def event_loop():
    """Create an event loop for the test module."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


class TestMetaPixels:
    """Test Meta Pixel management tools."""

    @pytest.mark.asyncio
    async def test_list_pixels(self, meta_access_token, meta_account_id):
        """List all pixels for the account."""
        result = await list_pixels(
            account_id=meta_account_id, access_token=meta_access_token
        )
        _skip_on_permission_error(result, "pixel listing")
        assert "error" not in result
        assert "data" in result
        print(f"\nFound {len(result['data'])} pixels")
        for pixel in result["data"]:
            print(f"  - {pixel.get('name')} (ID: {pixel['id']})")

    @pytest.mark.asyncio
    async def test_get_pixel(self, meta_access_token, meta_account_id):
        """Get details of a specific pixel."""
        pixels = await list_pixels(
            account_id=meta_account_id, access_token=meta_access_token
        )
        _skip_on_permission_error(pixels, "pixel listing")
        if not pixels.get("data"):
            pytest.skip("No pixels found")

        pixel_id = pixels["data"][0]["id"]
        result = await get_pixel(pixel_id=pixel_id, access_token=meta_access_token)
        assert "error" not in result
        assert result["id"] == pixel_id

    @pytest.mark.asyncio
    async def test_get_pixel_stats(self, meta_access_token, meta_account_id):
        """Get pixel event statistics."""
        pixels = await list_pixels(
            account_id=meta_account_id, access_token=meta_access_token
        )
        _skip_on_permission_error(pixels, "pixel listing")
        if not pixels.get("data"):
            pytest.skip("No pixels found")

        pixel_id = pixels["data"][0]["id"]
        result = await get_pixel_stats(
            pixel_id=pixel_id, access_token=meta_access_token
        )
        assert "error" not in result
        print(f"\nPixel {pixel_id} stats: {result}")


class TestMetaCustomConversions:
    """Test Meta custom conversion management tools."""

    @pytest.mark.asyncio
    async def test_list_custom_conversions(self, meta_access_token, meta_account_id):
        """List all custom conversions."""
        result = await list_custom_conversions(
            account_id=meta_account_id, access_token=meta_access_token
        )
        _skip_on_permission_error(result, "custom conversions")
        assert "error" not in result
        data = result.get("data", [])
        print(f"\nFound {len(data)} custom conversions")

    @pytest.mark.asyncio
    async def test_create_update_delete_custom_conversion(
        self, meta_access_token, meta_account_id
    ):
        """Full lifecycle: create, update, delete a custom conversion."""
        # First get a pixel ID
        pixels = await list_pixels(
            account_id=meta_account_id, access_token=meta_access_token
        )
        _skip_on_permission_error(pixels, "pixel listing")
        if not pixels.get("data"):
            pytest.skip("No pixels found for custom conversion test")

        pixel_id = pixels["data"][0]["id"]

        # Create
        result = await create_custom_conversion(
            name="MCP Test Custom Conv - DELETE ME",
            pixel_id=pixel_id,
            rule='{"and":[{"url":{"i_contains":"mcp-test-page-delete-me"}}]}',
            custom_event_type="OTHER",
            default_conversion_value=100.0,
            account_id=meta_account_id,
            access_token=meta_access_token,
        )
        assert "error" not in result
        cc_id = result.get("id")
        assert cc_id
        print(f"\nCreated custom conversion: {cc_id}")

        # Update
        update_result = await update_custom_conversion(
            custom_conversion_id=cc_id,
            name="MCP Test Custom Conv UPDATED - DELETE ME",
            access_token=meta_access_token,
        )
        assert "error" not in update_result

        # Delete
        delete_result = await delete_custom_conversion(
            custom_conversion_id=cc_id,
            access_token=meta_access_token,
        )
        assert "error" not in delete_result
        print(f"  Deleted custom conversion: {cc_id}")


class TestMetaCAPI:
    """Test Meta Conversions API (CAPI) tools."""

    @pytest.mark.asyncio
    async def test_send_conversion_event(self, meta_access_token, meta_account_id):
        """Send a test conversion event via CAPI."""
        # Get pixel ID
        pixels = await list_pixels(
            account_id=meta_account_id, access_token=meta_access_token
        )
        _skip_on_permission_error(pixels, "pixel listing")
        if not pixels.get("data"):
            pytest.skip("No pixels found for CAPI test")

        pixel_id = pixels["data"][0]["id"]

        result = await send_conversion_event(
            pixel_id=pixel_id,
            event_name="Lead",
            access_token=meta_access_token,
            event_source_url="https://test.example.com/mcp-test",
            user_data={
                "em": "mcp-test@example.com",
                "fn": "Test",
                "ln": "User",
                "country": "CZ",
            },
            custom_data={
                "value": 100.0,
                "currency": "CZK",
            },
            event_id=f"mcp_test_{int(time.time())}",
        )
        assert "error" not in result
        print(f"\nCAPI event sent: {result}")


class TestMetaOfflineConversions:
    """Test Meta offline conversion tools."""

    @pytest.mark.asyncio
    async def test_list_offline_conversion_sets(
        self, meta_access_token, meta_account_id
    ):
        """List offline conversion sets."""
        result = await list_offline_conversion_sets(
            account_id=meta_account_id, access_token=meta_access_token
        )
        _skip_on_permission_error(result, "offline conversion sets")
        assert "error" not in result
        data = result.get("data", [])
        print(f"\nFound {len(data)} offline conversion sets")
