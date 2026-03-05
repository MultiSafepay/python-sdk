# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Test module for HTTPTransport implementations."""

from typing import NoReturn

import pytest
from unittest.mock import Mock

from multisafepay.sdk import Sdk
from multisafepay.transport import RequestsTransport
from tests.support.mock_transport import MockResponse, MockTransport


@pytest.fixture()
def requires_requests():
    """Skip tests when the optional `requests` dependency isn't installed."""
    return pytest.importorskip("requests")


class TestRequestsTransportWithRequests:
    """RequestsTransport behavior when `requests` is available."""

    def test_initializes_session_default_or_custom(
        self: "TestRequestsTransportWithRequests",
        requires_requests: object,
    ) -> None:
        """Initialize default and custom sessions."""
        assert requires_requests is not None
        custom_session = Mock()

        transport_default = RequestsTransport()
        assert transport_default.session is not None

        transport_custom = RequestsTransport(session=custom_session)
        assert transport_custom.session is custom_session

    def test_request_delegates_to_session(
        self: "TestRequestsTransportWithRequests",
        requires_requests: object,
    ) -> None:
        """Delegate prepared request sending to the session."""
        mock_session = Mock()
        prepared = object()
        mock_response = Mock()
        mock_session.prepare_request.return_value = prepared
        mock_session.send.return_value = mock_response

        transport = RequestsTransport(session=mock_session)
        response = transport.request(
            method="GET",
            url="https://api.example.com/resource",
            headers={"Authorization": "Bearer test"},
        )

        assert response is mock_response
        mock_session.prepare_request.assert_called_once()
        request_obj = mock_session.prepare_request.call_args.args[0]
        assert isinstance(request_obj, requires_requests.Request)
        mock_session.send.assert_called_once_with(prepared)

    def test_context_manager_closes_session(
        self: "TestRequestsTransportWithRequests",
        requires_requests: object,
    ) -> None:
        """Close session when exiting context manager."""
        assert requires_requests is not None
        mock_session = Mock()
        transport = RequestsTransport(session=mock_session)

        with transport as entered:
            assert entered is transport

        mock_session.close.assert_called_once()


class TestRequestsTransportWithoutRequests:
    """Failure modes when `requests` isn't installed and no transport is injected."""

    def test_raises_clear_error_when_requests_missing(
        self: "TestRequestsTransportWithoutRequests",
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Raise an actionable error when requests is unavailable."""
        from multisafepay.transport import requests_transport

        monkeypatch.setattr(requests_transport, "_HAS_REQUESTS", False)
        monkeypatch.setattr(
            requests_transport,
            "_REQUESTS_IMPORT_ERROR",
            ModuleNotFoundError("No module named 'requests'"),
        )

        with pytest.raises(
            ModuleNotFoundError,
            match="Optional dependency 'requests'",
        ):
            RequestsTransport()

    def test_sdk_does_not_touch_requests_when_transport_injected(
        self: "TestRequestsTransportWithoutRequests",
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Skip RequestsTransport construction when transport is injected."""
        import multisafepay.client.client as client_module

        def _boom() -> NoReturn:
            raise AssertionError("RequestsTransport() should not be called")

        monkeypatch.setattr(client_module, "RequestsTransport", _boom)

        sdk = Sdk(
            api_key="test_api_key",
            is_production=False,
            transport=MockTransport(),
        )
        assert sdk.client.transport is not None

    def test_sdk_raises_when_requests_missing_and_no_transport(
        self: "TestRequestsTransportWithoutRequests",
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Fail fast when no injected transport and requests is missing."""
        from multisafepay.transport import requests_transport

        monkeypatch.setattr(requests_transport, "_HAS_REQUESTS", False)
        monkeypatch.setattr(
            requests_transport,
            "_REQUESTS_IMPORT_ERROR",
            ModuleNotFoundError("No module named 'requests'"),
        )

        with pytest.raises(
            ModuleNotFoundError,
            match="multisafepay\\[requests\\]",
        ):
            Sdk(api_key="test_api_key", is_production=False)


class TestMockTransport:
    """Test suite for MockTransport."""

    @pytest.fixture()
    def transport(self: "TestMockTransport") -> MockTransport:
        """Provide a fresh mock transport."""
        return MockTransport()

    def test_request_fifo_and_history(
        self: "TestMockTransport",
        transport: MockTransport,
    ) -> None:
        """Return responses in FIFO order and keep request history."""
        transport.add_response(
            MockResponse(status_code=200, json_data={"id": 1}),
        )
        transport.add_response(
            MockResponse(status_code=201, json_data={"id": 2}),
        )

        first = transport.request(
            "GET",
            "https://api.example.com/1",
            headers={"Authorization": "Bearer token"},
        )
        second = transport.request("POST", "https://api.example.com/2")
        assert first.json()["id"] == 1
        assert second.json()["id"] == 2

        assert len(transport.request_history) == 2
        assert transport.request_history[0]["method"] == "GET"
        assert (
            transport.get_last_request()["url"] == "https://api.example.com/2"
        )

    def test_request_raises_when_no_responses(
        self: "TestMockTransport",
        transport: MockTransport,
    ) -> None:
        """Raise when no mock responses were queued."""
        with pytest.raises(RuntimeError, match="No mock responses available"):
            transport.request("GET", "https://api.example.com")

    def test_response_factory(self: "TestMockTransport") -> None:
        """Use the factory callback to produce responses."""

        def factory(
            method: str,
            _url: str,
            _kwargs: dict[str, object],
        ) -> MockResponse:
            status = 200 if method == "GET" else 201
            return MockResponse(
                status_code=status,
                json_data={"method": method},
            )

        transport = MockTransport(response_factory=factory)

        assert (
            transport.request("GET", "https://api.example.com").json()[
                "method"
            ]
            == "GET"
        )
        assert (
            transport.request("POST", "https://api.example.com").json()[
                "method"
            ]
            == "POST"
        )


class TestMockResponse:
    """Test suite for MockResponse."""

    def test_values_default_and_custom(self: "TestMockResponse") -> None:
        """Expose defaults and preserve custom values."""
        default = MockResponse()
        assert default.status_code == 200
        assert default.headers == {}
        assert default.json() == {}

        custom = MockResponse(
            status_code=201,
            json_data={"id": 123, "name": "test"},
            headers={"Content-Type": "application/json"},
        )
        assert custom.status_code == 201
        assert custom.json()["id"] == 123
        assert custom.headers["Content-Type"] == "application/json"

    def test_raise_for_status(self: "TestMockResponse") -> None:
        """Raise only for HTTP error status codes."""
        MockResponse(status_code=200).raise_for_status()
        with pytest.raises(Exception, match="HTTP Error 404"):
            MockResponse(status_code=404).raise_for_status()
