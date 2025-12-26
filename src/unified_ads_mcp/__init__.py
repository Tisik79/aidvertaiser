"""Unified Ads MCP Server for Google Ads and Meta Ads.

This package provides a unified MCP (Model Context Protocol) server that enables
AI assistants to manage advertising campaigns across both Google Ads and Meta Ads
platforms using a single interface.

Features:
    - Browser-based OAuth authentication for both platforms
    - Automatic token refresh and caching
    - Full campaign management (CRUD operations)
    - Reporting and insights
    - GAQL query support for Google Ads
"""

from unified_ads_mcp.server import main, mcp

__version__ = "1.0.0"
__all__ = ["main", "mcp", "__version__"]
