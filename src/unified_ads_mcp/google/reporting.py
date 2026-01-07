"""Reporting tools for Google Ads API.

This module provides MCP tools for running GAQL queries and generating
performance reports for Google Ads campaigns, keywords, and other entities.
"""

from typing import Any, Optional

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.util import get_nested_attr
from mcp.server.fastmcp.exceptions import ToolError
import proto

from ..server import mcp
from .client import get_google_ads_client, clean_customer_id, format_error, format_value, get_default_customer_id, get_enum_name, micros_to_currency, get_customer_currency


def _preprocess_gaql(query: str) -> str:
    """Preprocesses a GAQL query to add omit_unselected_resource_names=true.

    This optimization reduces response size by omitting resource names
    that weren't explicitly selected in the query.

    Args:
        query: The GAQL query to preprocess.

    Returns:
        The preprocessed query with PARAMETERS clause.
    """
    if "omit_unselected_resource_names" not in query.lower():
        if "PARAMETERS" in query.upper():
            if "include_drafts" in query.lower():
                return query + ", omit_unselected_resource_names=true"
            return query + " omit_unselected_resource_names=true"
        return query + " PARAMETERS omit_unselected_resource_names=true"
    return query


@mcp.tool()
def google_run_query(
    query: str,
    customer_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Executes a Google Ads Query Language (GAQL) query.

    GAQL is a SQL-like language for querying Google Ads data.
    Use this for custom reports and data extraction.

    Args:
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        query: The GAQL query to execute. Example:
            SELECT campaign.id, campaign.name, metrics.clicks
            FROM campaign
            WHERE campaign.status = 'ENABLED'
            ORDER BY metrics.clicks DESC
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        list[dict]: Query results as a list of dictionaries.
            Each dictionary contains the selected fields with their values.
            Enum values are converted to their string names.

    Raises:
        ToolError: If the query is invalid or API request fails.

    Example queries:
        - Campaign performance:
          SELECT campaign.id, campaign.name, metrics.impressions, metrics.clicks
          FROM campaign WHERE campaign.status = 'ENABLED'

        - Keyword performance:
          SELECT ad_group_criterion.keyword.text, metrics.clicks, metrics.cost_micros
          FROM keyword_view ORDER BY metrics.cost_micros DESC LIMIT 10

        - Ad group performance by day:
          SELECT ad_group.name, segments.date, metrics.impressions
          FROM ad_group WHERE segments.date DURING LAST_7_DAYS
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = _preprocess_gaql(query)

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        results = []
        for batch in response:
            for row in batch.results:
                row_data = {}
                for field_path in batch.field_mask.paths:
                    value = get_nested_attr(row, field_path)
                    row_data[field_path] = format_value(value)
                results.append(row_data)

        return results

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_get_campaign_performance(
    customer_id: Optional[str] = None,
    date_range: str = "LAST_30_DAYS",
    campaign_id: Optional[str] = None,
    include_removed: bool = False,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Gets campaign performance metrics for a date range.

    Args:
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        date_range: Predefined date range. Options:
            - TODAY
            - YESTERDAY
            - LAST_7_DAYS
            - LAST_14_DAYS
            - LAST_30_DAYS (default)
            - THIS_WEEK_SUN_TODAY
            - THIS_WEEK_MON_TODAY
            - LAST_WEEK_SUN_SAT
            - LAST_WEEK_MON_SUN
            - THIS_MONTH
            - LAST_MONTH
            - ALL_TIME
        campaign_id: Optional specific campaign ID to get metrics for.
        include_removed: If True, includes removed campaigns.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        list[dict]: Campaign performance data with:
            - campaign_id: Campaign ID
            - campaign_name: Campaign name
            - status: Campaign status
            - channel_type: Advertising channel
            - impressions: Total impressions
            - clicks: Total clicks
            - cost: Total cost in account currency
            - conversions: Total conversions
            - conversion_value: Total conversion value
            - ctr: Click-through rate
            - average_cpc: Average cost per click
            - cost_per_conversion: Cost per conversion

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                campaign.advertising_channel_type,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_per_conversion
            FROM campaign
            WHERE segments.date DURING {date_range}
        """

        conditions = []
        if campaign_id:
            conditions.append(f"campaign.id = {campaign_id}")
        if not include_removed:
            conditions.append("campaign.status != 'REMOVED'")

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " ORDER BY metrics.cost_micros DESC"

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        # Get currency code for the account
        currency_code = get_customer_currency(customer_id, login_customer_id)

        results = []
        for batch in response:
            for row in batch.results:
                results.append({
                    "campaign_id": str(row.campaign.id),
                    "campaign_name": row.campaign.name,
                    "status": get_enum_name(client, "CampaignStatusEnum", row.campaign.status),
                    "channel_type": get_enum_name(client, "AdvertisingChannelTypeEnum", row.campaign.advertising_channel_type),
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost": micros_to_currency(row.metrics.cost_micros),
                    "conversions": row.metrics.conversions,
                    "conversion_value": row.metrics.conversions_value,
                    "ctr": row.metrics.ctr,
                    "average_cpc": micros_to_currency(row.metrics.average_cpc),
                    "cost_per_conversion": micros_to_currency(row.metrics.cost_per_conversion),
                    "currency": currency_code,
                })

        return results

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_get_keyword_performance(
    customer_id: Optional[str] = None,
    date_range: str = "LAST_30_DAYS",
    ad_group_id: Optional[str] = None,
    campaign_id: Optional[str] = None,
    min_impressions: int = 0,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Gets keyword performance metrics for a date range.

    Args:
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        date_range: Predefined date range (same options as campaign performance).
        ad_group_id: Optional ad group ID to filter keywords.
        campaign_id: Optional campaign ID to filter keywords.
        min_impressions: Minimum impressions threshold (default 0).
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        list[dict]: Keyword performance data with:
            - keyword_id: Keyword criterion ID
            - keyword_text: The keyword text
            - match_type: Match type
            - campaign_id: Parent campaign ID
            - campaign_name: Parent campaign name
            - ad_group_id: Parent ad group ID
            - ad_group_name: Parent ad group name
            - impressions, clicks, cost, conversions: Metrics
            - ctr, average_cpc, quality_score: Performance metrics

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = f"""
            SELECT
                ad_group_criterion.criterion_id,
                ad_group_criterion.keyword.text,
                ad_group_criterion.keyword.match_type,
                ad_group_criterion.status,
                ad_group_criterion.quality_info.quality_score,
                campaign.id,
                campaign.name,
                ad_group.id,
                ad_group.name,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc
            FROM keyword_view
            WHERE segments.date DURING {date_range}
                AND ad_group_criterion.status != 'REMOVED'
        """

        if campaign_id:
            query += f" AND campaign.id = {campaign_id}"
        if ad_group_id:
            query += f" AND ad_group.id = {ad_group_id}"
        if min_impressions > 0:
            query += f" AND metrics.impressions >= {min_impressions}"

        query += " ORDER BY metrics.cost_micros DESC"

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        results = []
        for batch in response:
            for row in batch.results:
                results.append({
                    "keyword_id": str(row.ad_group_criterion.criterion_id),
                    "keyword_text": row.ad_group_criterion.keyword.text,
                    "match_type": get_enum_name(client, "KeywordMatchTypeEnum", row.ad_group_criterion.keyword.match_type),
                    "status": get_enum_name(client, "AdGroupCriterionStatusEnum", row.ad_group_criterion.status),
                    "quality_score": row.ad_group_criterion.quality_info.quality_score or None,
                    "campaign_id": str(row.campaign.id),
                    "campaign_name": row.campaign.name,
                    "ad_group_id": str(row.ad_group.id),
                    "ad_group_name": row.ad_group.name,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost": micros_to_currency(row.metrics.cost_micros),
                    "conversions": row.metrics.conversions,
                    "ctr": row.metrics.ctr,
                    "average_cpc": micros_to_currency(row.metrics.average_cpc),
                })

        return results

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_get_ad_performance(
    customer_id: Optional[str] = None,
    date_range: str = "LAST_30_DAYS",
    ad_group_id: Optional[str] = None,
    campaign_id: Optional[str] = None,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Gets ad performance metrics for a date range.

    Args:
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        date_range: Predefined date range (same options as campaign performance).
        ad_group_id: Optional ad group ID to filter ads.
        campaign_id: Optional campaign ID to filter ads.
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        list[dict]: Ad performance data with:
            - ad_id: Ad ID
            - ad_type: Ad type
            - status: Ad status
            - campaign_id/name: Parent campaign
            - ad_group_id/name: Parent ad group
            - impressions, clicks, cost, conversions: Metrics
            - ctr, average_cpc: Performance metrics

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = f"""
            SELECT
                ad_group_ad.ad.id,
                ad_group_ad.ad.type,
                ad_group_ad.status,
                campaign.id,
                campaign.name,
                ad_group.id,
                ad_group.name,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc
            FROM ad_group_ad
            WHERE segments.date DURING {date_range}
                AND ad_group_ad.status != 'REMOVED'
        """

        if campaign_id:
            query += f" AND campaign.id = {campaign_id}"
        if ad_group_id:
            query += f" AND ad_group.id = {ad_group_id}"

        query += " ORDER BY metrics.cost_micros DESC"

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        results = []
        for batch in response:
            for row in batch.results:
                results.append({
                    "ad_id": str(row.ad_group_ad.ad.id),
                    "ad_type": get_enum_name(client, "AdTypeEnum", row.ad_group_ad.ad.type_),
                    "status": get_enum_name(client, "AdGroupAdStatusEnum", row.ad_group_ad.status),
                    "campaign_id": str(row.campaign.id),
                    "campaign_name": row.campaign.name,
                    "ad_group_id": str(row.ad_group.id),
                    "ad_group_name": row.ad_group.name,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost": micros_to_currency(row.metrics.cost_micros),
                    "conversions": row.metrics.conversions,
                    "ctr": row.metrics.ctr,
                    "average_cpc": micros_to_currency(row.metrics.average_cpc),
                })

        return results

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_get_search_terms_report(
    customer_id: Optional[str] = None,
    date_range: str = "LAST_30_DAYS",
    campaign_id: Optional[str] = None,
    ad_group_id: Optional[str] = None,
    min_impressions: int = 0,
    login_customer_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Gets search terms report showing actual user searches.

    This report shows what users actually searched for when your ads appeared.
    Useful for finding new keyword opportunities and negative keywords.

    Args:
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        date_range: Predefined date range (same options as campaign performance).
        campaign_id: Optional campaign ID to filter results.
        ad_group_id: Optional ad group ID to filter results.
        min_impressions: Minimum impressions threshold (default 0).
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        list[dict]: Search terms data with:
            - search_term: The actual search query
            - keyword_text: The matched keyword
            - match_type: How the keyword was matched
            - impressions, clicks, cost, conversions: Metrics
            - campaign/ad_group info

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = f"""
            SELECT
                search_term_view.search_term,
                ad_group_criterion.keyword.text,
                ad_group_criterion.keyword.match_type,
                campaign.id,
                campaign.name,
                ad_group.id,
                ad_group.name,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr
            FROM search_term_view
            WHERE segments.date DURING {date_range}
        """

        if campaign_id:
            query += f" AND campaign.id = {campaign_id}"
        if ad_group_id:
            query += f" AND ad_group.id = {ad_group_id}"
        if min_impressions > 0:
            query += f" AND metrics.impressions >= {min_impressions}"

        query += " ORDER BY metrics.impressions DESC"

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        results = []
        for batch in response:
            for row in batch.results:
                results.append({
                    "search_term": row.search_term_view.search_term,
                    "keyword_text": row.ad_group_criterion.keyword.text,
                    "match_type": get_enum_name(client, "KeywordMatchTypeEnum", row.ad_group_criterion.keyword.match_type),
                    "campaign_id": str(row.campaign.id),
                    "campaign_name": row.campaign.name,
                    "ad_group_id": str(row.ad_group.id),
                    "ad_group_name": row.ad_group.name,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "cost": micros_to_currency(row.metrics.cost_micros),
                    "conversions": row.metrics.conversions,
                    "ctr": row.metrics.ctr,
                })

        return results

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e


@mcp.tool()
def google_get_account_summary(
    customer_id: Optional[str] = None,
    date_range: str = "LAST_30_DAYS",
    login_customer_id: Optional[str] = None,
) -> dict[str, Any]:
    """Gets an account-level performance summary.

    Provides a high-level overview of account performance including
    totals across all campaigns.

    Args:
        customer_id: The Google Ads customer ID (digits only, no dashes).
            Uses default from config if not provided.
        date_range: Predefined date range (same options as campaign performance).
        login_customer_id: Optional MCC account ID if accessing through
            a manager account.

    Returns:
        dict: Account summary with:
            - customer_id: The account ID
            - date_range: The date range used
            - total_campaigns: Number of active campaigns
            - total_impressions: Sum of all impressions
            - total_clicks: Sum of all clicks
            - total_cost: Sum of all costs in account currency
            - total_conversions: Sum of all conversions
            - average_ctr: Overall CTR
            - average_cpc: Overall average CPC
            - cost_per_conversion: Overall cost per conversion

    Raises:
        ToolError: If the API request fails.
    """
    try:
        client = get_google_ads_client(login_customer_id=login_customer_id)
        customer_id = clean_customer_id(customer_id or get_default_customer_id() or "")
        if not customer_id:
            raise ToolError("No customer_id provided and no default configured")

        query = f"""
            SELECT
                customer.id,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value
            FROM customer
            WHERE segments.date DURING {date_range}
        """

        ga_service = client.get_service("GoogleAdsService")
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )

        total_impressions = 0
        total_clicks = 0
        total_cost_micros = 0
        total_conversions = 0
        total_conversion_value = 0

        for batch in response:
            for row in batch.results:
                total_impressions += row.metrics.impressions
                total_clicks += row.metrics.clicks
                total_cost_micros += row.metrics.cost_micros
                total_conversions += row.metrics.conversions
                total_conversion_value += row.metrics.conversions_value

        # Calculate averages
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_cpc = (total_cost_micros / total_clicks) if total_clicks > 0 else 0
        cost_per_conv = (total_cost_micros / total_conversions) if total_conversions > 0 else 0

        # Count active campaigns
        campaign_query = """
            SELECT campaign.id
            FROM campaign
            WHERE campaign.status = 'ENABLED'
        """
        campaign_response = ga_service.search_stream(
            customer_id=customer_id,
            query=campaign_query,
        )
        campaign_count = sum(1 for batch in campaign_response for _ in batch.results)

        # Get currency code for the account
        currency_code = get_customer_currency(customer_id, login_customer_id)

        return {
            "customer_id": customer_id,
            "date_range": date_range,
            "currency": currency_code,
            "total_campaigns": campaign_count,
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "total_cost": micros_to_currency(total_cost_micros),
            "total_conversions": total_conversions,
            "total_conversion_value": total_conversion_value,
            "average_ctr": round(avg_ctr, 2),
            "average_cpc": micros_to_currency(int(avg_cpc)),
            "cost_per_conversion": micros_to_currency(int(cost_per_conv)),
        }

    except GoogleAdsException as e:
        raise ToolError(format_error(e)) from e
