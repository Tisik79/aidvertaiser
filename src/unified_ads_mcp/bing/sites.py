"""Bing Webmaster Tools Site Management."""

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import bing_request


@mcp.tool()
def bing_list_sites() -> dict:
    """Lists all sites registered in Bing Webmaster Tools.

    Returns all sites the authenticated user has access to, including
    their URL and verification status.

    Returns:
        dict: Dictionary with sites list, each containing Url and
            verification status fields.
    """
    try:
        return bing_request("GetUserSites")
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_add_site(site_url: str) -> dict:
    """Adds (registers) a new site in Bing Webmaster Tools.

    The site will appear as unverified until you complete verification
    (DNS CNAME record, meta tag, or XML file method).

    Args:
        site_url: The full site URL to register (e.g. "https://example.com").

    Returns:
        dict: Success confirmation with the added site URL.
    """
    try:
        bing_request(
            "AddSite", body={"siteUrl": site_url}, http_method="POST"
        )
        return {
            "success": True,
            "siteUrl": site_url,
            "message": "Site added. Complete verification to gain full access.",
        }
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_verify_site(site_url: str) -> dict:
    """Verifies ownership of a site in Bing Webmaster Tools.

    The DNS CNAME record, meta tag, or XML file must already be in place
    before calling this. Bing will check for the verification token and
    confirm ownership if found.

    Args:
        site_url: The site URL to verify (e.g. "https://example.com").

    Returns:
        dict: Success confirmation with the verified site URL.
    """
    try:
        bing_request(
            "VerifySite", body={"siteUrl": site_url}, http_method="POST"
        )
        return {
            "success": True,
            "siteUrl": site_url,
            "message": "Site verification initiated. Check Bing Webmaster Tools for status.",
        }
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_remove_site(site_url: str) -> dict:
    """Removes a site from Bing Webmaster Tools.

    This only removes the site from your Bing Webmaster Tools account.
    It does not affect the actual website or its indexing.

    Args:
        site_url: The site URL to remove (e.g. "https://example.com").

    Returns:
        dict: Success confirmation with the removed site URL.
    """
    try:
        bing_request(
            "RemoveSite", body={"siteUrl": site_url}, http_method="POST"
        )
        return {
            "success": True,
            "siteUrl": site_url,
            "message": "Site removed from Bing Webmaster Tools.",
        }
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e
