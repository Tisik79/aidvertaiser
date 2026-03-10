"""Google Search Console Site Management Tools."""

from typing import Optional

from ..server import mcp
from .client import get_searchconsole_service


@mcp.tool()
async def gsc_list_sites() -> dict:
    """Lists all sites registered in Google Search Console.

    Returns all sites the authenticated user has access to, including
    their permission level and verification status.

    Returns:
        Dictionary with siteEntry list, each containing:
            - siteUrl: The site URL (https://example.com/ or sc-domain:example.com)
            - permissionLevel: siteOwner, siteFullUser, siteRestrictedUser, siteUnverifiedUser
    """
    service = get_searchconsole_service()
    return service.sites().list().execute()


@mcp.tool()
async def gsc_get_site(site_url: str) -> dict:
    """Gets details for a specific site in Search Console.

    Args:
        site_url: The site URL exactly as shown in Search Console.
            Examples: "https://example.com/", "sc-domain:example.com"

    Returns:
        Dictionary with site details including siteUrl and permissionLevel.
    """
    service = get_searchconsole_service()
    return service.sites().get(siteUrl=site_url).execute()


@mcp.tool()
async def gsc_add_site(site_url: str) -> dict:
    """Adds (registers) a site in Google Search Console.

    The site will appear as unverified until you complete verification
    (DNS TXT record, HTML file, or other method).

    For domain properties use "sc-domain:example.com" format.
    For URL-prefix properties use "https://example.com/" format.

    Args:
        site_url: The site URL to register.
            - Domain property: "sc-domain:example.com"
            - URL prefix: "https://example.com/"

    Returns:
        Dictionary with success status.
    """
    service = get_searchconsole_service()
    service.sites().add(siteUrl=site_url).execute()
    return {"success": True, "siteUrl": site_url, "message": "Site added. Complete verification to gain full access."}


@mcp.tool()
async def gsc_delete_site(site_url: str) -> dict:
    """Removes a site from Google Search Console.

    This only removes your access - it doesn't affect the actual website.

    Args:
        site_url: The site URL to remove (exactly as shown in Search Console).

    Returns:
        Dictionary with success status.
    """
    service = get_searchconsole_service()
    service.sites().delete(siteUrl=site_url).execute()
    return {"success": True, "siteUrl": site_url, "message": "Site removed from Search Console."}
