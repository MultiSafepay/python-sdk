# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for generic SSE support."""

from __future__ import annotations

import io

import pytest

from multisafepay.client.sse import ServerSentEventStream

SSE_URL = "https://testapi.multisafepay.com/events/stream/"
PING_PAYLOAD = b"data: ping\n\n"
INVALID_SSE_URL = "not-a-valid-url"
INVALID_SSE_URL_ERROR = "Invalid SSE URL"


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
    """Open a generic SSE stream using the provided URL and headers."""
    captured: dict[str, object] = {}

    def fake_urlopen(request: object, timeout: float = 30.0) -> object:
        request_headers = {
            key.lower(): value
            for key, value in dict(request.header_items()).items()
        }
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["headers"] = request_headers
        return _FakeStreamingResponse(payload=PING_PAYLOAD)

    monkeypatch.setattr(
        "multisafepay.client.sse.urlopen",
        fake_urlopen,
    )

    stream = ServerSentEventStream.open(
        url=SSE_URL,
        headers={
            "Authorization": "Bearer events-token",
            "Accept": "text/event-stream",
        },
        timeout=9.5,
    )
    event = next(stream)

    assert event.data == "ping"
    assert captured["url"] == SSE_URL
    assert captured["timeout"] == 9.5
    headers = captured["headers"]
    assert headers["authorization"] == "Bearer events-token"
    assert headers["accept"] == "text/event-stream"


def test_parses_sse_fields_and_preserves_raw_data() -> None:
    """Parse generic SSE fields while keeping data as raw SSE text."""
    payload = (
        b"event: order.updated\n"
        b"id: 15\n"
        b"retry: 1000\n"
        b'data: {"status": "completed", "order_id": "123"}\n\n'
    )
    stream = ServerSentEventStream(response=_FakeStreamingResponse(payload))

    event = next(stream)

    assert event.event == "order.updated"
    assert event.event_id == "15"
    assert event.retry == 1000
    assert event.data == '{"status": "completed", "order_id": "123"}'
    assert event.raw_data == '{"status": "completed", "order_id": "123"}'


def test_rejects_invalid_sse_url() -> None:
    """Reject opening streams with invalid URL format."""
    with pytest.raises(ValueError, match=INVALID_SSE_URL_ERROR):
        ServerSentEventStream.open(url=INVALID_SSE_URL)


def test_context_manager_closes_stream_on_exit() -> None:
    """Close the underlying stream when context manager exits."""
    response = _FakeStreamingResponse(payload=PING_PAYLOAD)

    with ServerSentEventStream(response=response) as stream:
        assert next(stream).data == "ping"

    assert response.closed is True
    assert stream.closed is True


def test_ignores_unknown_fields_and_invalid_retry() -> None:
    """Ignore unsupported SSE fields instead of emitting empty events."""
    response = _FakeStreamingResponse(payload=b"foo: bar\nretry: nope\n\n")
    stream = ServerSentEventStream(response=response)

    with pytest.raises(StopIteration):
        next(stream)

    assert response.closed is True
    assert stream.closed is True
