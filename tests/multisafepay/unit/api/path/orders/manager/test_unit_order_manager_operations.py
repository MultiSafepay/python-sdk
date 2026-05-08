# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for OrderManager get, update, capture, and refund methods."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.orders.order_manager import OrderManager
from multisafepay.api.paths.orders.response.order_response import Order

ORDER_ID = "test-order-1"


def _build_order_api_response(order_id: str) -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": {
                "order_id": order_id,
                "status": "completed",
            },
        },
    )


def _build_empty_api_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={"success": True, "data": {}},
    )


def _build_capture_api_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": {
                "order_id": ORDER_ID,
                "status": "completed",
            },
        },
    )


def _build_refund_api_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": {
                "refund_id": "refund-1",
                "order_id": ORDER_ID,
            },
        },
    )


def test_get_order_by_id() -> None:
    """Retrieve an order by its ID."""
    client = MagicMock()
    client.create_get_request.return_value = _build_order_api_response(
        ORDER_ID,
    )

    manager = OrderManager(client)
    response = manager.get(order_id=ORDER_ID)

    called_endpoint = client.create_get_request.call_args.args[0]

    assert isinstance(response, CustomApiResponse)
    assert isinstance(response.get_data(), Order)
    assert response.get_data().order_id == ORDER_ID
    assert ORDER_ID in called_endpoint


def test_get_order_encodes_special_chars_in_id() -> None:
    """Verify order ID with special chars is encoded in the URL."""
    client = MagicMock()
    client.create_get_request.return_value = _build_order_api_response(
        "order/special",
    )

    manager = OrderManager(client)
    manager.get(order_id="order/special")

    called_endpoint = client.create_get_request.call_args.args[0]
    assert "order%2Fspecial" in called_endpoint


def test_get_order_returns_none_for_empty_data() -> None:
    """Return None when body data is empty."""
    client = MagicMock()
    client.create_get_request.return_value = _build_empty_api_response()

    manager = OrderManager(client)
    response = manager.get(order_id=ORDER_ID)

    assert isinstance(response, CustomApiResponse)
    assert response.get_data() is None


def test_update_order_sends_patch_request() -> None:
    """Update sends PATCH to the correct endpoint."""
    client = MagicMock()
    client.create_patch_request.return_value = _build_empty_api_response()

    update_request = MagicMock()
    update_request.to_dict.return_value = {"description": "updated"}

    manager = OrderManager(client)
    response = manager.update(order_id=ORDER_ID, update_request=update_request)

    called_endpoint = client.create_patch_request.call_args.args[0]

    assert isinstance(response, CustomApiResponse)
    assert ORDER_ID in called_endpoint


def test_capture_order_sends_post_and_parses_response() -> None:
    """Capture sends POST and parses OrderCapture response."""
    client = MagicMock()
    client.create_post_request.return_value = _build_capture_api_response()

    capture_request = MagicMock()
    capture_request.to_dict.return_value = {"amount": 100}

    manager = OrderManager(client)
    response = manager.capture(
        order_id=ORDER_ID,
        capture_request=capture_request,
    )

    called_endpoint = client.create_post_request.call_args.args[0]

    assert isinstance(response, CustomApiResponse)
    assert f"json/orders/{ORDER_ID}/capture" == called_endpoint


def test_refund_order_sends_post_and_parses_response() -> None:
    """Refund sends POST and parses OrderRefund response."""
    client = MagicMock()
    client.create_post_request.return_value = _build_refund_api_response()

    refund_request = MagicMock()
    refund_request.to_dict.return_value = {"amount": 50}

    manager = OrderManager(client)
    response = manager.refund(
        order_id=ORDER_ID,
        request_refund=refund_request,
    )

    called_endpoint = client.create_post_request.call_args.args[0]

    assert isinstance(response, CustomApiResponse)
    assert f"json/orders/{ORDER_ID}/refunds" == called_endpoint
