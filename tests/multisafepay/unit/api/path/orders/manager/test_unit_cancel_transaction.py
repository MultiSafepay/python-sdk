# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for OrderManager.cancel_transaction behavior."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.orders.order_id.cancel.request.cancel_transaction_request import (
    CancelTransactionRequest,
)
from multisafepay.api.paths.orders.order_id.cancel.response.cancel_transaction import (
    CancelTransaction,
)
from multisafepay.api.paths.orders.order_manager import OrderManager
from multisafepay.client.credential_resolver import (
    AuthScope,
    ScopedCredentialResolver,
)

ORDER_ID = "cloud-pos-cancel-1"
TERMINAL_GROUP_ID = "Default"


def _build_cancel_api_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": {
                "status": "void",
                "financial_status": "void",
                "created": "2026-01-01T00:00:00",
                "modified": "2026-01-01T00:00:01",
            },
        },
    )


def test_cancel_transaction_with_terminal_group_scope() -> None:
    """Use terminal-group auth scope when terminal_group_id is provided."""
    client = MagicMock()
    client.create_post_request.return_value = _build_cancel_api_response()

    manager = OrderManager(client)
    response = manager.cancel_transaction(
        cancel_transaction_request=ORDER_ID,
        terminal_group_id=TERMINAL_GROUP_ID,
    )

    called_auth_scope = client.create_post_request.call_args.kwargs[
        "auth_scope"
    ]

    assert isinstance(response, CustomApiResponse)
    assert isinstance(response.get_data(), CancelTransaction)
    assert response.get_data().status == "void"
    assert called_auth_scope == AuthScope(
        scope=ScopedCredentialResolver.AUTH_SCOPE_TERMINAL_GROUP,
        group_id=TERMINAL_GROUP_ID,
    )


def test_cancel_transaction_without_terminal_group_scope() -> None:
    """Omit auth scope when terminal_group_id is not provided."""
    client = MagicMock()
    client.create_post_request.return_value = _build_cancel_api_response()

    manager = OrderManager(client)
    response = manager.cancel_transaction(
        cancel_transaction_request=ORDER_ID,
    )

    called_auth_scope = client.create_post_request.call_args.kwargs[
        "auth_scope"
    ]

    assert isinstance(response, CustomApiResponse)
    assert called_auth_scope is None


def test_cancel_transaction_accepts_request_object() -> None:
    """Accept CancelTransactionRequest as input instead of raw string."""
    client = MagicMock()
    client.create_post_request.return_value = _build_cancel_api_response()

    request = CancelTransactionRequest(order_id=ORDER_ID)

    manager = OrderManager(client)
    response = manager.cancel_transaction(
        cancel_transaction_request=request,
        terminal_group_id=TERMINAL_GROUP_ID,
    )

    called_endpoint = client.create_post_request.call_args.args[0]

    assert isinstance(response, CustomApiResponse)
    assert ORDER_ID in called_endpoint
    assert called_endpoint.endswith("/cancel")


def test_cancel_transaction_encodes_order_id() -> None:
    """Verify order ID with special chars is encoded in the endpoint."""
    client = MagicMock()
    client.create_post_request.return_value = _build_cancel_api_response()

    manager = OrderManager(client)
    manager.cancel_transaction(
        cancel_transaction_request="order/special&chars",
    )

    called_endpoint = client.create_post_request.call_args.args[0]
    assert "order%2Fspecial%26chars" in called_endpoint
