"""
Test module for e2e testing.

This test validates that a custom `requests.Session` can be injected via
`RequestsTransport` and used end-to-end against the MultiSafepay test API.
"""

import os

import pytest
from dotenv import load_dotenv

from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.gateways.gateway_manager import GatewayManager
from multisafepay.api.paths.gateways.response.gateway import Gateway
from multisafepay.sdk import Sdk
from multisafepay.transport import RequestsTransport


@pytest.fixture(scope="module")
def gateway_manager() -> GatewayManager:
    """Fixture that provides a GatewayManager instance using a custom requests.Session."""
    requests = pytest.importorskip("requests")

    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        pytest.skip("API_KEY env var not set")

    session = requests.Session()
    session.headers.update({"User-Agent": "multisafepay-sdk-tests"})

    transport = RequestsTransport(session=session)
    multisafepay_sdk = Sdk(api_key, False, transport)

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
