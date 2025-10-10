# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Manager class for Test Integration Auth Manager Get Api Token.Py API operations."""

from multisafepay.api.paths.auth.api_token.response.api_token import ApiToken
from multisafepay.api.paths.auth.auth_manager import AuthManager
from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from unittest.mock import MagicMock


def test_get_api_token_with_valid_response():
    """
    Test the get_api_token method of AuthManager with a valid response.

    This test mocks the client to return a valid ApiResponse and verifies
    that the get_api_token method returns a CustomApiResponse with the expected
    ApiToken data.

    """
    client = MagicMock()
    client.create_get_request.return_value = ApiResponse(
        headers={},
        status_code=200,
        body={"success": True, "data": {"api_token": "pub.v2.fake"}},
    )
    auth_manager = AuthManager(client)
    response = auth_manager.get_api_token()
    assert isinstance(response, CustomApiResponse)
    assert response.data == ApiToken(api_token="pub.v2.fake")
