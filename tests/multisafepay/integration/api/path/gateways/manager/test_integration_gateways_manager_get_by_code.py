# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Manager class for Test Integration Gateways Manager Get By Code.Py API operations."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.paths.gateways.gateway_manager import GatewayManager
from multisafepay.api.paths.gateways.response.gateway import Gateway


def test_capture_reservation_cancel_with_valid_data():
    """
    Test the capture reservation cancel functionality with valid data.

    This test mocks the client to return a successful response with valid gateway data.
    It then verifies that the `get_by_code` method of `GatewayManager` correctly retrieves
    the gateway data.

    """
    client = MagicMock()
    client.create_get_request.return_value = ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": {"id": "IDEAL", "description": "iDEAL"},
        },
    )
    capture_manager = GatewayManager(client)

    response = capture_manager.get_by_code("IDEAL")

    assert response.get_data() == Gateway(id="IDEAL", description="iDEAL")
