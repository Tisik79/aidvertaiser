"""GA4 Measurement Protocol tools for sending server-side events.

This module provides MCP tools for sending events to Google Analytics 4
via the Measurement Protocol. This is used for server-side event tracking,
offline conversions, and other scenarios where client-side tracking is
not possible or appropriate.

Reference:
    https://developers.google.com/analytics/devguides/collection/protocol/ga4
"""

from typing import Any, Optional

import requests
from mcp.server.fastmcp.exceptions import ToolError

from ..server import mcp

MP_COLLECT_URL = "https://www.google-analytics.com/mp/collect"
MP_DEBUG_URL = "https://www.google-analytics.com/debug/mp/collect"


def _build_mp_payload(
    client_id: str,
    events: list[dict[str, Any]],
    user_id: Optional[str] = None,
) -> dict[str, Any]:
    """Build the Measurement Protocol JSON payload.

    Args:
        client_id: A unique identifier for the client/device. For web,
            this is typically the _ga cookie value. For server-side,
            use any stable unique identifier.
        events: List of event dicts, each with 'name' and optional 'params'.
        user_id: Optional User-ID for cross-device/session measurement.

    Returns:
        The JSON payload dict ready to POST to the MP endpoint.
    """
    payload: dict[str, Any] = {
        "client_id": client_id,
        "events": events,
    }
    if user_id:
        payload["user_id"] = user_id
    return payload


def _send_mp_request(
    measurement_id: str,
    api_secret: str,
    payload: dict[str, Any],
    debug: bool = False,
) -> dict[str, Any]:
    """Send a request to the Measurement Protocol endpoint.

    Args:
        measurement_id: The GA4 Measurement ID (e.g. "G-XXXXXXX").
        api_secret: The Measurement Protocol API secret.
        payload: The JSON payload to send.
        debug: If True, send to the debug endpoint for validation.

    Returns:
        A dict with status info. Debug mode returns validation messages.

    Raises:
        ToolError: If the HTTP request fails.
    """
    url = MP_DEBUG_URL if debug else MP_COLLECT_URL
    params = {
        "measurement_id": measurement_id,
        "api_secret": api_secret,
    }

    try:
        response = requests.post(
            url,
            json=payload,
            params=params,
            timeout=30,
        )
    except requests.RequestException as e:
        raise ToolError(f"Measurement Protocol request failed: {e}") from e

    result: dict[str, Any] = {
        "status_code": response.status_code,
        "success": response.status_code == 204
        or (debug and response.status_code == 200),
    }

    if debug and response.text:
        try:
            result["validation_messages"] = response.json()
        except ValueError:
            result["response_body"] = response.text
    elif response.status_code != 204:
        result["success"] = False
        result["error"] = f"Unexpected status code: {response.status_code}"
        if response.text:
            result["response_body"] = response.text

    return result


@mcp.tool()
def ga4_send_measurement_protocol_event(
    measurement_id: str,
    api_secret: str,
    client_id: str,
    event_name: str,
    event_params: Optional[dict[str, Any]] = None,
    user_id: Optional[str] = None,
    debug: bool = False,
) -> dict[str, Any]:
    """Sends a single event to GA4 via the Measurement Protocol.

    Use this for server-side event tracking when client-side gtag.js
    is not available. Common use cases include offline conversions,
    server-to-server tracking, and CRM event forwarding.

    The Measurement Protocol does NOT require OAuth — it uses an API secret
    that you create via ga4_create_measurement_protocol_secret.

    Args:
        measurement_id: The GA4 Measurement ID (e.g. "G-XXXXXXX").
            Find this in your GA4 data stream settings.
        api_secret: The Measurement Protocol API secret.
            Create one via ga4_create_measurement_protocol_secret.
        client_id: A unique identifier for the user/device. Use any
            stable unique string (e.g. CRM user ID, session ID).
            For web, this matches the _ga cookie value format.
        event_name: The event name (e.g. "purchase", "generate_lead",
            "sign_up", "offline_conversion"). Must follow GA4 event
            naming rules: alphanumeric + underscores, max 40 chars.
        event_params: Optional dict of event parameters. Keys must be
            alphanumeric + underscores (max 40 chars). Values can be
            strings (max 100 chars) or numbers. Example:
            {"value": 99.99, "currency": "USD", "transaction_id": "T123"}
        user_id: Optional User-ID for cross-device measurement.
            Must be a non-PII identifier (e.g. hashed email, CRM ID).
        debug: If True, sends to the debug endpoint which validates
            the payload and returns detailed error messages instead
            of actually recording the event. Use this to test your
            integration before going live.

    Returns:
        dict: Result with:
            - status_code: HTTP status code (204 = success, 200 for debug)
            - success: Whether the request was accepted
            - validation_messages: (debug mode only) Validation results
              showing any errors in the payload

    Raises:
        ToolError: If the HTTP request fails.
    """
    event: dict[str, Any] = {"name": event_name}
    if event_params:
        event["params"] = event_params

    payload = _build_mp_payload(
        client_id=client_id,
        events=[event],
        user_id=user_id,
    )

    return _send_mp_request(
        measurement_id=measurement_id,
        api_secret=api_secret,
        payload=payload,
        debug=debug,
    )


@mcp.tool()
def ga4_send_measurement_protocol_batch(
    measurement_id: str,
    api_secret: str,
    client_id: str,
    events: list[dict[str, Any]],
    user_id: Optional[str] = None,
    debug: bool = False,
) -> dict[str, Any]:
    """Sends multiple events to GA4 via the Measurement Protocol in a single request.

    Use this to batch multiple events for the same user/client. The GA4
    Measurement Protocol supports up to 25 events per request.

    Each event in the list must have a "name" key and optionally a "params" key.
    Example events list:
    [
        {"name": "page_view", "params": {"page_title": "Home"}},
        {"name": "purchase", "params": {"value": 49.99, "currency": "CZK", "transaction_id": "T456"}},
        {"name": "custom_event", "params": {"category": "engagement"}}
    ]

    Args:
        measurement_id: The GA4 Measurement ID (e.g. "G-XXXXXXX").
        api_secret: The Measurement Protocol API secret.
        client_id: A unique identifier for the user/device.
        events: List of event dicts. Each must have:
            - name (str): Event name (required)
            - params (dict): Event parameters (optional)
            Maximum 25 events per request.
        user_id: Optional User-ID for cross-device measurement.
        debug: If True, validates the payload without recording events.

    Returns:
        dict: Result with:
            - status_code: HTTP status code
            - success: Whether the request was accepted
            - event_count: Number of events sent
            - validation_messages: (debug mode only) Validation results

    Raises:
        ToolError: If the events list is empty, exceeds 25, has invalid
            format, or if the HTTP request fails.
    """
    if not events:
        raise ToolError("Events list cannot be empty.")
    if len(events) > 25:
        raise ToolError(
            f"Maximum 25 events per request, got {len(events)}. "
            "Split into multiple calls."
        )

    # Validate event structure
    for i, event in enumerate(events):
        if not isinstance(event, dict):
            raise ToolError(
                f"Event at index {i} must be a dict, got {type(event).__name__}."
            )
        if "name" not in event:
            raise ToolError(f"Event at index {i} is missing required 'name' key.")

    payload = _build_mp_payload(
        client_id=client_id,
        events=events,
        user_id=user_id,
    )

    result = _send_mp_request(
        measurement_id=measurement_id,
        api_secret=api_secret,
        payload=payload,
        debug=debug,
    )
    result["event_count"] = len(events)
    return result
