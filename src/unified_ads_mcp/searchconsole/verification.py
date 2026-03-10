"""Google Search Console Site Verification Tools."""

from typing import Optional

from googleapiclient.discovery import build

from ..server import mcp
from unified_ads_mcp.auth.google_searchconsole_auth import get_google_searchconsole_auth


def _get_verification_service():
    """Get a configured Site Verification API service."""
    auth = get_google_searchconsole_auth()
    creds = auth.get_credentials()
    return build("siteVerification", "v1", credentials=creds)


@mcp.tool()
async def gsc_get_verification_token(
    site_url: str,
    verification_method: str = "DNS_TXT",
    site_type: str = "INET_DOMAIN",
) -> dict:
    """Gets a verification token for proving site ownership.

    Use this before gsc_verify_site to get the token you need to place
    in DNS or on your website.

    Args:
        site_url: The domain or URL to verify.
            - For domain properties: "example.com" (no protocol)
            - For URL prefix: "https://example.com/" (with protocol)
        verification_method: How to verify. Options:
            - "DNS_TXT": Add a TXT record to DNS (recommended for domains)
            - "DNS_CNAME": Add a CNAME record to DNS
            - "FILE": Upload an HTML file to the site root
            - "META": Add a meta tag to the homepage
            - "ANALYTICS": Use existing Google Analytics access
            - "TAG_MANAGER": Use existing Tag Manager access
        site_type: Type of site identifier:
            - "INET_DOMAIN": A domain (e.g., "example.com")
            - "SITE": A URL prefix (e.g., "https://example.com/")

    Returns:
        Dictionary with:
            - token: The verification string to add
            - method: The verification method
    """
    service = _get_verification_service()
    return service.webResource().getToken(body={
        "site": {
            "type": site_type,
            "identifier": site_url,
        },
        "verificationMethod": verification_method,
    }).execute()


@mcp.tool()
async def gsc_verify_site(
    site_url: str,
    verification_method: str = "DNS_TXT",
    site_type: str = "INET_DOMAIN",
) -> dict:
    """Verifies site ownership after placing the verification token.

    Call this AFTER you've added the DNS TXT record, HTML file, or meta tag
    obtained from gsc_get_verification_token.

    Args:
        site_url: The domain or URL to verify (same as used in get_token).
        verification_method: The method used (same as used in get_token).
        site_type: Type of site identifier:
            - "INET_DOMAIN": A domain
            - "SITE": A URL prefix

    Returns:
        Dictionary with verification result including owners list.
    """
    service = _get_verification_service()
    return service.webResource().insert(
        verificationMethod=verification_method,
        body={
            "site": {
                "type": site_type,
                "identifier": site_url,
            }
        }
    ).execute()


@mcp.tool()
async def gsc_list_verified_sites() -> dict:
    """Lists all sites verified via the Site Verification API.

    Returns:
        Dictionary with list of verified web resources and their owners.
    """
    service = _get_verification_service()
    return service.webResource().list().execute()
