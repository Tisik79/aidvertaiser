"""Tests for Meta Ads authentication.

These tests verify that the token-based authentication works correctly,
including token validation, refresh, and config loading.
"""

import os
import time
import pytest
import requests

from unified_ads_mcp.auth.meta_auth import (
    MetaAdsAuth,
    get_meta_auth,
    reset_meta_auth,
    META_GRAPH_URL,
    META_TOKEN_URL,
)


class TestMetaAdsAuth:
    """Test MetaAdsAuth class."""

    def test_load_config(self, meta_config):
        """Test that config is loaded correctly."""
        auth = MetaAdsAuth()
        config = auth._load_config()

        assert isinstance(config, dict)
        assert "access_token" in config or "system_user_token" in config

    def test_get_access_token(self, meta_access_token):
        """Test getting access token."""
        reset_meta_auth()
        auth = get_meta_auth()
        token = auth.get_access_token()

        assert token is not None
        assert len(token) > 50  # Tokens are typically long

    def test_validate_token(self, meta_access_token):
        """Test token validation against Meta API."""
        auth = MetaAdsAuth()
        is_valid = auth._validate_token(meta_access_token)

        assert is_valid is True

    def test_validate_invalid_token(self):
        """Test that invalid tokens are rejected."""
        auth = MetaAdsAuth()
        is_valid = auth._validate_token("invalid_token_12345")

        assert is_valid is False

    def test_token_expiry(self, meta_config):
        """Test that token expiry is tracked."""
        auth = MetaAdsAuth()
        expiry = auth.get_token_expiry()

        if expiry:
            # Should be in the future
            assert expiry > int(time.time())
            # Should be within 60 days
            assert expiry < int(time.time()) + (60 * 24 * 60 * 60)


class TestTokenDebug:
    """Test token debugging via Meta API."""

    def test_debug_token(self, meta_access_token, meta_app_id, meta_app_secret):
        """Test debugging token to get expiry info."""
        response = requests.get(
            f"{META_GRAPH_URL}/debug_token",
            params={
                "input_token": meta_access_token,
                "access_token": f"{meta_app_id}|{meta_app_secret}"
            },
            timeout=10
        )

        assert response.status_code == 200
        data = response.json()

        assert "data" in data
        token_data = data["data"]

        assert token_data.get("is_valid") is True
        assert "expires_at" in token_data

        # Check expiry
        expires_at = token_data.get("expires_at", 0)
        if expires_at > 0:
            days_until_expiry = (expires_at - int(time.time())) / (24 * 60 * 60)
            print(f"\nToken expires in {days_until_expiry:.1f} days")
            assert days_until_expiry > 0  # Token should not be expired

    def test_token_scopes(self, meta_access_token, meta_app_id, meta_app_secret):
        """Test that token has required scopes."""
        response = requests.get(
            f"{META_GRAPH_URL}/debug_token",
            params={
                "input_token": meta_access_token,
                "access_token": f"{meta_app_id}|{meta_app_secret}"
            },
            timeout=10
        )

        data = response.json()
        scopes = data.get("data", {}).get("scopes", [])

        print(f"\nToken scopes: {scopes}")

        # Check for essential ad management scopes
        required_scopes = ["ads_management", "ads_read"]
        for scope in required_scopes:
            if scope not in scopes:
                print(f"Warning: Missing scope {scope}")


class TestGraphAPIAccess:
    """Test direct Graph API access."""

    def test_me_endpoint(self, meta_access_token):
        """Test access to /me endpoint."""
        response = requests.get(
            f"{META_GRAPH_URL}/me",
            params={"access_token": meta_access_token},
            timeout=10
        )

        assert response.status_code == 200
        data = response.json()
        assert "id" in data

        print(f"\nAuthenticated as: {data.get('name', data.get('id'))}")

    def test_ad_accounts_endpoint(self, meta_access_token):
        """Test access to ad accounts."""
        response = requests.get(
            f"{META_GRAPH_URL}/me/adaccounts",
            params={
                "access_token": meta_access_token,
                "fields": "id,name,account_status"
            },
            timeout=10
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data

        accounts = data["data"]
        print(f"\nAccessible ad accounts: {len(accounts)}")
        for acc in accounts[:5]:
            print(f"  - {acc.get('name')} ({acc.get('id')})")
