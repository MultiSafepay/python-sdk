# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Manager class for Test Integration Capture Manager Capture Reservation Cancel.Py API operations."""

from unittest.mock import Mock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.capture.capture_manager import CaptureManager
from multisafepay.api.paths.capture.request.capture_request import (
    CaptureRequest,
)
from multisafepay.api.paths.capture.response.capture import CancelReservation


def test_capture_reservation_cancel():
    """
    Test the capture_reservation_cancel method of CaptureManager.

    This test verifies that the capture_reservation_cancel method correctly
    processes a cancellation request and returns a CustomApiResponse object
    with the expected data.

    The test uses a mock client to simulate the API response.

    """
    client = Mock()
    capture_request = CaptureRequest(status="cancelled", reason="valid_reason")
    response_data = {
        "success": True,
        "data": {
            "transaction_id": "100100100100100",
            "order_id": "<example_order_id>",
            "success": True,
        },
    }
    client.create_patch_request.return_value = ApiResponse(
        headers="",
        status_code=200,
        body=response_data,
    )
    capture_manager = CaptureManager(client)

    response = capture_manager.capture_reservation_cancel(
        "<example_order_id>",
        capture_request,
    )
    assert isinstance(response, CustomApiResponse)

    assert response.get_data() == CancelReservation(
        order_id="<example_order_id>",
        success=True,
        transaction_id="100100100100100",
    )
