# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.me.me_manager import MeManager
from multisafepay.api.paths.me.response.me import Me


def test_integration_me_manager_get():
    """
    Test that the MeManager correctly retrieves and processes the 'me' data.

    This test verifies that the MeManager's get method returns a CustomApiResponse
    object containing the expected 'me' data when the API response is successful.

    """
    client = MagicMock()
    client.create_get_request.return_value = ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": {"account_id": 1, "role": "admin", "site_id": 100},
        },
    )
    manager = MeManager(client)
    response = manager.get()
    assert isinstance(response, CustomApiResponse)
    assert isinstance(response.get_data(), Me)
    assert response.get_data() == Me(account_id=1, role="admin", site_id=100)
