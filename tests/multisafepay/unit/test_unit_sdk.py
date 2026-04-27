# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for SDK-level environment/base URL guardrails."""

import pytest

from multisafepay import Sdk
from multisafepay.client.client import Client
from multisafepay.client.credential_resolver import ScopedCredentialResolver

DEFAULT_API_KEY = "resolver_api_key"


class _FakeResponse:
    """Small HTTP response stub for SDK transport tests."""

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
    """Transport stub that captures outbound request headers."""

    def __init__(self: "_CaptureTransport") -> None:
        self.headers = {}

    def request(self: "_CaptureTransport", **kwargs: dict) -> _FakeResponse:
        self.headers = kwargs.get("headers", {})
        return _FakeResponse()


def test_sdk_uses_test_url_by_default(monkeypatch: pytest.MonkeyPatch):
    """Test that SDK client defaults to test URL when not in production."""
    monkeypatch.delenv("MSP_SDK_BUILD_PROFILE", raising=False)
    monkeypatch.delenv("MSP_SDK_CUSTOM_BASE_URL", raising=False)
    monkeypatch.delenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", raising=False)

    sdk = Sdk(api_key="mock_api_key", is_production=False)

    assert sdk.get_client().url == Client.TEST_URL


def test_sdk_uses_live_url_in_production(monkeypatch: pytest.MonkeyPatch):
    """Test that SDK client uses live URL in production mode."""
    monkeypatch.delenv("MSP_SDK_BUILD_PROFILE", raising=False)
    monkeypatch.delenv("MSP_SDK_CUSTOM_BASE_URL", raising=False)
    monkeypatch.delenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", raising=False)

    sdk = Sdk(api_key="mock_api_key", is_production=True)

    assert sdk.get_client().url == Client.LIVE_URL


def test_sdk_allows_custom_base_url_in_dev_when_enabled(
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that SDK allows custom base URL in dev profile when enabled."""
    monkeypatch.setenv("MSP_SDK_BUILD_PROFILE", "dev")
    monkeypatch.setenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", "1")

    sdk = Sdk(
        api_key="mock_api_key",
        is_production=False,
        base_url="https://dev-api.multisafepay.test/v1",
    )

    assert sdk.get_client().url == "https://dev-api.multisafepay.test/v1/"


def test_sdk_blocks_custom_base_url_in_release(
    monkeypatch: pytest.MonkeyPatch,
):
    """Test that SDK blocks custom base URL in release profile."""
    monkeypatch.setenv("MSP_SDK_BUILD_PROFILE", "release")
    monkeypatch.setenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", "1")

    with pytest.raises(ValueError, match="Custom base URL"):
        Sdk(
            api_key="mock_api_key",
            is_production=False,
            base_url="https://dev-api.multisafepay.test/v1",
        )


def test_sdk_allows_resolver_only_initialization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Allow constructing SDK without api_key when resolver is provided."""
    monkeypatch.delenv("MSP_SDK_BUILD_PROFILE", raising=False)
    monkeypatch.delenv("MSP_SDK_CUSTOM_BASE_URL", raising=False)
    monkeypatch.delenv("MSP_SDK_ALLOW_CUSTOM_BASE_URL", raising=False)

    resolver = ScopedCredentialResolver(default_api_key="resolver_api_key")

    sdk = Sdk(
        is_production=False,
        credential_resolver=resolver,
    )

    assert sdk.get_client().url == Client.TEST_URL


def test_sdk_requires_api_key_or_resolver() -> None:
    """Reject SDK initialization when both api_key and resolver are missing."""
    with pytest.raises(ValueError, match="api_key is required"):
        Sdk(is_production=False)


def test_sdk_uses_credential_resolver_with_custom_transport() -> None:
    """Wire resolver + transport together and use resolved auth header."""
    transport = _CaptureTransport()
    resolver = ScopedCredentialResolver(default_api_key=DEFAULT_API_KEY)

    sdk = Sdk(
        is_production=False,
        transport=transport,
        credential_resolver=resolver,
    )

    sdk.get_client().create_get_request("json/orders")

    assert sdk.get_client().transport is transport
    assert transport.headers["Authorization"] == f"Bearer {DEFAULT_API_KEY}"
