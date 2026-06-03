# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for order response event fields compatibility."""

from typing import Optional

from multisafepay.api.paths.orders.response.order_response import Order

PLURAL_EVENTS_TOKEN = "token-123"
PLURAL_EVENTS_URL = "wss://testapi.multisafepay.com/events/"
PLURAL_EVENTS_STREAM_URL = "https://testapi.multisafepay.com/events/stream/"
LEGACY_EVENTS_TOKEN = "legacy-token"
LEGACY_EVENTS_URL = "wss://legacy.example.com/events/"
LEGACY_EVENTS_STREAM_URL = "https://legacy.example.com/events/stream/"


def _assert_event_fields(
    order: Optional[Order],
    expected_token: str,
    expected_url: str,
    expected_stream_url: str,
) -> None:
    """Assert both plural and legacy event fields are populated consistently."""
    assert order is not None

    assert order.events_token == expected_token
    assert order.events_url == expected_url
    assert order.events_stream_url == expected_stream_url
    assert order.event_token == expected_token
    assert order.event_url == expected_url
    assert order.event_stream_url == expected_stream_url


def test_from_dict_maps_plural_event_fields_to_legacy_aliases() -> None:
    """Map events_* fields to both plural and legacy singular attributes."""
    data = {
        "order_id": "order-1",
        "events_token": PLURAL_EVENTS_TOKEN,
        "events_url": PLURAL_EVENTS_URL,
        "events_stream_url": PLURAL_EVENTS_STREAM_URL,
    }

    order = Order.from_dict(data)

    _assert_event_fields(
        order=order,
        expected_token=PLURAL_EVENTS_TOKEN,
        expected_url=PLURAL_EVENTS_URL,
        expected_stream_url=PLURAL_EVENTS_STREAM_URL,
    )


def test_from_dict_maps_legacy_event_fields_to_plural_names() -> None:
    """Map event_* fields to newer plural names for consistency."""
    data = {
        "order_id": "order-2",
        "event_token": LEGACY_EVENTS_TOKEN,
        "event_url": LEGACY_EVENTS_URL,
        "event_stream_url": LEGACY_EVENTS_STREAM_URL,
    }

    order = Order.from_dict(data)

    _assert_event_fields(
        order=order,
        expected_token=LEGACY_EVENTS_TOKEN,
        expected_url=LEGACY_EVENTS_URL,
        expected_stream_url=LEGACY_EVENTS_STREAM_URL,
    )
