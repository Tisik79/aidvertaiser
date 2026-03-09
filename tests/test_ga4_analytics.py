"""Integration tests for Google Analytics tools.

These tests call the real GA4 API using credentials from
~/google-analytics.yaml or ~/google-ads.yaml (for client_id/client_secret).

Run with: pytest tests/test_ga4_analytics.py -v
"""

import os
import pytest
import yaml
from pathlib import Path


# --- Fixtures ---

GA_CONFIG_PATH = os.path.expanduser("~/google-analytics.yaml")
ADS_CONFIG_PATH = os.path.expanduser("~/google-ads.yaml")


@pytest.fixture(scope="session")
def ga_config():
    """Load Google Analytics configuration."""
    if os.path.exists(GA_CONFIG_PATH):
        with open(GA_CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    if os.path.exists(ADS_CONFIG_PATH):
        with open(ADS_CONFIG_PATH, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        return {
            "client_id": config.get("client_id"),
            "client_secret": config.get("client_secret"),
        }

    pytest.skip("No Google Analytics or Google Ads config found")


@pytest.fixture(scope="session")
def ga_property_id(ga_config):
    """Get default GA4 property ID from config."""
    prop_id = ga_config.get("default_property_id")
    if not prop_id:
        pytest.skip("No default_property_id in config")
    return str(prop_id)


# --- Import tool functions ---
# Access the underlying function via .fn to bypass MCP wrapper

from unified_ads_mcp.analytics.accounts import (
    ga4_list_accounts as _ga4_list_accounts,
    ga4_list_account_summaries as _ga4_list_account_summaries,
)
from unified_ads_mcp.analytics.properties import (
    ga4_list_properties as _ga4_list_properties,
    ga4_get_property as _ga4_get_property,
)
from unified_ads_mcp.analytics.data_streams import (
    ga4_list_data_streams as _ga4_list_data_streams,
)
from unified_ads_mcp.analytics.reporting import (
    ga4_run_report as _ga4_run_report,
    ga4_run_realtime_report as _ga4_run_realtime_report,
    ga4_get_metadata as _ga4_get_metadata,
)
from unified_ads_mcp.analytics.key_events import (
    ga4_list_key_events as _ga4_list_key_events,
)

ga4_list_accounts = _ga4_list_accounts.fn
ga4_list_account_summaries = _ga4_list_account_summaries.fn
ga4_list_properties = _ga4_list_properties.fn
ga4_get_property = _ga4_get_property.fn
ga4_list_data_streams = _ga4_list_data_streams.fn
ga4_run_report = _ga4_run_report.fn
ga4_run_realtime_report = _ga4_run_realtime_report.fn
ga4_get_metadata = _ga4_get_metadata.fn
ga4_list_key_events = _ga4_list_key_events.fn


# --- Account Tests ---


class TestAccounts:
    def test_list_accounts(self, ga_config):
        """Test listing all accessible GA4 accounts."""
        result = ga4_list_accounts()
        assert isinstance(result, list)
        if len(result) > 0:
            account = result[0]
            assert "id" in account
            assert "display_name" in account
            assert "name" in account
            print(f"\nFound {len(result)} accounts")
            for acc in result:
                print(f"  - {acc['display_name']} (ID: {acc['id']})")

    def test_list_account_summaries(self, ga_config):
        """Test listing account summaries with properties."""
        result = ga4_list_account_summaries()
        assert isinstance(result, list)
        if len(result) > 0:
            summary = result[0]
            assert "account" in summary
            assert "display_name" in summary
            assert "properties" in summary
            print(f"\nFound {len(result)} account summaries")
            for s in result:
                print(f"  - {s['display_name']}: {len(s['properties'])} properties")


# --- Property Tests ---


class TestProperties:
    def test_list_properties(self, ga_config):
        """Test listing properties for an account."""
        # First get an account
        accounts = ga4_list_accounts()
        if not accounts:
            pytest.skip("No GA4 accounts available")

        account_id = accounts[0]["id"]
        result = ga4_list_properties(account_id=account_id)
        assert isinstance(result, list)
        print(f"\nFound {len(result)} properties for account {account_id}")
        for prop in result:
            print(f"  - {prop['display_name']} (ID: {prop['id']}, TZ: {prop['time_zone']})")

    def test_get_property(self, ga_property_id):
        """Test getting a specific property."""
        result = ga4_get_property(property_id=ga_property_id)
        assert isinstance(result, dict)
        assert result["id"] == ga_property_id
        assert "display_name" in result
        assert "time_zone" in result
        assert "currency_code" in result
        print(f"\nProperty: {result['display_name']}")
        print(f"  Time zone: {result['time_zone']}")
        print(f"  Currency: {result['currency_code']}")
        print(f"  Type: {result['property_type']}")


# --- Data Stream Tests ---


class TestDataStreams:
    def test_list_data_streams(self, ga_property_id):
        """Test listing data streams for a property."""
        result = ga4_list_data_streams(property_id=ga_property_id)
        assert isinstance(result, list)
        print(f"\nFound {len(result)} data streams")
        for stream in result:
            print(f"  - {stream['display_name']} ({stream['type']})")
            if stream.get("measurement_id"):
                print(f"    Measurement ID: {stream['measurement_id']}")
            if stream.get("default_uri"):
                print(f"    URI: {stream['default_uri']}")


# --- Reporting Tests ---


class TestReporting:
    def test_run_report_basic(self, ga_property_id):
        """Test running a basic report with country and sessions."""
        result = ga4_run_report(
            property_id=ga_property_id,
            dimensions=["country"],
            metrics=["activeUsers", "sessions"],
            start_date="30daysAgo",
            end_date="today",
            limit=10,
        )
        assert isinstance(result, dict)
        assert "headers" in result
        assert "rows" in result
        assert "row_count" in result
        assert "country" in result["headers"]["dimensions"]
        assert "activeUsers" in result["headers"]["metrics"]
        print(f"\nReport: {result['row_count']} total rows, showing top {len(result['rows'])}")
        for row in result["rows"][:5]:
            print(f"  {row.get('country', 'N/A')}: {row.get('activeUsers', 0)} users, {row.get('sessions', 0)} sessions")

    def test_run_report_with_ordering(self, ga_property_id):
        """Test report with descending order by sessions."""
        result = ga4_run_report(
            property_id=ga_property_id,
            dimensions=["pagePath"],
            metrics=["screenPageViews", "activeUsers"],
            start_date="7daysAgo",
            end_date="today",
            order_by=["-screenPageViews"],
            limit=5,
        )
        assert isinstance(result, dict)
        assert len(result["rows"]) <= 5
        print(f"\nTop pages (last 7 days):")
        for row in result["rows"]:
            print(f"  {row.get('pagePath', 'N/A')}: {row.get('screenPageViews', 0)} views")

    def test_run_report_with_filter(self, ga_property_id):
        """Test report with a dimension filter."""
        result = ga4_run_report(
            property_id=ga_property_id,
            dimensions=["deviceCategory"],
            metrics=["activeUsers", "sessions"],
            start_date="30daysAgo",
            end_date="today",
            limit=10,
        )
        assert isinstance(result, dict)
        print(f"\nDevice categories:")
        for row in result["rows"]:
            print(f"  {row.get('deviceCategory', 'N/A')}: {row.get('activeUsers', 0)} users")

    def test_run_realtime_report(self, ga_property_id):
        """Test running a realtime report."""
        result = ga4_run_realtime_report(
            property_id=ga_property_id,
            dimensions=["country"],
            metrics=["activeUsers"],
            minutes_ago=30,
        )
        assert isinstance(result, dict)
        assert "headers" in result
        assert "rows" in result
        print(f"\nRealtime ({result['row_count']} countries active):")
        for row in result["rows"][:5]:
            print(f"  {row.get('country', 'N/A')}: {row.get('activeUsers', 0)} active")

    def test_get_metadata(self, ga_property_id):
        """Test getting available dimensions and metrics."""
        result = ga4_get_metadata(property_id=ga_property_id)
        assert isinstance(result, dict)
        assert "dimensions" in result
        assert "metrics" in result
        assert len(result["dimensions"]) > 0
        assert len(result["metrics"]) > 0
        print(f"\nAvailable: {len(result['dimensions'])} dimensions, {len(result['metrics'])} metrics")
        print("Sample dimensions:")
        for d in result["dimensions"][:5]:
            print(f"  - {d['api_name']}: {d['ui_name']}")
        print("Sample metrics:")
        for m in result["metrics"][:5]:
            print(f"  - {m['api_name']}: {m['ui_name']}")


# --- Key Events Tests ---


class TestKeyEvents:
    def test_list_key_events(self, ga_property_id):
        """Test listing key events (conversions)."""
        result = ga4_list_key_events(property_id=ga_property_id)
        assert isinstance(result, list)
        print(f"\nFound {len(result)} key events")
        for event in result:
            print(f"  - {event['event_name']} ({event.get('counting_method', 'N/A')})")
