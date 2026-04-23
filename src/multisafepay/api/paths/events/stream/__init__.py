# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Event stream contracts for the events path."""

from __future__ import annotations

import json

from multisafepay.api.paths.events.stream.response import Event, EventData
from multisafepay.client.sse import (
    ServerSentEvent,
    ServerSentEventStream,
    StreamingResponse,
)
from typing_extensions import Self


def _deserialize_event_payload(raw_payload: str | None) -> object | None:
    """Parse raw SSE data for this path and fall back to plain text."""
    if raw_payload is None:
        return None

    try:
        return json.loads(raw_payload)
    except json.JSONDecodeError:
        return raw_payload


def _to_event(server_sent_event: ServerSentEvent) -> Event:
    """Adapt a generic SSE message into the events-path response model."""
    event = Event.from_dict(
        {
            "event": server_sent_event.event,
            "data": _deserialize_event_payload(server_sent_event.data),
            "event_id": server_sent_event.event_id,
            "retry": server_sent_event.retry,
            "raw_data": server_sent_event.raw_data,
        },
    )
    if event is None:
        raise ValueError("Unable to adapt SSE payload to Event.")
    return event


class EventStream:
    """Iterator over events received from the MultiSafepay SSE endpoint."""

    def __init__(
        self: EventStream,
        response: StreamingResponse | None = None,
        stream: ServerSentEventStream | None = None,
    ) -> None:
        """Initialize the stream from an HTTP response or generic SSE stream."""
        if stream is not None:
            self._stream = stream
            return

        if response is None:
            raise ValueError(
                "response is required when stream is not provided.",
            )

        self._stream = ServerSentEventStream(response=response)

    @classmethod
    def _from_stream(
        cls: type[EventStream],
        stream: ServerSentEventStream,
    ) -> EventStream:
        """Build an EventStream around an already-open generic SSE stream."""
        return cls(stream=stream)

    @classmethod
    def open(
        cls: type[EventStream],
        events_token: str,
        events_stream_url: str,
        last_event_id: str | None = None,
        timeout: float = 30.0,
    ) -> EventStream:
        """Open a new SSE stream using the event token and stream URL."""
        headers = {
            "Accept": "text/event-stream",
            "Cache-Control": "no-cache",
            "Authorization": f"Bearer {events_token}",
        }
        if last_event_id is not None:
            headers["Last-Event-ID"] = last_event_id

        stream = ServerSentEventStream.open(
            url=events_stream_url,
            headers=headers,
            timeout=timeout,
        )
        return cls._from_stream(stream)

    @property
    def closed(self: EventStream) -> bool:
        """Return whether this stream is already closed."""
        return self._stream.closed

    def close(self: EventStream) -> None:
        """Close the underlying HTTP response stream."""
        self._stream.close()

    def __iter__(self: EventStream) -> EventStream:
        """Return self as an iterator over events."""
        return self

    def __next__(self: EventStream) -> Event:
        """Read the next SSE message and return it as an Event."""
        return _to_event(next(self._stream))

    def __enter__(self: Self) -> Self:
        """Support context manager protocol."""
        return self

    def __exit__(self: EventStream, *args: object) -> None:
        """Close stream when exiting context manager."""
        self.close()


__all__ = [
    "Event",
    "EventData",
    "EventStream",
]
