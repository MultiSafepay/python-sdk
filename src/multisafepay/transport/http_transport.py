# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""HTTP Transport layer abstraction for decoupling network communication."""

from typing import Optional, Protocol, runtime_checkable


class HTTPResponse(Protocol):
    """
    Protocol defining the interface for HTTP response objects.

    This abstraction ensures that different transport implementations
    return responses with a consistent interface.
    """

    @property
    def status_code(self: "HTTPResponse") -> int:
        """
        Get the HTTP status code.

        Returns
        -------
        int
            The HTTP status code (e.g., 200, 404, 500).

        """
        raise NotImplementedError

    @property
    def headers(self: "HTTPResponse") -> dict[str, str]:
        """
        Get the response headers.

        Returns
        -------
        Dict[str, str]
            Dictionary of response headers.

        """
        raise NotImplementedError

    def json(self: "HTTPResponse") -> object:
        """
        Parse the response body as JSON.

        Returns
        -------
        Any
            The parsed JSON data.

        Raises
        ------
        Exception
            If the response body cannot be parsed as JSON.

        """
        raise NotImplementedError

    def raise_for_status(self: "HTTPResponse") -> None:
        """
        Raise an exception for HTTP error status codes (4xx, 5xx).

        Raises
        ------
        Exception
            If the status code indicates an error.

        """
        raise NotImplementedError


class HTTPStreamResponse(HTTPResponse, Protocol):
    """Protocol for HTTP responses that can be consumed as a byte stream."""

    def readline(self: "HTTPStreamResponse") -> bytes:
        """Read one line from the streaming response."""
        raise NotImplementedError

    def close(self: "HTTPStreamResponse") -> None:
        """Close the streaming response and release resources."""
        raise NotImplementedError


class HTTPTransport(Protocol):
    """
    Protocol defining the interface for HTTP transport implementations.

    This abstraction allows the SDK to be decoupled from specific HTTP client
    libraries, enabling flexibility to switch between different implementations
    (e.g., requests, httpx, urllib) or to provide mock implementations for testing.

    The transport layer follows the Dependency Inversion Principle, allowing
    business logic to depend on abstractions rather than concrete implementations.

    Implementations only need to provide regular request/response support. For
    Server-Sent Events (SSE) subscriptions, implement
    :class:`HTTPStreamingTransport` instead, which extends this protocol with
    :meth:`open_stream`.
    """

    def request(
        self: "HTTPTransport",
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        data: Optional[str] = None,
        **kwargs: object,
    ) -> "HTTPResponse":
        """
        Execute an HTTP request.

        Parameters
        ----------
        method (str):
            The HTTP method (GET, POST, PATCH, DELETE, etc.).
        url (str):
            The full URL for the request.
        headers (Optional[dict[str, str]]):
            HTTP headers to include in the request, by default None.
        data (Optional[str]):
            Request body data, by default None.
        **kwargs (object):
            Additional keyword arguments for transport-specific options,
            such as query params, timeout, SSL options, etc.

        Returns
        -------
        HTTPResponse
            The HTTP response object.

        Raises
        ------
        Exception
            If the request fails or encounters an error.

        """
        raise NotImplementedError


@runtime_checkable
class HTTPStreamingTransport(HTTPTransport, Protocol):
    """
    Protocol for HTTP transports that also support streaming responses.

    Extends :class:`HTTPTransport` with :meth:`open_stream`, used by the SDK
    to consume Server-Sent Events (SSE). Transports that only need to handle
    regular API calls do not have to implement this protocol; SSE features
    will raise a clear runtime error when the configured transport does not
    support streaming.
    """

    def open_stream(
        self: "HTTPStreamingTransport",
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        data: Optional[str] = None,
        **kwargs: object,
    ) -> "HTTPStreamResponse":
        """
        Open an HTTP response stream.

        Parameters
        ----------
        method (str):
            The HTTP method (GET, POST, etc.).
        url (str):
            The full URL for the request.
        headers (Optional[dict[str, str]]):
            HTTP headers to include in the request, by default None.
        data (Optional[str]):
            Request body data, by default None.
        **kwargs (object):
            Additional keyword arguments for transport-specific send options,
            such as timeout, SSL options, and proxy configuration.

        Returns
        -------
        HTTPStreamResponse
            The open streaming HTTP response.

        Raises
        ------
        Exception
            If the stream cannot be opened or encounters an error.

        """
        raise NotImplementedError
