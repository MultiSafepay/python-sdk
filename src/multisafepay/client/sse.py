# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Generic Server-Sent Events support utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Protocol
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from typing_extensions import Self


class StreamingResponse(Protocol):
    """Protocol for the minimal stream response interface used by SSE streams."""

    def readline(self: StreamingResponse) -> bytes:
        """Read one line from the stream response."""

    def close(self: StreamingResponse) -> None:
        """Close the stream response."""


@dataclass(frozen=True)
class ServerSentEvent:
    """Generic representation of one SSE message."""

    event: str | None = None
    data: str | None = None
    event_id: str | None = None
    retry: int | None = None
    raw_data: str | None = None


@dataclass
class _ServerSentEventBuilder:
    """Mutable builder used while parsing one SSE message."""

    _FIELD_HANDLERS: ClassVar[dict[str, str]] = {
        "event": "_consume_event",
        "data": "_consume_data",
        "id": "_consume_id",
        "retry": "_consume_retry",
    }

    event_name: str | None = None
    event_id: str | None = None
    event_retry: int | None = None
    data_lines: list[str] = field(default_factory=list)
    has_fields: bool = False

    def consume_line(self: _ServerSentEventBuilder, line: str) -> None:
        """Consume one SSE line and update the builder state."""
        if line.startswith(":"):
            return

        field_name, field_value = _parse_line(line)
        if field_name is None:
            return

        handler_name = self._FIELD_HANDLERS.get(field_name)
        if handler_name is None:
            return

        getattr(self, handler_name)(field_value)

    def _consume_event(
        self: _ServerSentEventBuilder,
        field_value: str,
    ) -> None:
        """Consume the SSE event field."""
        self.has_fields = True
        self.event_name = field_value

    def _consume_data(self: _ServerSentEventBuilder, field_value: str) -> None:
        """Consume one SSE data line."""
        self.has_fields = True
        self.data_lines.append(field_value)

    def _consume_id(self: _ServerSentEventBuilder, field_value: str) -> None:
        """Consume the SSE id field."""
        self.has_fields = True
        self.event_id = field_value

    def _consume_retry(
        self: _ServerSentEventBuilder,
        field_value: str,
    ) -> None:
        """Consume the SSE retry field when it is a valid integer."""
        try:
            self.event_retry = int(field_value)
        except ValueError:
            return

        self.has_fields = True

    def build(self: _ServerSentEventBuilder) -> ServerSentEvent | None:
        """Build an immutable SSE message or None when no message exists."""
        if not self.has_fields and not self.data_lines:
            return None

        raw_data = "\n".join(self.data_lines) if self.data_lines else None
        return ServerSentEvent(
            event=self.event_name,
            data=raw_data,
            event_id=self.event_id,
            retry=self.event_retry,
            raw_data=raw_data,
        )


class ServerSentEventStream:
    """Iterator over messages received from a generic SSE endpoint."""

    def __init__(
        self: ServerSentEventStream,
        response: StreamingResponse,
    ) -> None:
        """Initialize the stream from an already-open HTTP response."""
        self._response = response
        self._closed = False

    @classmethod
    def open(
        cls: type[ServerSentEventStream],
        url: str,
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
    ) -> ServerSentEventStream:
        """Open a new SSE stream using a URL and optional headers."""
        cls._validate_url(url)

        request = Request(  # noqa: S310
            url=url,
            headers=headers or {},
            method="GET",
        )
        # Keep the response open; close manages the lifecycle.
        # pylint: disable=consider-using-with
        response = urlopen(request, timeout=timeout)  # noqa: S310
        # pylint: enable=consider-using-with

        return cls(response=response)

    @staticmethod
    def _validate_url(url: str) -> None:
        """Validate the stream URL before opening the network connection."""
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Invalid SSE URL.")

    @property
    def closed(self: ServerSentEventStream) -> bool:
        """Return whether this stream is already closed."""
        return self._closed

    def close(self: ServerSentEventStream) -> None:
        """Close the underlying HTTP response stream."""
        if self._closed:
            return

        self._response.close()
        self._closed = True

    def __iter__(self: ServerSentEventStream) -> ServerSentEventStream:
        """Return self as an iterator over SSE messages."""
        return self

    def __next__(self: ServerSentEventStream) -> ServerSentEvent:
        """Read the next SSE message and return it."""
        if self._closed:
            raise StopIteration

        builder = _ServerSentEventBuilder()
        while True:
            line = self._read_line()
            if line is None:
                self.close()
                raise StopIteration

            if line == "":
                event = builder.build()
                if event is not None:
                    return event
                builder = _ServerSentEventBuilder()
                continue

            builder.consume_line(line)

    def _read_line(self: ServerSentEventStream) -> str | None:
        """Read and decode one line from the underlying stream response."""
        raw_line = self._response.readline()
        if not raw_line:
            return None

        return raw_line.decode("utf-8", errors="replace").rstrip("\r\n")

    def __enter__(self: Self) -> Self:
        """Support context manager protocol."""
        return self

    def __exit__(self: ServerSentEventStream, *args: object) -> None:
        """Close stream when exiting context manager."""
        self.close()


def _parse_line(line: str) -> tuple[str | None, str]:
    """Parse one SSE line into field and value parts."""
    if ":" not in line:
        return line or None, ""

    field_name, field_value = line.split(":", 1)
    if field_name == "":
        return None, ""
    if field_value.startswith(" "):
        field_value = field_value[1:]

    return field_name, field_value
