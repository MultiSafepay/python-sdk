# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""
E2E: injected transport using httpx (sync).

This test performs a REAL call against the MultiSafepay test environment.
It runs only when `API_KEY` is set (see `tests/multisafepay/e2e/conftest.py`).

What this validates
-------------------
- The SDK works end-to-end with an alternative HTTP client (httpx) via
    dependency injection (`Sdk(..., transport=...)`).
- The SDK still parses gateway models correctly.

Async note
----------
This uses httpx in sync mode.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest
from dotenv import load_dotenv

from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.gateways.response.gateway import Gateway
from multisafepay.sdk import Sdk

from tests.support.alt_http_transports import HttpxTransport

if TYPE_CHECKING:
    from multisafepay.api.paths.gateways.gateway_manager import GatewayManager


@pytest.fixture(scope="module")
def gateway_manager() -> GatewayManager:
    """
    Create a GatewayManager using an injected httpx-backed transport.

    Skips if `httpx` is not installed or if `API_KEY` is not set.
    """
    pytest.importorskip("httpx")

    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        pytest.skip("API_KEY env var not set")

    # Ensure resources are cleaned up after the module.
    transport = HttpxTransport()
    try:
        sdk = Sdk(api_key=api_key, is_production=False, transport=transport)
        yield sdk.get_gateway_manager()
    finally:
        transport.close()


def test_get_gateways_with_injected_httpx_transport(
    gateway_manager: GatewayManager,
):
    """Fetch gateways through the injected transport and validate parsed models."""
    response = gateway_manager.get_gateways()
    assert isinstance(response, CustomApiResponse)

    listing = response.get_data()
    assert isinstance(listing, list)
    assert len(listing) > 0
    assert all(isinstance(gateway, Gateway) for gateway in listing)
