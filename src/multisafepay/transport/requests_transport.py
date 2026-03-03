# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Concrete implementation of HTTPTransport using the requests library."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from typing_extensions import Self

_REQUESTS_IMPORT_ERROR: ImportError | None = None

if TYPE_CHECKING:  # pragma: no cover
    from requests import Request, Session
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
        "Install it via 'pip install multisafepay[requests]' (or add the Poetry extra 'requests'), "
        "or pass a custom HTTPTransport implementation to Sdk(..., transport=...).",
    ) from _REQUESTS_IMPORT_ERROR


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
        session = cast("Session", self.session)
        request = Request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            **kwargs,
        )
        prepared_request = session.prepare_request(request)
        return session.send(prepared_request)

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
