"""
Test-only mock HTTP transport utilities.

These helpers intentionally live under `tests/` (not `src/`) so they are not
shipped as part of the public SDK package.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


class MockTransportError(RuntimeError):
    """Raised for invalid mock transport usage."""


class MockHTTPError(RuntimeError):
    """Raised when a mock response represents an HTTP error status."""


@dataclass
class MockResponse:
    """Minimal response object compatible with the SDK's expectations."""

    status_code: int = 200
    json_data: dict[str, object] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)

    def json(self: MockResponse) -> dict[str, object]:
        """Return configured JSON payload."""
        return self.json_data

    def raise_for_status(self: MockResponse) -> None:
        """Raise MockHTTPError for error-like status codes."""
        if self.status_code >= 400:
            raise MockHTTPError(f"HTTP Error {self.status_code}")


ResponseFactory = Callable[[str, str, dict[str, object]], MockResponse]


class MockTransport:
    """A simple FIFO mock transport with request history."""

    def __init__(
        self: MockTransport,
        response_factory: ResponseFactory | None = None,
    ) -> None:
        """Initialize transport with optional response factory callback."""
        self.responses: list[MockResponse] = []
        self.request_history: list[dict[str, object]] = []
        self._response_factory = response_factory

    def add_response(self: MockTransport, response: MockResponse) -> None:
        """Queue a response to be returned by the next request call."""
        self.responses.append(response)

    def request(
        self: MockTransport,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        data: str | None = None,
        **kwargs: object,
    ) -> MockResponse:
        """Record request details and return next mocked response."""
        params = kwargs.get("params")
        self.request_history.append(
            {
                "method": method,
                "url": url,
                "headers": headers or {},
                "params": params,
                "data": data,
                "kwargs": kwargs,
            },
        )

        if self._response_factory is not None:
            return self._response_factory(
                method,
                url,
                {"headers": headers, "params": params, "data": data, **kwargs},
            )

        if not self.responses:
            raise MockTransportError("No mock responses available")

        return self.responses.pop(0)

    def get_last_request(self: MockTransport) -> dict[str, object]:
        """Return most recently recorded request entry."""
        if not self.request_history:
            raise MockTransportError("No requests recorded")
        return self.request_history[-1]

    def reset(self: MockTransport) -> None:
        """Clear queued responses and request history."""
        self.responses.clear()
        self.request_history.clear()
