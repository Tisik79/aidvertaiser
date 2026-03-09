"""Site management tools for Matomo Analytics."""

from typing import Any, Optional

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import matomo_request, resolve_site_id


@mcp.tool()
def matomo_list_sites() -> list[dict[str, Any]]:
    """Lists all websites/apps tracked in Matomo.

    Returns:
        list[dict]: List of sites with idsite, name, main_url, timezone,
            currency, ecommerce, sitesearch, ts_created, type.
    """
    try:
        return matomo_request("SitesManager.getAllSites")
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_site(site_id: Optional[int] = None) -> dict[str, Any]:
    """Gets details about a specific Matomo site.

    Args:
        site_id: The Matomo site ID. Uses default from config if not provided.

    Returns:
        dict: Site details including name, main_url, timezone, currency, etc.
    """
    try:
        site_id = resolve_site_id(site_id)
        result = matomo_request(
            "SitesManager.getSiteFromId", {"idSite": site_id}
        )
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return result
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_add_site(
    name: str,
    urls: list[str],
    timezone: str = "Europe/Prague",
    currency: str = "CZK",
    ecommerce: bool = False,
    site_search: bool = True,
    site_type: str = "website",
) -> dict[str, Any]:
    """Creates a new website/app in Matomo.

    Args:
        name: Site name.
        urls: List of URLs for the site (first is main URL).
        timezone: IANA timezone (default "Europe/Prague").
        currency: ISO 4217 currency code (default "CZK").
        ecommerce: Enable ecommerce tracking.
        site_search: Enable site search tracking.
        site_type: Type of site ("website" or "mobileapp").

    Returns:
        dict: Created site with its new idsite.
    """
    try:
        params = {
            "siteName": name,
            "timezone": timezone,
            "currency": currency,
            "ecommerce": 1 if ecommerce else 0,
            "siteSearch": 1 if site_search else 0,
            "type": site_type,
        }
        for i, url in enumerate(urls):
            params[f"urls[{i}]"] = url

        result = matomo_request("SitesManager.addSite", params)
        site_id = result.get("value") if isinstance(result, dict) else result
        return {"idsite": site_id, "name": name, "urls": urls, "status": "created"}
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_update_site(
    site_id: Optional[int] = None,
    name: Optional[str] = None,
    urls: Optional[list[str]] = None,
    timezone: Optional[str] = None,
    currency: Optional[str] = None,
    ecommerce: Optional[bool] = None,
    site_search: Optional[bool] = None,
) -> dict[str, Any]:
    """Updates an existing Matomo site.

    Args:
        site_id: The site ID to update. Uses default from config if not provided.
        name: New site name.
        urls: New list of URLs.
        timezone: New IANA timezone.
        currency: New ISO 4217 currency code.
        ecommerce: Enable/disable ecommerce tracking.
        site_search: Enable/disable site search tracking.

    Returns:
        dict: Update confirmation.
    """
    try:
        site_id = resolve_site_id(site_id)
        params: dict[str, Any] = {"idSite": site_id}

        if name is not None:
            params["siteName"] = name
        if timezone is not None:
            params["timezone"] = timezone
        if currency is not None:
            params["currency"] = currency
        if ecommerce is not None:
            params["ecommerce"] = 1 if ecommerce else 0
        if site_search is not None:
            params["siteSearch"] = 1 if site_search else 0
        if urls is not None:
            for i, url in enumerate(urls):
                params[f"urls[{i}]"] = url

        if len(params) <= 1:
            raise ToolError("No fields to update. Provide at least one field.")

        matomo_request("SitesManager.updateSite", params)
        return {"idsite": site_id, "status": "updated"}
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_delete_site(site_id: int) -> dict[str, Any]:
    """Deletes a site from Matomo.

    Args:
        site_id: The site ID to delete.

    Returns:
        dict: Deletion confirmation.
    """
    try:
        matomo_request("SitesManager.deleteSite", {"idSite": site_id})
        return {"idsite": site_id, "status": "deleted"}
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def matomo_get_site_urls(site_id: Optional[int] = None) -> list[str]:
    """Gets all URLs associated with a Matomo site.

    Args:
        site_id: The site ID. Uses default from config if not provided.

    Returns:
        list[str]: All URLs for the site.
    """
    try:
        site_id = resolve_site_id(site_id)
        return matomo_request(
            "SitesManager.getSiteUrlsFromId", {"idSite": site_id}
        )
    except Exception as e:
        raise ToolError(str(e)) from e
