"""Reporting tools for Google Analytics Data API.

This module provides MCP tools for running GA4 reports, realtime reports,
and retrieving available dimensions/metrics metadata. These are the primary
tools for extracting analytics data from Google Analytics 4 properties.
"""

from typing import Any, Optional

from google.api_core.exceptions import GoogleAPICallError
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import get_data_client, resolve_property_id, format_property_name

from google.analytics.data_v1beta.types import (
    RunReportRequest,
    RunRealtimeReportRequest,
    DateRange,
    Dimension,
    Metric,
    FilterExpression,
    Filter,
    NumericValue,
    OrderBy,
    MinuteRange,
)

# These filter types are nested inside Filter
StringFilter = Filter.StringFilter
NumericFilter = Filter.NumericFilter
InListFilter = Filter.InListFilter


def _parse_report_response(response) -> dict[str, Any]:
    """Parse a report response into a serializable dict.

    Extracts dimension/metric headers, row data, totals, and quota
    information from a GA4 report response into a plain dictionary
    that can be serialized to JSON.

    Args:
        response: A RunReportResponse or RunRealtimeReportResponse from
            the GA4 Data API.

    Returns:
        A dictionary containing:
            - headers: Dimension and metric header names
            - rows: List of row dicts mapping header names to values
            - row_count: Total number of rows in the full result set
            - totals: Aggregated totals (if available)
            - quota: Property quota usage (if available)
    """
    headers = {
        "dimensions": [h.name for h in response.dimension_headers],
        "metrics": [h.name for h in response.metric_headers],
    }

    rows = []
    for row in response.rows:
        row_data = {}
        for i, dim_value in enumerate(row.dimension_values):
            row_data[headers["dimensions"][i]] = dim_value.value
        for i, metric_value in enumerate(row.metric_values):
            row_data[headers["metrics"][i]] = metric_value.value
        rows.append(row_data)

    result: dict[str, Any] = {
        "headers": headers,
        "rows": rows,
        "row_count": response.row_count,
    }

    # Include totals if available
    if response.totals:
        result["totals"] = [
            {
                headers["metrics"][i]: v.value
                for i, v in enumerate(total.metric_values)
            }
            for total in response.totals
        ]

    # Include property quota if available
    if response.property_quota:
        quota = response.property_quota
        result["quota"] = {
            "tokens_per_day": {
                "consumed": quota.tokens_per_day.consumed,
                "remaining": quota.tokens_per_day.remaining,
            }
            if quota.tokens_per_day
            else None,
            "tokens_per_hour": {
                "consumed": quota.tokens_per_hour.consumed,
                "remaining": quota.tokens_per_hour.remaining,
            }
            if quota.tokens_per_hour
            else None,
        }

    return result


def _build_filter_expression(filter_dict: dict) -> FilterExpression:
    """Build a FilterExpression from a simple dictionary specification.

    Supports three filter types based on the keys present in the dict:

    - String filter: requires 'match_type' key
    - Numeric filter: requires 'numeric_op' key
    - In-list filter: requires 'values' key

    Args:
        filter_dict: A dictionary describing the filter. Must contain 'field'
            and exactly one of the type-specific keys:

            String filter example:
                {"field": "country", "match_type": "EXACT", "value": "United States"}
                match_type options: EXACT, BEGINS_WITH, ENDS_WITH, CONTAINS,
                    FULL_REGEXP, PARTIAL_REGEXP
                Optional: case_sensitive (bool, default False)

            Numeric filter example:
                {"field": "sessions", "numeric_op": "GREATER_THAN", "value": 10}
                numeric_op options: EQUAL, LESS_THAN, LESS_THAN_OR_EQUAL,
                    GREATER_THAN, GREATER_THAN_OR_EQUAL

            In-list filter example:
                {"field": "country", "values": ["United States", "Canada", "Mexico"]}
                Optional: case_sensitive (bool, default False)

    Returns:
        A FilterExpression configured according to the dict specification.

    Raises:
        ValueError: If the dict is missing required keys or has an
            unrecognized filter type.
    """
    field = filter_dict.get("field")
    if not field:
        raise ValueError("Filter dict must contain a 'field' key")

    if "match_type" in filter_dict:
        # String filter
        match_type = getattr(
            StringFilter.MatchType,
            filter_dict.get("match_type", "EXACT"),
        )
        return FilterExpression(
            filter=Filter(
                field_name=field,
                string_filter=StringFilter(
                    match_type=match_type,
                    value=str(filter_dict["value"]),
                    case_sensitive=filter_dict.get("case_sensitive", False),
                ),
            )
        )
    elif "numeric_op" in filter_dict:
        # Numeric filter
        op = getattr(NumericFilter.Operation, filter_dict["numeric_op"])
        value = filter_dict["value"]
        if isinstance(value, int):
            num_value = NumericValue(int64_value=value)
        else:
            num_value = NumericValue(double_value=float(value))
        return FilterExpression(
            filter=Filter(
                field_name=field,
                numeric_filter=NumericFilter(
                    operation=op,
                    value=num_value,
                ),
            )
        )
    elif "values" in filter_dict:
        # In-list filter
        return FilterExpression(
            filter=Filter(
                field_name=field,
                in_list_filter=InListFilter(
                    values=[str(v) for v in filter_dict["values"]],
                    case_sensitive=filter_dict.get("case_sensitive", False),
                ),
            )
        )
    else:
        raise ValueError(
            f"Invalid filter dict for field '{field}': must contain "
            "'match_type', 'numeric_op', or 'values' key"
        )


@mcp.tool()
def ga4_run_report(
    property_id: Optional[str] = None,
    dimensions: list[str] = [],
    metrics: list[str] = [],
    start_date: str = "30daysAgo",
    end_date: str = "today",
    dimension_filter: Optional[dict] = None,
    metric_filter: Optional[dict] = None,
    order_by: Optional[list[str]] = None,
    limit: int = 10000,
    offset: int = 0,
    return_quota: bool = False,
) -> dict[str, Any]:
    """Run a Google Analytics 4 report with dimensions and metrics.

    This is the primary GA4 reporting tool. It queries analytics data for a
    property over a date range, with optional filtering and sorting.

    Args:
        property_id: The GA4 property ID (numeric, e.g. "123456789").
            Uses default from config if not provided.
        dimensions: List of dimension names to include (max 9). Examples:
            - Geographic: "country", "city", "region", "continent"
            - Content: "pagePath", "pageTitle", "landingPage", "hostName"
            - Traffic: "source", "medium", "campaignName", "defaultChannelGroup"
            - User: "newVsReturning", "language", "firstSessionDate"
            - Technology: "browser", "deviceCategory", "operatingSystem", "platform"
            - Time: "date", "dateHour", "month", "dayOfWeek", "hour"
            - Event: "eventName", "isKeyEvent"
            - E-commerce: "itemName", "itemId", "itemBrand", "itemCategory"
        metrics: List of metric names to include. Examples:
            - "activeUsers", "newUsers", "totalUsers", "sessions"
            - "screenPageViews", "eventCount", "engagementRate"
            - "conversions", "totalRevenue", "itemRevenue"
            - "bounceRate", "averageSessionDuration"
        start_date: Report start date. Accepts YYYY-MM-DD format or relative
            strings: "today", "yesterday", "7daysAgo", "30daysAgo", "90daysAgo".
            Default: "30daysAgo".
        end_date: Report end date. Same format as start_date. Default: "today".
        dimension_filter: Optional filter for dimensions. Provide a dict with one of:
            - String filter: {"field": "country", "match_type": "EXACT",
              "value": "United States"}
              match_type options: EXACT, BEGINS_WITH, ENDS_WITH, CONTAINS,
              FULL_REGEXP, PARTIAL_REGEXP
            - Numeric filter: {"field": "sessions", "numeric_op": "GREATER_THAN",
              "value": 10}
              numeric_op options: EQUAL, LESS_THAN, LESS_THAN_OR_EQUAL,
              GREATER_THAN, GREATER_THAN_OR_EQUAL
            - In-list filter: {"field": "country",
              "values": ["United States", "Canada"]}
        metric_filter: Optional filter for metrics (applied post-aggregation).
            Same format as dimension_filter.
        order_by: Optional list of field names to sort by. Prefix with "-"
            for descending order. Examples: ["-sessions", "country"],
            ["-activeUsers"], ["date"].
        limit: Maximum rows to return (default 10000, max 250000).
        offset: Row offset for pagination (0-indexed). Use with limit
            to page through large result sets.
        return_quota: If True, includes API quota usage in the response.

    Returns:
        Dictionary containing:
            - headers: {"dimensions": [...], "metrics": [...]}
            - rows: List of dicts mapping dimension/metric names to values
            - row_count: Total rows matching the query (may exceed limit)
            - totals: Aggregated metric totals (if available)
            - quota: API token usage (if return_quota=True)

    Raises:
        ToolError: If the API request fails or parameters are invalid.

    Examples:
        Basic page views by country (last 7 days):
            ga4_run_report(
                dimensions=["country"],
                metrics=["activeUsers", "sessions", "screenPageViews"],
                start_date="7daysAgo"
            )

        Top landing pages with filter:
            ga4_run_report(
                dimensions=["landingPage"],
                metrics=["sessions", "engagementRate", "conversions"],
                order_by=["-sessions"],
                limit=20
            )

        Traffic sources for a specific country:
            ga4_run_report(
                dimensions=["source", "medium"],
                metrics=["activeUsers", "sessions"],
                dimension_filter={"field": "country", "match_type": "EXACT",
                                  "value": "United States"},
                order_by=["-sessions"]
            )
    """
    try:
        client = get_data_client()
        property_id = resolve_property_id(property_id)

        request = RunReportRequest(
            property=format_property_name(property_id),
            dimensions=[Dimension(name=d) for d in dimensions],
            metrics=[Metric(name=m) for m in metrics],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            limit=limit,
            offset=offset,
            return_property_quota=return_quota,
        )

        if dimension_filter:
            request.dimension_filter = _build_filter_expression(dimension_filter)
        if metric_filter:
            request.metric_filter = _build_filter_expression(metric_filter)

        if order_by:
            orders = []
            for field in order_by:
                desc = field.startswith("-")
                field_name = field.lstrip("-")
                if field_name in dimensions:
                    orders.append(
                        OrderBy(
                            dimension=OrderBy.DimensionOrderBy(
                                dimension_name=field_name,
                            ),
                            desc=desc,
                        )
                    )
                else:
                    orders.append(
                        OrderBy(
                            metric=OrderBy.MetricOrderBy(
                                metric_name=field_name,
                            ),
                            desc=desc,
                        )
                    )
            request.order_bys = orders

        response = client.run_report(request)
        return _parse_report_response(response)

    except GoogleAPICallError as e:
        raise ToolError(f"GA4 report failed: {e.message}") from e
    except ValueError as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def ga4_run_realtime_report(
    property_id: Optional[str] = None,
    dimensions: list[str] = [],
    metrics: list[str] = ["activeUsers"],
    minutes_ago: int = 29,
) -> dict[str, Any]:
    """Run a Google Analytics 4 realtime report.

    Returns live data about current activity on the property within the
    last N minutes. Useful for monitoring current site/app usage.

    Args:
        property_id: The GA4 property ID (numeric, e.g. "123456789").
            Uses default from config if not provided.
        dimensions: List of realtime dimension names. Available options:
            - "country", "city", "countryId", "cityId"
            - "eventName", "minutesAgo"
            - "deviceCategory", "platform"
            - "streamId", "streamName"
            - "audienceId", "audienceName"
            - "appVersion", "unifiedScreenName"
        metrics: List of realtime metric names. Available options:
            - "activeUsers" (default)
            - "eventCount"
            - "keyEvents"
            - "screenPageViews"
        minutes_ago: How many minutes back to include (default 29, max 29).
            Standard GA4 properties support up to 29 minutes;
            GA 360 properties support up to 60 minutes.

    Returns:
        Dictionary containing:
            - headers: {"dimensions": [...], "metrics": [...]}
            - rows: List of dicts mapping dimension/metric names to values
            - row_count: Total rows in the result

    Raises:
        ToolError: If the API request fails or parameters are invalid.

    Examples:
        Current active users by country:
            ga4_run_realtime_report(
                dimensions=["country"],
                metrics=["activeUsers"]
            )

        Active users by page in last 5 minutes:
            ga4_run_realtime_report(
                dimensions=["unifiedScreenName"],
                metrics=["activeUsers", "screenPageViews"],
                minutes_ago=5
            )

        Current events by device category:
            ga4_run_realtime_report(
                dimensions=["deviceCategory", "eventName"],
                metrics=["eventCount"]
            )
    """
    try:
        client = get_data_client()
        property_id = resolve_property_id(property_id)

        request = RunRealtimeReportRequest(
            property=format_property_name(property_id),
            dimensions=[Dimension(name=d) for d in dimensions],
            metrics=[Metric(name=m) for m in metrics],
            minute_ranges=[
                MinuteRange(start_minutes_ago=minutes_ago, end_minutes_ago=0)
            ],
        )

        response = client.run_realtime_report(request)

        # Parse realtime response (same structure but may lack totals/quota)
        headers = {
            "dimensions": [h.name for h in response.dimension_headers],
            "metrics": [h.name for h in response.metric_headers],
        }

        rows = []
        for row in response.rows:
            row_data = {}
            for i, dim_value in enumerate(row.dimension_values):
                row_data[headers["dimensions"][i]] = dim_value.value
            for i, metric_value in enumerate(row.metric_values):
                row_data[headers["metrics"][i]] = metric_value.value
            rows.append(row_data)

        result: dict[str, Any] = {
            "headers": headers,
            "rows": rows,
            "row_count": response.row_count,
        }

        # Include totals if available
        if response.totals:
            result["totals"] = [
                {
                    headers["metrics"][i]: v.value
                    for i, v in enumerate(total.metric_values)
                }
                for total in response.totals
            ]

        return result

    except GoogleAPICallError as e:
        raise ToolError(f"GA4 realtime report failed: {e.message}") from e
    except ValueError as e:
        raise ToolError(str(e)) from e


@mcp.tool()
def ga4_get_metadata(
    property_id: Optional[str] = None,
) -> dict[str, Any]:
    """Get available dimensions and metrics for a GA4 property.

    Returns the full list of dimensions and metrics that can be used in
    reports for the specified property, including custom dimensions and
    metrics if configured.

    Args:
        property_id: The GA4 property ID (numeric, e.g. "123456789").
            Uses default from config if not provided.

    Returns:
        Dictionary containing:
            - dimensions: List of available dimensions, each with:
                - api_name: Name to use in reports (e.g. "country")
                - ui_name: Display name (e.g. "Country")
                - description: What the dimension represents
                - category: Grouping category (e.g. "Geography")
            - metrics: List of available metrics, each with:
                - api_name: Name to use in reports (e.g. "activeUsers")
                - ui_name: Display name (e.g. "Active users")
                - description: What the metric measures
                - category: Grouping category (e.g. "User")
                - type: Data type (e.g. "TYPE_INTEGER", "TYPE_FLOAT")

    Raises:
        ToolError: If the API request fails.

    Examples:
        Get all available dimensions and metrics:
            ga4_get_metadata()

        Get metadata for a specific property:
            ga4_get_metadata(property_id="123456789")
    """
    try:
        client = get_data_client()
        property_id = resolve_property_id(property_id)

        metadata = client.get_metadata(
            name=f"{format_property_name(property_id)}/metadata"
        )

        return {
            "dimensions": [
                {
                    "api_name": d.api_name,
                    "ui_name": d.ui_name,
                    "description": d.description,
                    "category": d.category,
                }
                for d in metadata.dimensions
            ],
            "metrics": [
                {
                    "api_name": m.api_name,
                    "ui_name": m.ui_name,
                    "description": m.description,
                    "category": m.category,
                    "type": m.type_.name if m.type_ else None,
                }
                for m in metadata.metrics
            ],
        }

    except GoogleAPICallError as e:
        raise ToolError(f"GA4 metadata request failed: {e.message}") from e
    except ValueError as e:
        raise ToolError(str(e)) from e
