"""Meta Ads API client factory.

This module provides factory functions for creating configured Meta (Facebook)
Ads API clients that use the authentication handled by the auth module.

Example:
    >>> from unified_ads_mcp.meta.client import get_meta_api, get_ad_account
    >>> api = get_meta_api()
    >>> account = get_ad_account("act_123456789")
    >>> campaigns = account.get_campaigns()
"""

import os
import sys
import json
import functools
from typing import Any, Dict, Optional, Callable

import yaml
import httpx
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.user import User
from facebook_business.exceptions import FacebookRequestError

from unified_ads_mcp.auth.meta_auth import get_meta_auth, MetaAdsAuth
from ..config import only_default_account_enabled


# Constants
META_GRAPH_API_VERSION = "v22.0"
META_GRAPH_API_BASE = f"https://graph.facebook.com/{META_GRAPH_API_VERSION}"
USER_AGENT = "unified-ads-mcp/1.0"
DEFAULT_CREDENTIALS_PATH = os.path.expanduser("~/meta-ads.yaml")


def get_default_account_id() -> Optional[str]:
    """Get the default Meta Ads account ID from config file.

    Reads from META_DEFAULT_ACCOUNT_ID env var or META_ADS_CREDENTIALS/~/meta-ads.yaml.

    Returns:
        The default account ID (with act_ prefix) or None if not configured.
    """
    env_default = os.environ.get("META_DEFAULT_ACCOUNT_ID")
    if env_default:
        return ensure_account_prefix(str(env_default))

    credentials_path = os.environ.get("META_ADS_CREDENTIALS", DEFAULT_CREDENTIALS_PATH)

    if not os.path.isfile(credentials_path):
        return None

    try:
        with open(credentials_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

        default_id = config.get("default_account_id")
        if default_id:
            # Ensure it has the act_ prefix
            default_id = str(default_id)
            if not default_id.startswith("act_"):
                default_id = f"act_{default_id}"
            return default_id
        return None
    except Exception:
        return None


def resolve_account_id(account_id: Optional[str]) -> Optional[str]:
    """Resolve the account ID, enforcing ONLY_DEFAULT_ACCOUNT when enabled."""
    default_id = get_default_account_id()
    if only_default_account_enabled():
        return default_id
    return account_id or default_id


class MetaAdsClientFactory:
    """Factory for creating configured Meta Ads API clients.

    This factory manages the initialization of the FacebookAdsApi and
    creation of AdAccount objects with proper authentication. It supports:
        - Automatic OAuth authentication via browser
        - Token refresh when tokens expire
        - Ad account access by ID

    Example:
        >>> factory = MetaAdsClientFactory()
        >>> api = factory.get_api()
        >>> account = factory.get_ad_account("act_123456789")
    """

    def __init__(self, auth: Optional[MetaAdsAuth] = None):
        """Initialize the client factory.

        Args:
            auth: Optional MetaAdsAuth instance. If not provided,
                  the global singleton will be used.
        """
        self._auth = auth
        self._api_initialized = False

    @property
    def auth(self) -> MetaAdsAuth:
        """Get the auth handler, creating if necessary."""
        if self._auth is None:
            self._auth = get_meta_auth()
        return self._auth

    def get_api(self, force_refresh: bool = False) -> FacebookAdsApi:
        """Get an initialized Facebook Ads API instance.

        This method ensures the API is initialized with a valid access token.
        If the token is expired, it will trigger re-authentication.

        Args:
            force_refresh: If True, force re-authentication via browser.

        Returns:
            An initialized FacebookAdsApi instance.

        Raises:
            TimeoutError: If browser authentication times out.
            RuntimeError: If authentication fails.
        """
        auth = self.auth
        access_token = auth.get_access_token(force_refresh=force_refresh)

        if not self._api_initialized:
            app_id = os.environ.get("META_APP_ID", "")
            app_secret = os.environ.get("META_APP_SECRET", "")

            FacebookAdsApi.init(
                app_id=app_id,
                app_secret=app_secret,
                access_token=access_token,
                api_version=META_GRAPH_API_VERSION,
            )
            self._api_initialized = True
            print("[Meta Ads] API initialized", file=sys.stderr)
        else:
            # Update the token in case it was refreshed
            api = FacebookAdsApi.get_default_api()
            if api:
                api._session.access_token = access_token

        return FacebookAdsApi.get_default_api()

    def get_ad_account(
        self,
        account_id: str,
        force_refresh: bool = False,
    ) -> AdAccount:
        """Get an AdAccount object for the specified account ID.

        Args:
            account_id: The Meta Ads account ID. Can be with or without
                       the "act_" prefix.
            force_refresh: If True, force re-authentication via browser.

        Returns:
            An AdAccount object configured with valid authentication.

        Raises:
            TimeoutError: If browser authentication times out.
            RuntimeError: If authentication fails.
        """
        # Ensure API is initialized
        self.get_api(force_refresh=force_refresh)

        # Normalize account ID
        account_id = ensure_account_prefix(account_id)

        return AdAccount(account_id)

    def get_current_user(self, force_refresh: bool = False) -> User:
        """Get the current authenticated user.

        Args:
            force_refresh: If True, force re-authentication via browser.

        Returns:
            A User object for the current user.
        """
        self.get_api(force_refresh=force_refresh)
        return User(fbid="me")

    def list_ad_accounts(self, force_refresh: bool = False) -> list[dict]:
        """List all ad accounts accessible by the current user.

        Args:
            force_refresh: If True, force re-authentication via browser.

        Returns:
            List of dictionaries containing account information.
        """
        user = self.get_current_user(force_refresh=force_refresh)

        try:
            accounts = user.get_ad_accounts(
                fields=[
                    "id",
                    "name",
                    "account_status",
                    "currency",
                    "amount_spent",
                    "business_name",
                ]
            )

            return [
                {
                    "id": acc.get("id"),
                    "name": acc.get("name"),
                    "status": acc.get("account_status"),
                    "currency": acc.get("currency"),
                    "amount_spent": acc.get("amount_spent"),
                    "business_name": acc.get("business_name"),
                }
                for acc in accounts
            ]
        except FacebookRequestError as e:
            # Token might be expired - try to re-authenticate
            error_msg = str(e).lower()
            if "expired" in error_msg or "invalid" in error_msg:
                print("[Meta Ads] Token expired, re-authenticating...", file=sys.stderr)
                self.auth.invalidate()
                self._api_initialized = False
                return self.list_ad_accounts(force_refresh=True)
            raise

    def validate_api(self) -> bool:
        """Validate that the API is properly authenticated.

        Returns:
            True if the API is valid, False otherwise.
        """
        try:
            user = self.get_current_user()
            user.api_get(fields=["id", "name"])
            return True
        except FacebookRequestError:
            return False
        except Exception:
            return False


# Global factory instance
_factory: Optional[MetaAdsClientFactory] = None


def get_meta_api(force_refresh: bool = False) -> FacebookAdsApi:
    """Get an initialized Meta Ads API using the global factory.

    This is the primary entry point for getting a Meta Ads API instance.
    The API is configured with authentication from the auth module
    and is ready to use with the facebook-business library.

    Args:
        force_refresh: If True, force re-authentication via browser.

    Returns:
        An initialized FacebookAdsApi instance.

    Raises:
        TimeoutError: If browser authentication times out.
        RuntimeError: If authentication fails.

    Example:
        >>> api = get_meta_api()
        >>>
        >>> # The API is now the default for all SDK operations
        >>> from facebook_business.adobjects.adaccount import AdAccount
        >>> account = AdAccount("act_123456789")
        >>> campaigns = account.get_campaigns()
    """
    global _factory

    if _factory is None:
        _factory = MetaAdsClientFactory()

    return _factory.get_api(force_refresh=force_refresh)


def get_ad_account(
    account_id: str,
    force_refresh: bool = False,
) -> AdAccount:
    """Get an AdAccount object for the specified account ID.

    This function ensures the API is initialized before creating the
    AdAccount object.

    Args:
        account_id: The Meta Ads account ID. Can be with or without
                   the "act_" prefix (e.g., "123456789" or "act_123456789").
        force_refresh: If True, force re-authentication via browser.

    Returns:
        An AdAccount object configured with valid authentication.

    Raises:
        TimeoutError: If browser authentication times out.
        RuntimeError: If authentication fails.

    Example:
        >>> account = get_ad_account("act_123456789")
        >>>
        >>> # List campaigns
        >>> campaigns = account.get_campaigns(
        ...     fields=["id", "name", "status", "objective"]
        ... )
        >>>
        >>> # Create a campaign
        >>> campaign = account.create_campaign(params={
        ...     "name": "My Campaign",
        ...     "objective": "OUTCOME_LEADS",
        ...     "status": "PAUSED",
        ... })
    """
    global _factory

    if _factory is None:
        _factory = MetaAdsClientFactory()

    return _factory.get_ad_account(
        account_id=account_id,
        force_refresh=force_refresh,
    )


def list_accessible_accounts(force_refresh: bool = False) -> list[dict]:
    """List all ad accounts accessible by the current user.

    Convenience function that wraps the factory's list_ad_accounts method.

    Args:
        force_refresh: If True, force re-authentication via browser.

    Returns:
        List of dictionaries containing account information with keys:
            - id: Account ID (with act_ prefix)
            - name: Account name
            - status: Account status
            - currency: Account currency
            - amount_spent: Total amount spent
            - business_name: Associated business name

    Example:
        >>> accounts = list_accessible_accounts()
        >>> for acc in accounts:
        ...     print(f"{acc['name']} ({acc['id']})")
    """
    global _factory

    if _factory is None:
        _factory = MetaAdsClientFactory()

    return _factory.list_ad_accounts(force_refresh=force_refresh)


def reset_client_factory() -> None:
    """Reset the global client factory (useful for testing)."""
    global _factory
    _factory = None


# Utility functions (kept for backward compatibility)


def ensure_account_prefix(account_id: str) -> str:
    """Ensure account ID has the 'act_' prefix.

    Args:
        account_id: Account ID with or without prefix.

    Returns:
        Account ID with 'act_' prefix.
    """
    if not account_id:
        return account_id
    if not account_id.startswith("act_"):
        return f"act_{account_id}"
    return account_id


async def make_api_request(
    endpoint: str,
    access_token: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    method: str = "GET",
) -> Dict[str, Any]:
    """Make a direct request to the Meta Graph API.

    This is a lower-level function for making direct API calls without
    using the facebook-business SDK.

    Args:
        endpoint: API endpoint path (without base URL).
        access_token: Meta API access token. If not provided, gets from auth.
        params: Additional query parameters.
        method: HTTP method (GET, POST, DELETE).

    Returns:
        API response as a dictionary.
    """
    if not access_token:
        auth = get_meta_auth()
        access_token = auth.get_access_token()

    url = f"{META_GRAPH_API_BASE}/{endpoint}"

    headers = {
        "User-Agent": USER_AGENT,
    }

    request_params = params or {}
    request_params["access_token"] = access_token

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                # JSON-encode dict/list params
                encoded_params = {}
                for key, value in request_params.items():
                    if isinstance(value, (dict, list)):
                        encoded_params[key] = json.dumps(value)
                    else:
                        encoded_params[key] = value
                response = await client.get(
                    url, params=encoded_params, headers=headers, timeout=30.0
                )

            elif method == "POST":
                # Convert lists and dicts to JSON strings for POST
                for key, value in list(request_params.items()):
                    if isinstance(value, (list, dict)):
                        request_params[key] = json.dumps(value)
                response = await client.post(
                    url, data=request_params, headers=headers, timeout=30.0
                )

            elif method == "DELETE":
                response = await client.delete(
                    url, params=request_params, headers=headers, timeout=30.0
                )

            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

            try:
                return response.json()
            except json.JSONDecodeError:
                return {
                    "text_response": response.text,
                    "status_code": response.status_code,
                }

        except httpx.HTTPStatusError as e:
            error_info = {}
            try:
                error_info = e.response.json()
            except Exception:
                error_info = {
                    "status_code": e.response.status_code,
                    "text": e.response.text,
                }

            return {
                "error": {
                    "message": f"HTTP Error: {e.response.status_code}",
                    "details": error_info,
                }
            }

        except Exception as e:
            return {"error": {"message": str(e)}}


def meta_api_tool(func: Callable) -> Callable:
    """Decorator for Meta API tools that handles authentication and error handling.

    Args:
        func: The async function to wrap.

    Returns:
        Wrapped function with authentication and error handling.
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # If access_token is not in kwargs or empty, get from auth
            if "access_token" not in kwargs or not kwargs["access_token"]:
                auth = get_meta_auth()
                kwargs["access_token"] = auth.get_access_token()

            # Call the original function
            result = await func(*args, **kwargs)
            return result

        except FacebookRequestError as e:
            # Handle Facebook API errors
            error_code = e.api_error_code()

            # Check for auth errors and invalidate token
            if error_code in [190, 102, 4]:
                auth = get_meta_auth()
                auth.invalidate()

            return {
                "error": {
                    "message": e.api_error_message(),
                    "code": error_code,
                    "type": e.api_error_type(),
                }
            }

        except Exception as e:
            return {"error": {"message": str(e)}}

    return wrapper
