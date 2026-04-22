# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

import pytest

from multisafepay.client.client import Client
from multisafepay.client.credential_resolver import (
    ScopedCredentialResolver,
)
from multisafepay.transport import RequestsTransport

requests = pytest.importorskip("requests")

DEFAULT_API_KEY = "default_api_key"
TERMINAL_GROUP_ID = "Default"
TERMINAL_GROUP_API_KEY = "terminal_group_api_key"
ORDERS_ENDPOINT = "json/orders"
API_KEY_REQUIRED_ERROR = "api_key is required"


class _FakeResponse:
    """Small HTTP response stub for unit tests."""

    status_code = 200
    headers = {}

    @staticmethod
    def json() -> dict:
        return {
            "success": True,
            "data": {},
        }

    @staticmethod
    def raise_for_status() -> None:
        return


class _CaptureTransport:
    """Transport stub that captures the request headers."""

    def __init__(self: "_CaptureTransport") -> None:
        self.headers = {}

    def request(self: "_CaptureTransport", **kwargs: dict) -> _FakeResponse:
        self.headers = kwargs.get("headers", {})
        return _FakeResponse()


def _build_resolver_client(
    resolver: ScopedCredentialResolver,
    transport: _CaptureTransport,
) -> Client:
    """Build a client configured for resolver-based auth tests."""
    return Client(
        api_key=None,
        is_production=False,
        transport=transport,
        credential_resolver=resolver,
    )


def test_initializes_with_default_requests_transport():
    """Test that the Client initializes with the default requests transport."""
    client = Client(api_key="mock_api_key", is_production=False)
    assert isinstance(client.transport, RequestsTransport)
    assert isinstance(client.transport.session, requests.Session)


def test_initializes_with_custom_requests_session_via_transport():
    """Test that the Client can be initialized with a custom requests.Session via transport."""
    session = requests.Session()
    transport = RequestsTransport(session=session)
    client = Client(
        api_key="mock_api_key",
        is_production=False,
        transport=transport,
    )
    assert client.transport is transport
    assert client.transport.session is session
    session.close()


def test_defaults_to_test_url(monkeypatch: pytest.MonkeyPatch):
    """Test that client defaults to test URL when not in production."""
    monkeypatch.delenv("MSP_SDK_BUILD_PROFILE", raising=False)
    monkeypatch.delenv("MSP_SDK_CUSTOM_BASE_URL", raising=False)
    monkeypatch.delenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", raising=False)

    client = Client(api_key="mock_api_key", is_production=False)
    assert client.url == Client.TEST_URL


def test_defaults_to_live_url(monkeypatch: pytest.MonkeyPatch):
    """Test that client defaults to live URL when in production mode."""
    monkeypatch.delenv("MSP_SDK_BUILD_PROFILE", raising=False)
    monkeypatch.delenv("MSP_SDK_CUSTOM_BASE_URL", raising=False)
    monkeypatch.delenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", raising=False)

    client = Client(api_key="mock_api_key", is_production=True)
    assert client.url == Client.LIVE_URL


def test_allows_custom_base_url_only_in_dev_profile(
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that custom base URL is allowed only in dev profile with flag enabled."""
    monkeypatch.setenv("MSP_SDK_BUILD_PROFILE", "dev")
    monkeypatch.setenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", "1")

    client = Client(
        api_key="mock_api_key",
        is_production=False,
        base_url="https://dev-api.multisafepay.test/v1",
    )
    assert client.url == "https://dev-api.multisafepay.test/v1/"


def test_blocks_custom_base_url_in_release_profile(
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that custom base URL is blocked in release profile."""
    monkeypatch.setenv("MSP_SDK_BUILD_PROFILE", "release")
    monkeypatch.setenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", "1")

    with pytest.raises(ValueError, match="Custom base URL"):
        Client(
            api_key="mock_api_key",
            is_production=False,
            base_url="https://dev-api.multisafepay.test/v1",
        )


def test_blocks_custom_base_url_when_flag_disabled(
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that custom base URL is blocked when the enable flag is disabled."""
    monkeypatch.setenv("MSP_SDK_BUILD_PROFILE", "dev")
    monkeypatch.setenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", "0")

    with pytest.raises(ValueError, match="Custom base URL"):
        Client(
            api_key="mock_api_key",
            is_production=False,
            base_url="https://dev-api.multisafepay.test/v1",
        )


def test_allows_custom_base_url_from_env_in_dev_profile(
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that custom base URL can be provided via environment in dev profile."""
    monkeypatch.setenv("MSP_SDK_BUILD_PROFILE", "dev")
    monkeypatch.setenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", "1")
    monkeypatch.setenv(
        "MSP_SDK_CUSTOM_BASE_URL",
        "https://dev-api.multisafepay.test/v1",
    )

    client = Client(api_key="mock_api_key", is_production=False)

    assert client.url == "https://dev-api.multisafepay.test/v1/"


def test_explicit_base_url_takes_precedence_over_env(
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that an explicit base URL overrides the environment value."""
    monkeypatch.setenv("MSP_SDK_BUILD_PROFILE", "dev")
    monkeypatch.setenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", "1")
    monkeypatch.setenv(
        "MSP_SDK_CUSTOM_BASE_URL",
        "https://env-api.multisafepay.test/v1",
    )

    client = Client(
        api_key="mock_api_key",
        is_production=False,
        base_url="https://explicit-api.multisafepay.test/v1",
    )

    assert client.url == "https://explicit-api.multisafepay.test/v1/"


def test_rejects_custom_base_url_with_query(
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that custom base URL rejects query strings."""
    monkeypatch.setenv("MSP_SDK_BUILD_PROFILE", "dev")
    monkeypatch.setenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", "1")

    with pytest.raises(ValueError, match="Invalid base URL"):
        Client(
            api_key="mock_api_key",
            is_production=False,
            base_url="https://dev-api.multisafepay.test/v1?foo=bar",
        )


def test_rejects_custom_base_url_with_fragment(
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that custom base URL rejects fragments."""
    monkeypatch.setenv("MSP_SDK_BUILD_PROFILE", "dev")
    monkeypatch.setenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", "1")

    with pytest.raises(ValueError, match="Invalid base URL"):
        Client(
            api_key="mock_api_key",
            is_production=False,
            base_url="https://dev-api.multisafepay.test/v1#section",
        )


def test_rejects_custom_base_url_with_params(
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that custom base URL rejects path parameters."""
    monkeypatch.setenv("MSP_SDK_BUILD_PROFILE", "dev")
    monkeypatch.setenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", "1")

    with pytest.raises(ValueError, match="Invalid base URL"):
        Client(
            api_key="mock_api_key",
            is_production=False,
            base_url="https://dev-api.multisafepay.test/v1;foo",
        )


def test_rejects_custom_base_url_without_scheme(
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that custom base URL rejects missing scheme."""
    monkeypatch.setenv("MSP_SDK_BUILD_PROFILE", "dev")
    monkeypatch.setenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", "1")

    with pytest.raises(ValueError, match="Invalid base URL"):
        Client(
            api_key="mock_api_key",
            is_production=False,
            base_url="dev-api.multisafepay.test/v1",
        )


def test_rejects_custom_base_url_without_netloc(
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that custom base URL rejects missing netloc."""
    monkeypatch.setenv("MSP_SDK_BUILD_PROFILE", "dev")
    monkeypatch.setenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", "1")

    with pytest.raises(ValueError, match="Invalid base URL"):
        Client(
            api_key="mock_api_key",
            is_production=False,
            base_url="https:///v1",
        )


def test_create_get_request_sends_authorization_header() -> None:
    """GET request includes Bearer authorization header."""
    transport = _CaptureTransport()
    client = Client(
        api_key="test_key",
        is_production=False,
        transport=transport,
    )
    client.create_get_request("json/orders")
    assert transport.headers["Authorization"] == "Bearer test_key"


def test_create_post_request_sends_authorization_header() -> None:
    """POST request includes Bearer authorization header."""
    transport = _CaptureTransport()
    client = Client(
        api_key="test_key",
        is_production=False,
        transport=transport,
    )
    client.create_post_request("json/orders", request_body='{"foo":"bar"}')
    assert transport.headers["Authorization"] == "Bearer test_key"


def test_create_patch_request_sends_authorization_header() -> None:
    """PATCH request includes Bearer authorization header."""
    transport = _CaptureTransport()
    client = Client(
        api_key="test_key",
        is_production=False,
        transport=transport,
    )
    client.create_patch_request("json/orders/1", request_body='{"foo":"bar"}')
    assert transport.headers["Authorization"] == "Bearer test_key"


def test_create_delete_request_sends_authorization_header() -> None:
    """DELETE request includes Bearer authorization header."""
    transport = _CaptureTransport()
    client = Client(
        api_key="test_key",
        is_production=False,
        transport=transport,
    )
    client.create_delete_request("json/recurring/1")
    assert transport.headers["Authorization"] == "Bearer test_key"


def test_resolve_api_key_uses_credential_resolver() -> None:
    """Prefer credential resolver when both api_key and resolver exist."""
    transport = _CaptureTransport()
    resolver = ScopedCredentialResolver(default_api_key="resolver_key")
    client = _build_resolver_client(resolver, transport)
    client.create_get_request("json/orders")
    assert transport.headers["Authorization"] == "Bearer resolver_key"


def test_resolve_api_key_raises_without_key_or_resolver() -> None:
    """Raise ValueError when no api_key or resolver is configured."""
    with pytest.raises(ValueError, match=API_KEY_REQUIRED_ERROR):
        Client(
            api_key=None,
            is_production=False,
            transport=_CaptureTransport(),
            credential_resolver=None,
        )
