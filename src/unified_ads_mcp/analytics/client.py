"""Google Analytics API client factory.

This module provides factory functions for creating configured Google Analytics
Admin and Data API clients that use the authentication handled by the auth module.

Example:
    >>> from unified_ads_mcp.analytics.client import get_admin_client, get_data_client
    >>> admin = get_admin_client()
    >>> data = get_data_client()
"""

import sys
from typing import Optional

from google.analytics.admin_v1beta import AnalyticsAdminServiceClient
from google.analytics.data_v1beta import BetaAnalyticsDataClient

from unified_ads_mcp.auth.google_analytics_auth import (
    get_google_analytics_auth,
    GoogleAnalyticsAuth,
)


class GoogleAnalyticsClientFactory:
    """Factory for creating configured Google Analytics API clients.

    This factory manages the creation of AnalyticsAdminServiceClient and
    BetaAnalyticsDataClient instances with proper authentication.
    """

    def __init__(self, auth: Optional[GoogleAnalyticsAuth] = None):
        self._auth = auth

    @property
    def auth(self) -> GoogleAnalyticsAuth:
        """Get the auth handler, creating if necessary."""
        if self._auth is None:
            self._auth = get_google_analytics_auth()
        return self._auth

    def get_admin_client(
        self, force_refresh: bool = False
    ) -> AnalyticsAdminServiceClient:
        """Get a configured Google Analytics Admin API client."""
        credentials = self.auth.get_credentials(force_refresh=force_refresh)
        try:
            return AnalyticsAdminServiceClient(credentials=credentials)
        except Exception as e:
            print(
                f"[Google Analytics] Admin client creation failed: {e}",
                file=sys.stderr,
            )
            raise

    def get_data_client(
        self, force_refresh: bool = False
    ) -> BetaAnalyticsDataClient:
        """Get a configured Google Analytics Data API client."""
        credentials = self.auth.get_credentials(force_refresh=force_refresh)
        try:
            return BetaAnalyticsDataClient(credentials=credentials)
        except Exception as e:
            print(
                f"[Google Analytics] Data client creation failed: {e}",
                file=sys.stderr,
            )
            raise


# Global factory instance
_factory: Optional[GoogleAnalyticsClientFactory] = None


def get_admin_client(
    force_refresh: bool = False,
) -> AnalyticsAdminServiceClient:
    """Get a configured Google Analytics Admin API client."""
    global _factory
    if _factory is None:
        _factory = GoogleAnalyticsClientFactory()
    return _factory.get_admin_client(force_refresh=force_refresh)


def get_data_client(
    force_refresh: bool = False,
) -> BetaAnalyticsDataClient:
    """Get a configured Google Analytics Data API client."""
    global _factory
    if _factory is None:
        _factory = GoogleAnalyticsClientFactory()
    return _factory.get_data_client(force_refresh=force_refresh)


def get_default_property_id() -> Optional[str]:
    """Gets the default GA4 property ID from the configuration.

    Returns:
        The default property ID if configured, None otherwise.
    """
    try:
        auth = get_google_analytics_auth()
        return auth.default_property_id
    except Exception:
        return None


def resolve_property_id(property_id: Optional[str] = None) -> str:
    """Resolve the property ID, falling back to the configured default.

    Args:
        property_id: An explicit property ID. If not provided, the default
                    from configuration will be used.

    Returns:
        The resolved property ID (digits only, without 'properties/' prefix).

    Raises:
        ValueError: If no property_id is provided and no default is configured.
    """
    if not property_id:
        property_id = get_default_property_id()
    if not property_id:
        raise ValueError(
            "No property_id provided and no default_property_id configured. "
            "Set default_property_id in google-analytics.yaml or pass property_id explicitly."
        )
    # Strip 'properties/' prefix if present
    if property_id.startswith("properties/"):
        property_id = property_id.split("/")[-1]
    return str(property_id).strip()


def format_property_name(property_id: str) -> str:
    """Format a property ID into the full resource name.

    Args:
        property_id: The property ID (digits only or full resource name).

    Returns:
        The full property resource name (e.g., 'properties/123456').
    """
    if property_id.startswith("properties/"):
        return property_id
    return f"properties/{property_id}"


def reset_client_factory() -> None:
    """Reset the global client factory (useful for testing)."""
    global _factory
    _factory = None
