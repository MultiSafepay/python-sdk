# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for PosManager.get_receipt behavior."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.pos.pos_manager import PosManager
from multisafepay.api.paths.pos.receipt.response.receipt import Receipt
from multisafepay.client.credential_resolver import (
    AuthScope,
    ScopedCredentialResolver,
)

ORDER_ID = "cloud-pos-order-1"
TERMINAL_GROUP_ID = "Default"


def _build_receipt_api_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": {
                "merchant": {"name": "Test Merchant", "address": "123 St"},
                "order": {
                    "order_id": ORDER_ID,
                    "amount": 100,
                    "currency": "EUR",
                    "status": "completed",
                    "financial_status": "completed",
                    "created": "2026-01-01T00:00:00",
                    "modified": "2026-01-01T00:00:01",
                    "completed": "2026-01-01T00:00:02",
                    "amount_refunded": 0,
                    "transaction_id": 12345,
                    "items": [
                        {
                            "name": "Widget",
                            "quantity": 1,
                            "unit_price": 100,
                            "item_price": 100,
                            "currency": "EUR",
                        },
                    ],
                    "tip": [
                        {
                            "amount": 50,
                            "employee": [
                                {"id": "emp-1", "name": "Alice"},
                            ],
                        },
                    ],
                },
                "payment": {
                    "payment_method": "VISA",
                    "last4": "1234",
                    "terminal_id": "T-001",
                    "authorization_code": 123456,
                    "application_id": "A001",
                    "card_acceptor_location": "NL",
                    "card_entry_mode": "contactless",
                    "card_expiry_date": "12/28",
                    "cardholder_verification_method": "pin",
                    "issuer_bin": "411111",
                    "issuer_country_code": "NL",
                    "response_code": "00",
                },
                "printed_on": "2026-01-01T00:00:03",
                "related_transactions": {
                    "amount": 100,
                    "created": "2026-01-01T00:00:00",
                    "currency": "EUR",
                    "description": "Refund",
                    "items": None,
                    "modified": "2026-01-01T00:00:01",
                    "order_id": ORDER_ID,
                    "reference_transaction_id": 99999,
                    "status": "completed",
                    "transaction_id": 12346,
                    "type": "refund",
                },
            },
        },
    )


def _build_empty_receipt_api_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={"success": True, "data": {}},
    )


def test_get_receipt_with_terminal_group_scope() -> None:
    """Use terminal-group auth scope when terminal_group_id is provided."""
    client = MagicMock()
    client.create_get_request.return_value = _build_receipt_api_response()

    manager = PosManager(client)
    response = manager.get_receipt(
        order_id=ORDER_ID,
        terminal_group_id=TERMINAL_GROUP_ID,
    )

    called_auth_scope = client.create_get_request.call_args.kwargs[
        "auth_scope"
    ]

    assert isinstance(response, CustomApiResponse)
    assert isinstance(response.get_data(), Receipt)
    assert response.get_data().printed_on == "2026-01-01T00:00:03"
    assert called_auth_scope == AuthScope(
        scope=ScopedCredentialResolver.AUTH_SCOPE_TERMINAL_GROUP,
        group_id=TERMINAL_GROUP_ID,
    )


def test_get_receipt_without_terminal_group_scope() -> None:
    """Omit auth scope when terminal_group_id is not provided."""
    client = MagicMock()
    client.create_get_request.return_value = _build_receipt_api_response()

    manager = PosManager(client)
    response = manager.get_receipt(order_id=ORDER_ID)

    called_auth_scope = client.create_get_request.call_args.kwargs[
        "auth_scope"
    ]

    assert isinstance(response, CustomApiResponse)
    assert isinstance(response.get_data(), Receipt)
    assert called_auth_scope is None


def test_get_receipt_parses_nested_receipt_components() -> None:
    """Verify receipt response parses all nested model components."""
    client = MagicMock()
    client.create_get_request.return_value = _build_receipt_api_response()

    manager = PosManager(client)
    response = manager.get_receipt(
        order_id=ORDER_ID,
        terminal_group_id=TERMINAL_GROUP_ID,
    )
    receipt = response.get_data()

    assert receipt.merchant.name == "Test Merchant"
    assert receipt.merchant.address == "123 St"
    assert receipt.order.order_id == ORDER_ID
    assert receipt.order.amount == 100
    assert len(receipt.order.items) == 1
    assert receipt.order.items[0].name == "Widget"
    assert len(receipt.order.tip) == 1
    assert receipt.order.tip[0].amount == 50
    assert receipt.order.tip[0].employee[0].name == "Alice"
    assert receipt.payment.payment_method == "VISA"
    assert receipt.payment.last4 == "1234"
    assert receipt.related_transactions.transaction_id == 12346
    assert receipt.related_transactions.type == "refund"


def test_get_receipt_returns_none_data_for_empty_body() -> None:
    """Return None data when body data is empty."""
    client = MagicMock()
    client.create_get_request.return_value = (
        _build_empty_receipt_api_response()
    )

    manager = PosManager(client)
    response = manager.get_receipt(order_id=ORDER_ID)

    assert isinstance(response, CustomApiResponse)
    assert response.get_data() is None


def test_get_receipt_encodes_order_id_in_endpoint() -> None:
    """Verify order ID with special chars is encoded in the URL."""
    client = MagicMock()
    client.create_get_request.return_value = _build_receipt_api_response()

    manager = PosManager(client)
    manager.get_receipt(order_id="order/special&chars")

    called_endpoint = client.create_get_request.call_args.args[0]
    assert "order%2Fspecial%26chars" in called_endpoint
