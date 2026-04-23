# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for basic order manager create behavior."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.orders.order_manager import OrderManager
from multisafepay.api.paths.orders.request.order_request import OrderRequest
from multisafepay.api.paths.orders.response.order_response import Order
from multisafepay.client.client import Client
from multisafepay.client.credential_resolver import AuthScope

ORDERS_ENDPOINT = "json/orders"
TERMINAL_GROUP_ID = "Default"
SCOPED_ORDER_ID = "cloud-pos-order"
DEFAULT_ORDER_ID = "default-order"


def _build_api_response(order_id: str) -> ApiResponse:
    """Create a minimal successful ApiResponse for order manager tests."""
    return ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": {
                "order_id": order_id,
            },
        },
    )


def _build_order_request(order_id: str) -> OrderRequest:
    """Create a minimal valid order request used in create() tests."""
    return (
        OrderRequest()
        .add_type("direct")
        .add_order_id(order_id)
        .add_currency("EUR")
        .add_amount(100)
    )


def test_create_uses_terminal_group_auth_scope_when_provided() -> None:
    """Use terminal-group scope only when terminal_group_id is passed."""
    client = MagicMock()
    client.create_post_request.return_value = _build_api_response(
        SCOPED_ORDER_ID,
    )
    request_order = _build_order_request(SCOPED_ORDER_ID)

    manager = OrderManager(client)
    response = manager.create(
        request_order=request_order,
        terminal_group_id=TERMINAL_GROUP_ID,
    )

    called_endpoint = client.create_post_request.call_args.args[0]
    called_auth_scope = client.create_post_request.call_args.kwargs[
        "auth_scope"
    ]

    assert isinstance(response, CustomApiResponse)
    assert isinstance(response.get_data(), Order)
    assert called_endpoint == ORDERS_ENDPOINT
    assert called_auth_scope == AuthScope(
        scope=Client.AUTH_SCOPE_TERMINAL_GROUP,
        group_id=TERMINAL_GROUP_ID,
    )


def test_create_omits_auth_scope_when_terminal_group_id_is_not_passed() -> (
    None
):
    """Do not set auth_scope when create request has no terminal group id."""
    client = MagicMock()
    client.create_post_request.return_value = _build_api_response(
        DEFAULT_ORDER_ID,
    )
    request_order = _build_order_request(DEFAULT_ORDER_ID)

    manager = OrderManager(client)
    response = manager.create(request_order=request_order)

    called_endpoint = client.create_post_request.call_args.args[0]
    called_auth_scope = client.create_post_request.call_args.kwargs[
        "auth_scope"
    ]

    assert isinstance(response, CustomApiResponse)
    assert isinstance(response.get_data(), Order)
    assert response.get_data().order_id == DEFAULT_ORDER_ID
    assert called_endpoint == ORDERS_ENDPOINT
    assert called_auth_scope is None
