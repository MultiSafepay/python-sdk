# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for RecurringManager get_list, get, and delete behavior."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.recurring.recurring_manager import RecurringManager

REFERENCE = "cust-ref-1"
TOKEN_VALUE = "tok-abc-123"


def _build_token_list_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": {
                "tokens": [
                    {
                        "token": TOKEN_VALUE,
                        "code": "VISA",
                        "display": "Visa ***1234",
                        "bin": "411111",
                        "name_holder": "John Doe",
                        "expiry_date": "2512",
                        "is_expired": False,
                        "last_four": "1234",
                        "model": "cardOnFile",
                    },
                ],
            },
        },
    )


def _build_single_token_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": {
                "token": TOKEN_VALUE,
                "code": "VISA",
                "display": "Visa ***1234",
            },
        },
    )


def _build_empty_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={"success": True, "data": {}},
    )


def test_get_list_returns_tokens() -> None:
    """Get_list parses a list of Token objects."""
    client = MagicMock()
    client.create_get_request.return_value = _build_token_list_response()

    manager = RecurringManager(client)
    response = manager.get_list(reference=REFERENCE)

    called_endpoint = client.create_get_request.call_args.args[0]

    assert isinstance(response, CustomApiResponse)
    assert isinstance(response.get_data(), list)
    assert len(response.get_data()) == 1
    assert response.get_data()[0].token == TOKEN_VALUE
    assert f"json/recurring/{REFERENCE}" == called_endpoint


def test_get_returns_single_token() -> None:
    """Get parses a single Token object."""
    client = MagicMock()
    client.create_get_request.return_value = _build_single_token_response()

    manager = RecurringManager(client)
    response = manager.get(token=TOKEN_VALUE, reference=REFERENCE)

    called_endpoint = client.create_get_request.call_args.args[0]

    assert isinstance(response, CustomApiResponse)
    assert response.get_data().token == TOKEN_VALUE
    assert TOKEN_VALUE in called_endpoint
    assert REFERENCE in called_endpoint


def test_get_returns_none_for_empty_data() -> None:
    """Get returns None when body data is empty."""
    client = MagicMock()
    client.create_get_request.return_value = _build_empty_response()

    manager = RecurringManager(client)
    response = manager.get(token=TOKEN_VALUE, reference=REFERENCE)

    assert isinstance(response, CustomApiResponse)
    assert response.get_data() is None


def test_delete_sends_delete_request() -> None:
    """Delete sends DELETE to the correct endpoint."""
    client = MagicMock()
    client.create_delete_request.return_value = _build_empty_response()

    manager = RecurringManager(client)
    response = manager.delete(reference=REFERENCE, token=TOKEN_VALUE)

    called_endpoint = client.create_delete_request.call_args.args[0]

    assert isinstance(response, CustomApiResponse)
    assert response.get_data() is None
    assert REFERENCE in called_endpoint
    assert TOKEN_VALUE in called_endpoint
    assert "remove" in called_endpoint
