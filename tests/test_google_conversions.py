"""Tests for Google Ads conversion management tools.

Integration tests using real API credentials.
"""

import pytest

from unified_ads_mcp.google.conversions import (
    google_list_conversion_actions as _list,
    google_get_conversion_action as _get,
    google_create_conversion_action as _create,
    google_update_conversion_action as _update,
    google_delete_conversion_action as _delete,
    google_get_conversion_action_performance as _perf,
)

# Unwrap FunctionTool objects
list_conversion_actions = _list.fn
get_conversion_action = _get.fn
create_conversion_action = _create.fn
update_conversion_action = _update.fn
delete_conversion_action = _delete.fn
get_conversion_action_performance = _perf.fn


class TestGoogleConversionActions:
    """Test Google Ads conversion action tools."""

    def test_list_conversion_actions(self):
        """List all conversion actions for the default account."""
        result = list_conversion_actions()
        assert isinstance(result, list)
        print(f"\nFound {len(result)} conversion actions")
        for action in result[:5]:
            print(f"  - {action['name']} ({action['type']}, {action['status']})")

    def test_list_conversion_actions_enabled_only(self):
        """List only enabled conversion actions."""
        result = list_conversion_actions(status="ENABLED")
        assert isinstance(result, list)
        for action in result:
            assert action["status"] == "ENABLED"

    def test_get_conversion_action(self):
        """Get details of a specific conversion action."""
        actions = list_conversion_actions()
        if not actions:
            pytest.skip("No conversion actions found")

        action_id = actions[0]["id"]
        result = get_conversion_action(conversion_action_id=action_id)
        assert result["id"] == action_id
        assert "name" in result
        assert "type" in result

    def test_conversion_action_performance(self):
        """Get performance metrics by conversion action."""
        result = get_conversion_action_performance(date_range="LAST_30_DAYS")
        assert isinstance(result, list)
        print(f"\nConversion action performance ({len(result)} actions with data):")
        for action in result[:5]:
            print(f"  - {action['name']}: {action['all_conversions']} conversions")

    def test_create_update_delete_conversion_action(self):
        """Full lifecycle: create, update, delete a conversion action."""
        # Create
        result = create_conversion_action(
            name="MCP Test Conversion - DELETE ME",
            type="WEBPAGE",
            category="SUBMIT_LEAD_FORM",
            counting_type="ONE_PER_CLICK",
            default_value=100.0,
            default_currency="CZK",
        )
        assert result["status"] == "created"
        action_id = result["id"]
        print(f"\nCreated conversion action: {action_id}")

        # Update
        update_result = update_conversion_action(
            conversion_action_id=action_id,
            name="MCP Test Conversion UPDATED - DELETE ME",
            default_value=200.0,
        )
        assert update_result["status"] == "updated"

        # Delete
        delete_result = delete_conversion_action(
            conversion_action_id=action_id,
        )
        assert delete_result["status"] == "removed"
        print(f"  Deleted conversion action: {action_id}")
