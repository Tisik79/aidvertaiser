"""Account management tools for Google Analytics."""

from typing import Any
from google.api_core.exceptions import GoogleAPICallError
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import get_admin_client


@mcp.tool()
def ga4_list_accounts() -> list[dict[str, Any]]:
    """Lists all Google Analytics accounts accessible by the authenticated user.
    
    Returns:
        list[dict]: List of accounts with id, display_name, region_code, create_time, update_time.
    """
    try:
        client = get_admin_client()
        accounts = list(client.list_accounts())
        return [
            {
                "id": account.name.split("/")[-1],
                "name": account.name,
                "display_name": account.display_name,
                "region_code": account.region_code,
                "create_time": account.create_time.isoformat() if account.create_time else None,
                "update_time": account.update_time.isoformat() if account.update_time else None,
            }
            for account in accounts
        ]
    except GoogleAPICallError as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def ga4_list_account_summaries() -> list[dict[str, Any]]:
    """Lists account summaries with their properties for a quick overview.
    
    Returns:
        list[dict]: Account summaries with nested property summaries.
    """
    try:
        client = get_admin_client()
        summaries = list(client.list_account_summaries())
        return [
            {
                "account": summary.account,
                "display_name": summary.display_name,
                "properties": [
                    {
                        "property": prop.property,
                        "display_name": prop.display_name,
                        "property_type": prop.property_type.name if prop.property_type else None,
                        "parent": prop.parent,
                    }
                    for prop in summary.property_summaries
                ],
            }
            for summary in summaries
        ]
    except GoogleAPICallError as e:
        raise ToolError(str(e)) from e
