"""Data stream management tools for Google Analytics.

This module provides MCP tools for managing GA4 data streams including
listing, creating, updating, and deleting web, Android, and iOS data streams.
"""

from typing import Any, Optional

from google.api_core.exceptions import GoogleAPICallError
from google.analytics.admin_v1beta.types import (
    DataStream,
)
from google.protobuf.field_mask_pb2 import FieldMask
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp
from .client import get_admin_client, resolve_property_id, format_property_name


def _stream_to_dict(stream) -> dict[str, Any]:
    """Convert a DataStream protobuf object to a plain dictionary.

    Args:
        stream: A DataStream protobuf instance from the Admin API.

    Returns:
        A dictionary with the stream's key fields, including
        platform-specific data (web, Android, iOS) when present.
    """
    result = {
        "id": stream.name.split("/")[-1] if stream.name else None,
        "name": stream.name,
        "type": stream.type_.name if stream.type_ else None,
        "display_name": stream.display_name,
        "create_time": stream.create_time.isoformat() if stream.create_time else None,
        "update_time": stream.update_time.isoformat() if stream.update_time else None,
    }
    # Add web-specific data
    if stream.web_stream_data:
        result["measurement_id"] = stream.web_stream_data.measurement_id
        result["default_uri"] = stream.web_stream_data.default_uri
    # Add Android-specific data
    if stream.android_app_stream_data:
        result["package_name"] = stream.android_app_stream_data.package_name
    # Add iOS-specific data
    if stream.ios_app_stream_data:
        result["bundle_id"] = stream.ios_app_stream_data.bundle_id
    return result


@mcp.tool()
def ga4_list_data_streams(
    property_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Lists all data streams for a Google Analytics 4 property.

    Args:
        property_id: The GA4 property ID (numeric, e.g. "123456").
            Uses default from config if not provided.

    Returns:
        list[dict]: List of data streams, each containing:
            - id: Stream ID
            - name: Full resource name (properties/X/dataStreams/Y)
            - type: Stream type (WEB_DATA_STREAM, ANDROID_APP_DATA_STREAM, IOS_APP_DATA_STREAM)
            - display_name: Human-readable stream name
            - create_time: Creation timestamp
            - update_time: Last update timestamp
            - measurement_id: Web measurement ID (e.g. "G-XXXXXXX") if web stream
            - default_uri: Default URI if web stream
            - package_name: Android package name if Android stream
            - bundle_id: iOS bundle ID if iOS stream

    Raises:
        ToolError: If the API request fails.
    """
    try:
        property_id = resolve_property_id(property_id)
        client = get_admin_client()
        streams = client.list_data_streams(
            parent=format_property_name(property_id),
        )
        return [_stream_to_dict(stream) for stream in streams]
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to list data streams: {e}") from e


@mcp.tool()
def ga4_get_data_stream(
    stream_name: str,
) -> dict[str, Any]:
    """Gets detailed information about a specific GA4 data stream.

    Args:
        stream_name: Full resource name of the data stream,
            e.g. "properties/123456/dataStreams/789".

    Returns:
        dict: Data stream details including:
            - id: Stream ID
            - name: Full resource name
            - type: Stream type
            - display_name: Human-readable stream name
            - create_time: Creation timestamp
            - update_time: Last update timestamp
            - measurement_id: Web measurement ID if web stream
            - default_uri: Default URI if web stream
            - package_name: Android package name if Android stream
            - bundle_id: iOS bundle ID if iOS stream

    Raises:
        ToolError: If the stream is not found or API request fails.
    """
    try:
        client = get_admin_client()
        stream = client.get_data_stream(name=stream_name)
        return _stream_to_dict(stream)
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to get data stream: {e}") from e


@mcp.tool()
def ga4_create_web_data_stream(
    property_id: Optional[str] = None,
    display_name: str = "",
    default_uri: str = "",
) -> dict[str, Any]:
    """Creates a new web data stream on a GA4 property.

    The created stream will include a generated measurement ID (e.g. "G-XXXXXXX")
    that you can use to install the Google Analytics tag on your website.

    Args:
        property_id: The GA4 property ID (numeric, e.g. "123456").
            Uses default from config if not provided.
        display_name: Human-readable name for the data stream.
        default_uri: The default URI for the web stream (e.g. "https://example.com").

    Returns:
        dict: Created data stream details including:
            - id: Stream ID
            - name: Full resource name
            - type: WEB_DATA_STREAM
            - display_name: Stream name
            - measurement_id: Generated measurement ID (e.g. "G-XXXXXXX")
            - default_uri: The configured default URI

    Raises:
        ToolError: If the API request fails.
    """
    try:
        property_id = resolve_property_id(property_id)
        client = get_admin_client()
        stream = DataStream(
            type_=DataStream.DataStreamType.WEB_DATA_STREAM,
            display_name=display_name,
            web_stream_data=DataStream.WebStreamData(default_uri=default_uri),
        )
        created = client.create_data_stream(
            parent=format_property_name(property_id),
            data_stream=stream,
        )
        return _stream_to_dict(created)
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to create web data stream: {e}") from e


@mcp.tool()
def ga4_create_android_data_stream(
    property_id: Optional[str] = None,
    display_name: str = "",
    package_name: str = "",
) -> dict[str, Any]:
    """Creates a new Android app data stream on a GA4 property.

    Args:
        property_id: The GA4 property ID (numeric, e.g. "123456").
            Uses default from config if not provided.
        display_name: Human-readable name for the data stream.
        package_name: The Android app package name (e.g. "com.example.app").

    Returns:
        dict: Created data stream details including:
            - id: Stream ID
            - name: Full resource name
            - type: ANDROID_APP_DATA_STREAM
            - display_name: Stream name
            - package_name: The configured package name

    Raises:
        ToolError: If the API request fails.
    """
    try:
        property_id = resolve_property_id(property_id)
        client = get_admin_client()
        stream = DataStream(
            type_=DataStream.DataStreamType.ANDROID_APP_DATA_STREAM,
            display_name=display_name,
            android_app_stream_data=DataStream.AndroidAppStreamData(
                package_name=package_name,
            ),
        )
        created = client.create_data_stream(
            parent=format_property_name(property_id),
            data_stream=stream,
        )
        return _stream_to_dict(created)
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to create Android data stream: {e}") from e


@mcp.tool()
def ga4_create_ios_data_stream(
    property_id: Optional[str] = None,
    display_name: str = "",
    bundle_id: str = "",
) -> dict[str, Any]:
    """Creates a new iOS app data stream on a GA4 property.

    Args:
        property_id: The GA4 property ID (numeric, e.g. "123456").
            Uses default from config if not provided.
        display_name: Human-readable name for the data stream.
        bundle_id: The iOS app bundle ID (e.g. "com.example.app").

    Returns:
        dict: Created data stream details including:
            - id: Stream ID
            - name: Full resource name
            - type: IOS_APP_DATA_STREAM
            - display_name: Stream name
            - bundle_id: The configured bundle ID

    Raises:
        ToolError: If the API request fails.
    """
    try:
        property_id = resolve_property_id(property_id)
        client = get_admin_client()
        stream = DataStream(
            type_=DataStream.DataStreamType.IOS_APP_DATA_STREAM,
            display_name=display_name,
            ios_app_stream_data=DataStream.IosAppStreamData(
                bundle_id=bundle_id,
            ),
        )
        created = client.create_data_stream(
            parent=format_property_name(property_id),
            data_stream=stream,
        )
        return _stream_to_dict(created)
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to create iOS data stream: {e}") from e


@mcp.tool()
def ga4_update_data_stream(
    stream_name: str,
    display_name: Optional[str] = None,
) -> dict[str, Any]:
    """Updates an existing GA4 data stream.

    Only the display_name can be updated. The stream type and
    platform-specific data (URI, package name, bundle ID) are immutable.

    Args:
        stream_name: Full resource name of the data stream,
            e.g. "properties/123456/dataStreams/789".
        display_name: New human-readable name for the data stream.

    Returns:
        dict: Updated data stream details.

    Raises:
        ToolError: If no fields to update or the API request fails.
    """
    try:
        if display_name is None:
            raise ToolError("No fields to update. Provide display_name.")

        client = get_admin_client()
        stream = DataStream(
            name=stream_name,
            display_name=display_name,
        )
        mask = FieldMask(paths=["display_name"])
        updated = client.update_data_stream(
            data_stream=stream,
            update_mask=mask,
        )
        return _stream_to_dict(updated)
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to update data stream: {e}") from e


@mcp.tool()
def ga4_delete_data_stream(
    stream_name: str,
) -> dict[str, Any]:
    """Deletes a GA4 data stream.

    This permanently removes the data stream from the property.
    Historical data collected by the stream is retained in the property.

    Args:
        stream_name: Full resource name of the data stream,
            e.g. "properties/123456/dataStreams/789".

    Returns:
        dict: Deletion status:
            - status: "deleted"
            - name: The deleted stream's resource name

    Raises:
        ToolError: If the stream is not found or API request fails.
    """
    try:
        client = get_admin_client()
        client.delete_data_stream(name=stream_name)
        return {"status": "deleted", "name": stream_name}
    except GoogleAPICallError as e:
        raise ToolError(f"Failed to delete data stream: {e}") from e
