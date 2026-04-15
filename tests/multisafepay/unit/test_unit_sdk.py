# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for SDK-level environment/base URL guardrails."""

import pytest

from multisafepay import Sdk
from multisafepay.client.client import Client


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
