# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for event-path stream contracts."""

from __future__ import annotations

import io

import pytest

from multisafepay.api.paths.events.stream import Event, EventData, EventStream
from multisafepay.client.sse import ServerSentEventStream

EVENTS_STREAM_URL = "https://testapi.multisafepay.com/events/stream/"
EVENTS_TOKEN = "events-token"
LAST_EVENT_ID = "last-10"
PING_PAYLOAD = b"data: ping\n\n"


class _FakeStreamingResponse:
    """Small streaming response stub used for unit testing."""

    def __init__(self: _FakeStreamingResponse, payload: bytes) -> None:
        self._buffer = io.BytesIO(payload)
        self.closed = False

    def readline(self: _FakeStreamingResponse) -> bytes:
        return self._buffer.readline()

    def close(self: _FakeStreamingResponse) -> None:
        self._buffer.close()
        self.closed = True


def test_open_builds_expected_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    """Build event-specific auth headers before opening the generic SSE stream."""
    captured: dict[str, object] = {}

    def fake_open(
        url: str,
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
    ) -> ServerSentEventStream:
        captured["url"] = url
        captured["headers"] = headers
        captured["timeout"] = timeout
        return ServerSentEventStream(
            response=_FakeStreamingResponse(PING_PAYLOAD),
        )

    monkeypatch.setattr(
        "multisafepay.api.paths.events.stream.ServerSentEventStream.open",
        fake_open,
    )

    stream = EventStream.open(
        events_token=EVENTS_TOKEN,
        events_stream_url=EVENTS_STREAM_URL,
        last_event_id=LAST_EVENT_ID,
        timeout=9.5,
    )
    event = next(stream)

    assert isinstance(event, Event)
    assert event.data == "ping"
    assert captured["url"] == EVENTS_STREAM_URL
    assert captured["timeout"] == 9.5
    headers = captured["headers"]
    assert headers["Authorization"] == f"Bearer {EVENTS_TOKEN}"
    assert headers["Accept"] == "text/event-stream"
    assert headers["Cache-Control"] == "no-cache"
    assert headers["Last-Event-ID"] == LAST_EVENT_ID


def test_wraps_generic_sse_messages_as_event_contracts() -> None:
    """Adapt generic SSE messages into the events-path Event contract."""
    payload = (
        b"event: order.updated\n"
        b"id: 15\n"
        b"retry: 1000\n"
        b'data: {"status": "completed", "order_id": "123"}\n\n'
    )
    stream = EventStream(response=_FakeStreamingResponse(payload))

    event = next(stream)

    assert isinstance(event, Event)
    assert event.event == "order.updated"
    assert event.event_id == "15"
    assert event.retry == 1000
    assert isinstance(event.data, EventData)
    assert event.data.status == "completed"
    assert event.data.order_id == "123"


def test_event_from_dict_adapts_nested_payloads() -> None:
    """Build nested event payload models through the common from_dict path."""
    event = Event.from_dict(
        {
            "event": "order.updated",
            "data": {
                "status": "processing",
                "data": {
                    "status": "completed",
                    "order_id": "nested-1",
                },
            },
        },
    )

    assert event is not None
    assert isinstance(event.data, EventData)
    assert event.data.status == "processing"
    assert isinstance(event.data.data, EventData)
    assert event.data.data.status == "completed"
    assert event.data.data.order_id == "nested-1"


def test_event_data_from_dict_adapts_nested_list_payloads() -> None:
    """Build nested EventData items when payload data contains a list."""
    payload = EventData.from_dict(
        {
            "status": "processing",
            "data": [
                {
                    "status": "completed",
                    "order_id": "nested-2",
                },
                "keep-me",
            ],
        },
    )

    assert payload is not None
    assert payload.status == "processing"
    assert isinstance(payload.data, list)
    assert isinstance(payload.data[0], EventData)
    assert payload.data[0].status == "completed"
    assert payload.data[0].order_id == "nested-2"
    assert payload.data[1] == "keep-me"


def test_event_from_dict_adapts_list_payload_items() -> None:
    """Build top-level event payload lists through the common from_dict path."""
    event = Event.from_dict(
        {
            "event": "order.batch",
            "data": [
                {
                    "status": "completed",
                    "order_id": "batch-1",
                },
                "tail",
            ],
        },
    )

    assert event is not None
    assert isinstance(event.data, list)
    assert isinstance(event.data[0], EventData)
    assert event.data[0].status == "completed"
    assert event.data[0].order_id == "batch-1"
    assert event.data[1] == "tail"


def test_from_dict_returns_none_for_none_payload() -> None:
    """Return None when from_dict receives None input."""
    assert Event.from_dict(None) is None
    assert EventData.from_dict(None) is None


def test_closes_wrapped_stream_on_eof() -> None:
    """Close the wrapped generic stream when EOF is reached."""
    response = _FakeStreamingResponse(payload=b"")
    stream = EventStream(response=response)

    with pytest.raises(StopIteration):
        next(stream)

    assert response.closed is True
    assert stream.closed is True
