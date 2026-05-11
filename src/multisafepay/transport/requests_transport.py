# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Concrete implementation of HTTPTransport using the requests library."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from multisafepay.transport.http_transport import HTTPStreamResponse
from typing_extensions import Self

_REQUESTS_IMPORT_ERROR: ImportError | None = None
_REQUEST_KWARG_NAMES = frozenset(
    {
        "auth",
        "cookies",
        "files",
        "hooks",
        "json",
        "params",
    },
)

if TYPE_CHECKING:  # pragma: no cover
    from requests import PreparedRequest, Request, Session
    from requests.models import Response

try:
    from requests import Request, Session
    from requests.models import Response

    _HAS_REQUESTS = True
except ImportError as exc:  # pragma: no cover
    # `requests` is an optional dependency. The SDK can still be used if a
    # custom HTTPTransport implementation is provided.
    _HAS_REQUESTS = False
    _REQUESTS_IMPORT_ERROR = exc


def _raise_requests_missing() -> None:
    raise ModuleNotFoundError(
        "Optional dependency 'requests' is required for RequestsTransport. "
        "Install it via 'pip install multisafepay[requests]' or 'pip install requests', "
        "or pass a custom HTTPTransport implementation to Sdk(..., transport=...).",
    ) from _REQUESTS_IMPORT_ERROR


class _RequestsStreamResponse:
    """Adapter exposing a requests streaming response through the SDK contract."""

    def __init__(self: _RequestsStreamResponse, response: Response) -> None:
        self._response = response

    @property
    def status_code(self: _RequestsStreamResponse) -> int:
        """Return the wrapped response status code."""
        return int(self._response.status_code)

    @property
    def headers(self: _RequestsStreamResponse) -> dict[str, str]:
        """Return normalized response headers."""
        return {
            str(key): str(value)
            for key, value in dict(self._response.headers).items()
        }

    def json(self: _RequestsStreamResponse) -> object:
        """Parse the wrapped response body as JSON."""
        return self._response.json()

    def raise_for_status(self: _RequestsStreamResponse) -> None:
        """Raise requests' HTTP error for non-success status codes."""
        self._response.raise_for_status()

    def readline(self: _RequestsStreamResponse) -> bytes:
        """Read one line from the underlying streaming body."""
        raw_stream = self._response.raw
        if raw_stream is None:
            return b""

        return cast(bytes, raw_stream.readline())

    def close(self: _RequestsStreamResponse) -> None:
        """Close the wrapped streaming response."""
        self._response.close()


class RequestsTransport:
    """
    Concrete implementation of HTTPTransport using the requests library.

    This is the default transport implementation that wraps the requests library,
    providing a standardized interface for making HTTP requests.

    Attributes
    ----------
    session (Session): The underlying requests Session object used for
        connection pooling and request execution.

    """

    def __init__(
        self: RequestsTransport,
        session: Session | None = None,
    ) -> None:
        """
        Initialize the RequestsTransport.

        Parameters
        ----------
        session (Session | None): An existing requests Session to use. If not
            provided, a new Session will be created, by default None.

        """
        if not _HAS_REQUESTS:  # pragma: no cover
            _raise_requests_missing()
        self.session = session if session is not None else Session()

    def request(
        self: RequestsTransport,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        data: str | None = None,
        **kwargs: object,
    ) -> Response:
        """
        Execute an HTTP request using the requests library.

        Parameters
        ----------
        method (str): The HTTP method (GET, POST, PATCH, DELETE, etc.).
        url (str): The full URL for the request.
        headers (dict[str, str] | None): HTTP headers to include in the request, by default None.
        data (str | None): Request body data, by default None.
        **kwargs (object): Additional keyword arguments passed to requests.

        Returns
        -------
        Response: The requests Response object.

        Raises
        ------
        RequestException: If the request fails or encounters an error.

        """
        if not _HAS_REQUESTS:  # pragma: no cover
            _raise_requests_missing()
        session, prepared_request, send_kwargs = self._prepare_request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            **kwargs,
        )
        return session.send(prepared_request, **send_kwargs)

    def open_stream(
        self: RequestsTransport,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        data: str | None = None,
        **kwargs: object,
    ) -> HTTPStreamResponse:
        """Open a streaming HTTP response using the shared requests session."""
        if not _HAS_REQUESTS:  # pragma: no cover
            _raise_requests_missing()

        session, prepared_request, send_kwargs = self._prepare_request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            **kwargs,
        )
        send_kwargs["stream"] = True
        response = session.send(prepared_request, **send_kwargs)
        return _RequestsStreamResponse(response)

    def _prepare_request(
        self: RequestsTransport,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        data: str | None = None,
        **kwargs: object,
    ) -> tuple[Session, PreparedRequest, dict[str, object]]:
        """Prepare a request once so regular and streaming calls share the same path."""
        if not _HAS_REQUESTS:  # pragma: no cover
            _raise_requests_missing()

        session = cast("Session", self.session)
        request_kwargs: dict[str, object] = {}
        send_kwargs: dict[str, object] = {}

        if headers is not None:
            request_kwargs["headers"] = headers

        if data is not None:
            request_kwargs["data"] = data

        for key, value in kwargs.items():
            if key in _REQUEST_KWARG_NAMES:
                request_kwargs[key] = value
            else:
                send_kwargs[key] = value

        request = Request(
            method=method,
            url=url,
            **request_kwargs,
        )
        prepared_request = session.prepare_request(request)
        return session, prepared_request, send_kwargs

    def close(self: RequestsTransport) -> None:
        """
        Close the underlying session.

        This method should be called when the transport is no longer needed
        to properly clean up resources.
        """
        if not _HAS_REQUESTS:  # pragma: no cover
            _raise_requests_missing()
        session = cast("Session", self.session)
        session.close()

    def __enter__(self: Self) -> Self:
        """Support context manager protocol."""
        return self

    def __exit__(self: RequestsTransport, *args: object) -> None:
        """Close session when exiting context."""
        self.close()
