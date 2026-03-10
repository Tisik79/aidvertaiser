"""Bing Webmaster Tools API key authentication handler.

This module provides simple API key authentication for the Bing Webmaster Tools API.
No OAuth is needed - just an API key from Bing Webmaster Tools settings.

Configuration:
    Set BING_WEBMASTER_CREDENTIALS env var to point to your config file,
    or place it at ~/bing-webmaster.yaml (default location).

    Required fields in bing-webmaster.yaml:
        api_key: Your Bing Webmaster Tools API key

    Optional fields:
        default_site_url: https://yoursite.com  # default site for operations
"""

import os
from typing import Optional

import yaml

DEFAULT_CREDENTIALS_PATH = os.path.expanduser("~/bing-webmaster.yaml")


class BingWebmasterAuth:
    """Handles Bing Webmaster Tools API key authentication.

    Simple API key auth - no browser flow needed.
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Bing Webmaster auth handler.

        Args:
            config_path: Path to bing-webmaster.yaml config file.
                Falls back to BING_WEBMASTER_CREDENTIALS env var,
                then ~/bing-webmaster.yaml.

        Raises:
            FileNotFoundError: If config file does not exist.
            ValueError: If api_key is missing from config.
        """
        self.config_path = config_path or os.environ.get(
            "BING_WEBMASTER_CREDENTIALS", DEFAULT_CREDENTIALS_PATH
        )
        self._config = self._load_config()
        self._validate_config()

    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Bing Webmaster config not found at {self.config_path}. "
                "Set BING_WEBMASTER_CREDENTIALS env var or create "
                "~/bing-webmaster.yaml with: api_key (required) and "
                "optional default_site_url."
            )

        with open(self.config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

        return config

    def _validate_config(self) -> None:
        """Validate that required config fields are present."""
        if not self._config.get("api_key"):
            raise ValueError(
                f"Missing required field 'api_key' in {self.config_path}. "
                "Get your API key from Bing Webmaster Tools > Settings > API Access."
            )

    @property
    def api_key(self) -> str:
        """Get the Bing Webmaster Tools API key."""
        return self._config["api_key"]

    @property
    def default_site_url(self) -> Optional[str]:
        """Get the default site URL, if configured."""
        return self._config.get("default_site_url")


# Global singleton instance
_bing_auth: Optional[BingWebmasterAuth] = None


def get_bing_auth(config_path: Optional[str] = None) -> BingWebmasterAuth:
    """Get or create the Bing Webmaster auth handler singleton.

    Args:
        config_path: Optional path to config file (only used on first call).

    Returns:
        BingWebmasterAuth singleton instance.
    """
    global _bing_auth

    if _bing_auth is None:
        _bing_auth = BingWebmasterAuth(config_path)

    return _bing_auth


def reset_bing_auth() -> None:
    """Reset the Bing auth singleton (for testing)."""
    global _bing_auth
    _bing_auth = None
