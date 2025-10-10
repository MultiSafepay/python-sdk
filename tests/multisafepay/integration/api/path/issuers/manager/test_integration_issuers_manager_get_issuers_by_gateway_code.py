# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Manager class for Test Integration Issuers Manager Get Issuers By Gateway Code.Py API operations."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.issuers.issuer_manager import IssuerManager
from multisafepay.api.paths.issuers.response.issuer import Issuer
from multisafepay.exception.invalid_argument import InvalidArgumentException


def test_issuer_manager_get_issuers_by_gateway_code_returns_correct_response():
    """
    Test that get_issuers_by_gateway_code returns the correct response.

    This test verifies that the method returns a CustomApiResponse object
    containing the expected issuer data when a valid gateway code is provided.

    """
    client = MagicMock()
    client.create_get_request.return_value = ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": [
                {
                    "gateway_code": "mybank",
                    "code": "123",
                    "description": "Test Issuer",
                },
            ],
        },
    )
    manager = IssuerManager(client)
    response = manager.get_issuers_by_gateway_code("mybank")
    assert isinstance(response, CustomApiResponse)
    assert response.get_data() == [
        Issuer(gateway_code="mybank", code="123", description="Test Issuer"),
    ]


def test_issuer_manager_get_issuers_by_gateway_code_raises_exception_for_invalid_code():
    """
    Test that get_issuers_by_gateway_code raises an exception for an invalid code.

    This test verifies that the method raises an InvalidArgumentException
    when an invalid gateway code is provided.

    """
    client = MagicMock()
    manager = IssuerManager(client)
    try:
        manager.get_issuers_by_gateway_code("invalid_code")
    except InvalidArgumentException as e:
        assert str(e) == "Gateway code is not allowed"


def test_issuer_manager_get_issuers_by_gateway_code_handles_empty_response():
    """
    Test that get_issuers_by_gateway_code handles an empty response.

    This test verifies that the method returns a CustomApiResponse object
    with an empty data list when the API response contains no issuer data.

    """
    client = MagicMock()
    client.create_get_request.return_value = ApiResponse(
        headers={},
        status_code=200,
        body={"success": True, "data": []},
    )
    manager = IssuerManager(client)
    response = manager.get_issuers_by_gateway_code("mybank")
    assert isinstance(response, CustomApiResponse)
    assert response.get_data() == []
