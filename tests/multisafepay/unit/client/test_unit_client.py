# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from unittest.mock import Mock
from requests import Session
from multisafepay.client.client import Client


def test_initializes_with_default_http_client():
    """
    Test that the Client initializes with the default HTTP client.

    """
    client = Client(api_key="mock_api_key", is_production=False)
    assert isinstance(client.http_client, Session)


def test_initializes_with_custom_http_client():
    """
    Test that the Client initializes with a custom HTTP client.

    """
    custom_http_client = Mock()
    client = Client(
        api_key="mock_api_key",
        is_production=False,
        http_client=custom_http_client,
    )
    assert client.http_client == custom_http_client
