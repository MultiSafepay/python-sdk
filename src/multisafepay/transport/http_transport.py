# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""HTTP Transport layer abstraction for decoupling network communication."""

from typing import Optional, Protocol


class HTTPTransport(Protocol):
    """
    Protocol defining the interface for HTTP transport implementations.

    This abstraction allows the SDK to be decoupled from specific HTTP client
    libraries, enabling flexibility to switch between different implementations
    (e.g., requests, httpx, urllib) or to provide mock implementations for testing.

    The transport layer follows the Dependency Inversion Principle, allowing
    business logic to depend on abstractions rather than concrete implementations.
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
        method : str
            The HTTP method (GET, POST, PATCH, DELETE, etc.).
        url : str
            The full URL for the request.
        headers : Optional[Dict[str, str]], optional
            HTTP headers to include in the request, by default None.
        data : Optional[str], optional
            Request body data, by default None.
        **kwargs : Any
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
