# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Manager class for Test Integration Gateways Manager Get Gateways.Py API operations."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.gateways.gateway_manager import GatewayManager
from multisafepay.api.paths.gateways.response.gateway import Gateway


def test_get_gateways():
    """
    Test the get_gateways method of GatewayManager.

    This test mocks the client to return a successful response with a list of gateway data.
    It then verifies that the get_gateways method of GatewayManager correctly retrieves
    the list of gateways and returns a CustomApiResponse object.

    """
    client = MagicMock()
    client.create_get_request.return_value = ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": [
                {"id": "BIZUM", "description": "Bizum"},
                {
                    "id": "ALPHABAIT",
                    "description": "Alphabait Giftcardt",
                    "type": "coupon",
                },
            ],
        },
    )
    manager = GatewayManager(client)
    response = manager.get_gateways()
    assert isinstance(response, CustomApiResponse)
    assert response.get_data() == [
        Gateway(id="BIZUM", description="Bizum"),
        Gateway(
            id="ALPHABAIT",
            description="Alphabait Giftcardt",
            type="coupon",
        ),
    ]
