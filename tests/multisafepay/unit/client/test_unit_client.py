# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

import pytest

from multisafepay.client.client import Client
from multisafepay.transport import RequestsTransport

requests = pytest.importorskip("requests")


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
