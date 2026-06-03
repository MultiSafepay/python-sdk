# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Tests for the HTTPStreamingTransport / HTTPTransport protocol split."""

from typing import TYPE_CHECKING, Optional

import pytest

from multisafepay.transport import (
    HTTPStreamingTransport,
    HTTPTransport,
    RequestsTransport,
)

if TYPE_CHECKING:
    from multisafepay.transport.http_transport import (
        HTTPResponse,
        HTTPStreamResponse,
    )


class _RequestOnlyTransport:
    """Custom transport that only implements the request-only protocol."""

    def request(
        self: "_RequestOnlyTransport",
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        data: Optional[str] = None,
        **kwargs: object,
    ) -> "HTTPResponse":
        raise NotImplementedError


class _StreamingTransport(_RequestOnlyTransport):
    """Custom transport that also implements the streaming protocol."""

    def open_stream(
        self: "_StreamingTransport",
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        data: Optional[str] = None,
        **kwargs: object,
    ) -> "HTTPStreamResponse":
        raise NotImplementedError


class TestHTTPStreamingTransportProtocol:
    """HTTPStreamingTransport runtime classification."""

    def test_requests_transport_satisfies_streaming_protocol(
        self: "TestHTTPStreamingTransportProtocol",
    ) -> None:
        """Default RequestsTransport implements both protocols."""
        pytest.importorskip("requests")
        transport = RequestsTransport()
        assert isinstance(transport, HTTPStreamingTransport)

    def test_request_only_transport_is_not_streaming(
        self: "TestHTTPStreamingTransportProtocol",
    ) -> None:
        """Transports without open_stream are rejected by the streaming protocol."""
        assert not isinstance(
            _RequestOnlyTransport(),
            HTTPStreamingTransport,
        )

    def test_streaming_custom_transport_is_recognized(
        self: "TestHTTPStreamingTransportProtocol",
    ) -> None:
        """Custom transports implementing open_stream satisfy the streaming protocol."""
        assert isinstance(_StreamingTransport(), HTTPStreamingTransport)

    def test_streaming_protocol_extends_base_transport(
        self: "TestHTTPStreamingTransportProtocol",
    ) -> None:
        """HTTPStreamingTransport must inherit from HTTPTransport."""
        assert HTTPTransport in HTTPStreamingTransport.__mro__

    def test_base_transport_no_longer_requires_open_stream(
        self: "TestHTTPStreamingTransportProtocol",
    ) -> None:
        """HTTPTransport must not expose open_stream as a protocol member."""
        assert "open_stream" not in HTTPTransport.__dict__
