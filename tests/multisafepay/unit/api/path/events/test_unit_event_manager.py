# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for event manager subscription helpers."""

from typing import Optional
from unittest.mock import MagicMock

import pytest

from multisafepay.api.paths.events.event_manager import EventManager
from multisafepay.api.paths.orders.response.order_response import Order

TEST_EVENTS_STREAM_URL = "https://testapi.multisafepay.com/events/stream/"
ORDER_EVENTS_STREAM_URL = "https://stream.example/events/stream/"
LEGACY_EVENTS_STREAM_URL = "https://legacy.example/events/stream/"
MISSING_EVENTS_ERROR = "events_token/events_stream_url"


def _patch_event_stream_open(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[dict[str, object], object]:
    """Patch EventStream.open and return capture dict plus sentinel stream."""
    captured: dict[str, object] = {}
    expected_stream = object()

    def fake_open(
        events_token: str,
        events_stream_url: str,
        last_event_id: Optional[str] = None,
        timeout: float = 30.0,
    ) -> object:
        captured["events_token"] = events_token
        captured["events_stream_url"] = events_stream_url
        captured["last_event_id"] = last_event_id
        captured["timeout"] = timeout
        return expected_stream

    monkeypatch.setattr(
        "multisafepay.api.paths.events.event_manager.EventStream.open",
        fake_open,
    )

    return captured, expected_stream


def test_subscribe_events_delegates_to_stream_open(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Delegate direct subscriptions to EventStream.open."""
    captured, expected_stream = _patch_event_stream_open(monkeypatch)

    manager = EventManager(MagicMock())
    stream = manager.subscribe_events(
        events_token="token-abc",
        events_stream_url=TEST_EVENTS_STREAM_URL,
        last_event_id="last-15",
        timeout=10.0,
    )

    assert stream is expected_stream
    assert captured["events_token"] == "token-abc"
    assert captured["events_stream_url"] == TEST_EVENTS_STREAM_URL
    assert captured["last_event_id"] == "last-15"
    assert captured["timeout"] == 10.0


def test_subscribe_order_events_uses_plural_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Read events credentials from events_* fields when present."""
    captured, expected_stream = _patch_event_stream_open(monkeypatch)

    manager = EventManager(MagicMock())
    order = Order(
        order_id="order-1",
        events_token="events-token",
        events_stream_url=ORDER_EVENTS_STREAM_URL,
    )

    stream = manager.subscribe_order_events(order)

    assert stream is expected_stream
    assert captured["events_token"] == "events-token"
    assert captured["events_stream_url"] == ORDER_EVENTS_STREAM_URL


def test_subscribe_order_events_falls_back_to_legacy_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Support old event_* field names for backward compatibility."""
    captured, expected_stream = _patch_event_stream_open(monkeypatch)

    manager = EventManager(MagicMock())
    order = Order(
        order_id="order-2",
        event_token="legacy-token",
        event_stream_url=LEGACY_EVENTS_STREAM_URL,
    )

    stream = manager.subscribe_order_events(order)

    assert stream is expected_stream
    assert captured["events_token"] == "legacy-token"
    assert captured["events_stream_url"] == LEGACY_EVENTS_STREAM_URL


def test_subscribe_order_events_requires_token_and_stream_url() -> None:
    """Raise a clear error when event credentials are missing in order."""
    manager = EventManager(MagicMock())
    order = Order(order_id="order-3")

    with pytest.raises(
        ValueError,
        match=MISSING_EVENTS_ERROR,
    ):
        manager.subscribe_order_events(order)
