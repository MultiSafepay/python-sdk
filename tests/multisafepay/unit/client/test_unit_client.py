# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import pytest
from unittest.mock import Mock
from requests import Session
from requests.exceptions import RequestException
from multisafepay.client.client import Client


def api_response_mock(json_data, status_code=200):
    """
    Create a mock API response with the given JSON data and status code.

    """
    mock_response = Mock()
    mock_response.json.return_value = json_data
    mock_response.status_code = status_code
    mock_response.raise_for_status = Mock()
    return mock_response


def api_response_mock_with_exception_server_error(json_data, status_code=500):
    """
    Create a mock API response that raises a RequestException for server errors.

    """
    mock_response = Mock()
    mock_response.json.return_value = json_data
    mock_response.status_code = status_code
    mock_response.raise_for_status.side_effect = RequestException(
        "Server error",
    )
    return mock_response


def api_response_mock_with_exception_wrong_request(json_data, status_code=400):
    """
    Create a mock API response that raises a RequestException for bad requests.

    """
    mock_response = Mock()
    mock_response.json.return_value = json_data
    mock_response.status_code = status_code
    mock_response.raise_for_status.side_effect = RequestException(
        "Request failed",
    )
    return mock_response


def api_key_mock():
    """
    Create a mock API key.

    """
    mock_api_key = Mock()
    mock_api_key.get.return_value = "mock_api_key"
    return mock_api_key


@pytest.fixture()
def client():
    """
    Fixture to create a Client instance with a mock API key.

    """
    return Client(api_key="mock_api_key", is_production=False)


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
