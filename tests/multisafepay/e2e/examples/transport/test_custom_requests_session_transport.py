# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""
Test module for e2e testing.

This test validates that a custom `requests.Session` can be injected via
`RequestsTransport` and used end-to-end against the MultiSafepay test API.
"""

from collections.abc import Callable

import pytest

from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.gateways.gateway_manager import GatewayManager
from multisafepay.api.paths.gateways.response.gateway import Gateway
from multisafepay.sdk import Sdk
from multisafepay.transport import RequestsTransport


@pytest.fixture(scope="module")
def gateway_manager(e2e_sdk_factory: Callable[..., Sdk]) -> GatewayManager:
    """Fixture that provides a GatewayManager instance using a custom requests.Session."""
    requests = pytest.importorskip("requests")

    session = requests.Session()
    session.headers.update({"User-Agent": "multisafepay-sdk-tests"})

    transport = RequestsTransport(session=session)
    multisafepay_sdk = e2e_sdk_factory(transport=transport)

    try:
        yield multisafepay_sdk.get_gateway_manager()
    finally:
        session.close()


def test_get_gateways_with_custom_requests_session(
    gateway_manager: GatewayManager,
):
    """Retrieves gateways and validates parsed models."""
    response = gateway_manager.get_gateways()
    assert isinstance(response, CustomApiResponse)

    listing = response.get_data()
    assert isinstance(listing, list)
    assert len(listing) > 0
    assert all(isinstance(gateway, Gateway) for gateway in listing)
