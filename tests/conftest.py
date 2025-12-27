"""Pytest configuration and shared fixtures for Meta Ads tests.

These tests simulate MCP requests by calling the underlying Python functions
directly, bypassing the MCP layer for faster and more reliable testing.
"""

import os
import pytest
import yaml
from pathlib import Path


# Test configuration - uses real Meta Ads credentials from ~/meta-ads.yaml
META_CONFIG_PATH = os.path.expanduser("~/meta-ads.yaml")


@pytest.fixture(scope="session")
def meta_config():
    """Load Meta Ads configuration from ~/meta-ads.yaml."""
    if not os.path.exists(META_CONFIG_PATH):
        pytest.skip("Meta Ads config not found at ~/meta-ads.yaml")

    with open(META_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config


@pytest.fixture(scope="session")
def meta_access_token(meta_config):
    """Get Meta access token from config."""
    token = meta_config.get("access_token") or meta_config.get("system_user_token")
    if not token:
        pytest.skip("No access token in config")
    return token


@pytest.fixture(scope="session")
def meta_account_id(meta_config):
    """Get default Meta Ads account ID from config."""
    account_id = meta_config.get("default_account_id")
    if not account_id:
        pytest.skip("No default_account_id in config")

    # Ensure act_ prefix
    if not account_id.startswith("act_"):
        account_id = f"act_{account_id}"

    return account_id


@pytest.fixture(scope="session")
def meta_app_id(meta_config):
    """Get Meta App ID from config."""
    return meta_config.get("app_id", "779761636818489")


@pytest.fixture(scope="session")
def meta_app_secret(meta_config):
    """Get Meta App Secret from config."""
    secret = meta_config.get("app_secret")
    if not secret:
        pytest.skip("No app_secret in config")
    return secret


@pytest.fixture
def test_image_path():
    """Get path to a test image for upload tests."""
    # Look for images in Downloads/images
    downloads_images = Path.home() / "Downloads" / "images"
    if downloads_images.exists():
        # Find most recent image
        images = list(downloads_images.glob("*.jpg")) + \
                 list(downloads_images.glob("*.png")) + \
                 list(downloads_images.glob("*.jpeg"))
        if images:
            # Sort by modification time, newest first
            images.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            return str(images[0])

    # Fallback to any test image in tests folder
    tests_dir = Path(__file__).parent
    test_images = list(tests_dir.glob("*.jpg")) + list(tests_dir.glob("*.png"))
    if test_images:
        return str(test_images[0])

    pytest.skip("No test image available")


# Test campaign/ad set/creative IDs created during this session
# These will be cleaned up if tests pass
@pytest.fixture(scope="session")
def test_entities():
    """Track test entities for cleanup."""
    return {
        "campaigns": [],
        "adsets": [],
        "creatives": [],
        "ads": [],
        "images": []
    }
