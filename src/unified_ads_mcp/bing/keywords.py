"""Bing Webmaster Tools Keyword Research."""

from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import bing_request


@mcp.tool()
def bing_get_keyword(query: str) -> dict:
    """Gets search volume data for a keyword across all of Bing.

    Returns impression and click data for the given keyword across
    the entire Bing search network. This is NOT site-specific -- it
    shows overall Bing search volume for the keyword.

    Useful for evaluating keyword potential and search demand.

    Args:
        query: The keyword or phrase to look up
            (e.g. "python tutorial", "best running shoes").

    Returns:
        dict: Search volume data including impressions and clicks
            for the keyword.
    """
    try:
        return bing_request("GetKeyword", params={"q": query})
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def bing_get_related_keywords(query: str) -> dict:
    """Gets related and suggested keywords for a query from Bing.

    Returns keywords related to the given query across all of Bing.
    This is NOT site-specific -- it provides keyword suggestions based
    on Bing's search data for content planning and keyword research.

    Args:
        query: The seed keyword or phrase to find related keywords for
            (e.g. "content marketing", "web development").

    Returns:
        dict: List of related keywords with their search volume data.
    """
    try:
        return bing_request("GetRelatedKeywords", params={"q": query})
    except ToolError:
        raise
    except Exception as e:
        raise ToolError(str(e)) from e
