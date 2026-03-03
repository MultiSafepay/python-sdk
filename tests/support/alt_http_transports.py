"""
Test-only HTTP transports used by integration and end-to-end tests.

Purpose
-------
The SDK exposes a small transport contract (``HTTPTransport`` / ``HTTPResponse``)
to decouple business logic from a specific HTTP client. Production code defaults
to ``RequestsTransport``, while tests can inject alternative backends such as
``urllib3`` and ``httpx``.

Scope
-----
This module intentionally lives under ``tests/support`` and is not distributed
as part of the published ``multisafepay`` package.

Current SDK behavior note
-------------------------
``Client`` builds the request URL and passes it to transports. In normal SDK
flows this module therefore treats the URL as the source of truth for query
parameters.

For consistency in tests:
- ``Urllib3Transport`` ignores ``params`` and uses the URL as provided.
- ``HttpxTransport`` forwards ``params`` when explicitly supplied.
"""

from __future__ import annotations

import json
import httpx
import urllib3
from dataclasses import dataclass

from typing_extensions import Self


class TransportHTTPError(RuntimeError):
    """Raised when a response indicates an HTTP error status."""


@dataclass
class Urllib3ResponseAdapter:
    """
    Adapter that makes a urllib3 response compatible with HTTPResponse.

    urllib3 returns an HTTPResponse-like object with different attributes:
    - status (int) instead of status_code
    - data (bytes) instead of json()

    This adapter exposes:
    - status_code
    - headers as dict[str, str]
    - json() parsing data as JSON
    - raise_for_status() similar to requests/httpx
    """

    response: object

    @property
    def status_code(self: Urllib3ResponseAdapter) -> int:
        """Return integer status code from wrapped urllib3 response."""
        return int(self.response.status)

    @property
    def headers(self: Urllib3ResponseAdapter) -> dict[str, str]:
        """Return normalized response headers as string dictionary."""
        raw = getattr(self.response, "headers", {})
        # urllib3 headers behave like a mapping; normalize to dict[str, str].
        return {str(k): str(v) for k, v in dict(raw).items()}

    def json(self: Urllib3ResponseAdapter) -> object:
        """Parse wrapped response data as JSON payload."""
        data = getattr(self.response, "data", b"")
        if data is None:
            return None
        text = data if isinstance(data, str) else data.decode("utf-8")
        return json.loads(text) if text else {}

    def raise_for_status(self: Urllib3ResponseAdapter) -> None:
        """Raise TransportHTTPError for error status codes."""
        if self.status_code >= 400:
            raise TransportHTTPError(f"HTTP Error {self.status_code}")


class Urllib3Transport:
    """
    Simple HTTPTransport backed by urllib3.PoolManager.

    This is a test-focused example implementation. It does not try to cover
    every possible option; it only provides the minimum needed to demonstrate
    transport injection with another popular HTTP backend.
    """

    def __init__(
        self: Urllib3Transport,
        pool_manager: object | None = None,
    ) -> None:
        """Initialize transport with optional custom urllib3 pool manager."""
        self._pool = pool_manager or urllib3.PoolManager()

    def request(
        self: Urllib3Transport,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        data: object | None = None,
        **kwargs: object,
    ) -> Urllib3ResponseAdapter:
        """Perform request using urllib3 and return adapted response object."""
        # Intentionally ignore params to avoid duplicates,
        # because the SDK Client already builds the query string in url.
        # body must be bytes/str. If data is dict/list, serialize it to JSON.
        body: bytes | None
        if data is None:
            body = None
        elif isinstance(data, (bytes, bytearray)):
            body = bytes(data)
        elif isinstance(data, str):
            body = data.encode("utf-8")
        else:
            body = json.dumps(data).encode("utf-8")

        resp = self._pool.request(
            method=method,
            url=url,
            body=body,
            headers=headers,
            **kwargs,
        )
        return Urllib3ResponseAdapter(resp)


class HttpxTransport:
    """
    Simple HTTPTransport backed by httpx.Client.

    Used in tests with pytest.importorskip('httpx') so environments that do
    not have httpx installed are not forced to install it.
    """

    def __init__(
        self: HttpxTransport,
        client: object | None = None,
    ) -> None:
        """Initialize transport with optional custom httpx client."""
        self.client = client or httpx.Client()

    def request(
        self: HttpxTransport,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        data: object | None = None,
        **kwargs: object,
    ) -> object:
        """Perform request using httpx, mapping payload as JSON or content."""
        # httpx distinguishes between raw body (content=) and JSON (json=).
        # If data is dict/list send as JSON; otherwise send as content.
        params = kwargs.pop("params", None)
        request_kwargs: dict[str, object] = {
            "method": method,
            "url": url,
            "headers": headers,
        }

        if params is not None:
            request_kwargs["params"] = params

        if data is not None:
            if isinstance(data, (dict, list)):
                request_kwargs["json"] = data
            else:
                request_kwargs["content"] = data

        request_kwargs.update(kwargs)
        return self.client.request(**request_kwargs)

    def close(self: HttpxTransport) -> None:
        """Close the underlying httpx client."""
        self.client.close()

    def __enter__(self: Self) -> Self:
        """Return self for context manager support."""
        return self

    def __exit__(self: HttpxTransport, *args: object) -> None:
        """Close transport when exiting context manager."""
        self.close()
