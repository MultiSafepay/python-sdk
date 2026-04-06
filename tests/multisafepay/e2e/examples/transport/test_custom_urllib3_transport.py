# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""
E2E: injected transport using urllib3.

This test performs a REAL call against the MultiSafepay test environment.
It runs only when `E2E_API_KEY` is set (see `tests/multisafepay/e2e/conftest.py`).

What this validates
-------------------
- The SDK works end-to-end with an alternative HTTP client (urllib3) via
    dependency injection (`Sdk(..., transport=...)`).
- The SDK still parses gateway models correctly.

Why an adapter is needed
------------------------
`urllib3` does not expose the same response interface as requests/httpx (e.g.
`.json()` / `.raise_for_status()` / `status_code`), so we use a small adapter
transport from `tests/support`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.gateways.response.gateway import Gateway
from tests.support.alt_http_transports import Urllib3Transport

if TYPE_CHECKING:
    from collections.abc import Callable

    from multisafepay.api.paths.gateways.gateway_manager import GatewayManager
    from multisafepay.sdk import Sdk


@pytest.fixture(scope="module")
def gateway_manager(e2e_sdk_factory: Callable[..., Sdk]) -> GatewayManager:
    """
    Create a GatewayManager using an injected urllib3-backed transport.

    Skips if `urllib3` is not installed or if `E2E_API_KEY` is not set.
    """
    pytest.importorskip("urllib3")

    transport = Urllib3Transport()
    sdk = e2e_sdk_factory(transport=transport)
    return sdk.get_gateway_manager()


def test_get_gateways_with_injected_urllib3_transport(
    gateway_manager: GatewayManager,
):
    """Fetch gateways through the injected transport and validate parsed models."""
    response = gateway_manager.get_gateways()
    assert isinstance(response, CustomApiResponse)
    listing = response.get_data()
    assert isinstance(listing, list)
    assert len(listing) > 0
    assert all(isinstance(gateway, Gateway) for gateway in listing)
