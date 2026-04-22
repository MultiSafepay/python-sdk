# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for CaptureManager.capture_reservation_cancel behavior."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.capture.capture_manager import CaptureManager
from multisafepay.api.paths.capture.request.capture_request import (
    CaptureRequest,
)
from multisafepay.api.paths.capture.response.capture import CancelReservation

ORDER_ID = "capture-order-1"


def _build_capture_api_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": {
                "order_id": ORDER_ID,
                "success": True,
                "transaction_id": "txn-001",
            },
        },
    )


def _build_empty_capture_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={"success": True, "data": {}},
    )


def test_capture_reservation_cancel_sends_patch_and_parses() -> None:
    """Send PATCH to json/capture/{order_id} and parse CancelReservation."""
    client = MagicMock()
    client.create_patch_request.return_value = _build_capture_api_response()

    request = CaptureRequest(status="cancelled", reason="test")

    manager = CaptureManager(client)
    response = manager.capture_reservation_cancel(
        order_id=ORDER_ID,
        capture_request=request,
    )

    called_endpoint = client.create_patch_request.call_args.args[0]

    assert isinstance(response, CustomApiResponse)
    assert isinstance(response.get_data(), CancelReservation)
    assert response.get_data().order_id == ORDER_ID
    assert f"json/capture/{ORDER_ID}" == called_endpoint


def test_capture_reservation_cancel_empty_data() -> None:
    """Return None data when body data is empty."""
    client = MagicMock()
    client.create_patch_request.return_value = _build_empty_capture_response()

    request = CaptureRequest(status="cancelled", reason="test")

    manager = CaptureManager(client)
    response = manager.capture_reservation_cancel(
        order_id=ORDER_ID,
        capture_request=request,
    )

    assert isinstance(response, CustomApiResponse)
    assert response.get_data() is None
