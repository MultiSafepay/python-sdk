# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Manager class for Test Integration Categories Manager Get Categories.Py API operations."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.categories.category_manager import CategoryManager
from multisafepay.api.paths.categories.response.category import Category


def test_get_categories():
    """
    Test the get_categories method of CategoryManager with a valid response.

    This test mocks the client to return a valid ApiResponse and verifies
    that the get_categories method returns a CustomApiResponse with the expected
    Category data.

    """
    client = MagicMock()
    client.create_get_request.return_value = ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": [
                {"code": "1237", "description": "Accounting services"},
                {
                    "code": "1202",
                    "description": "A/c, plumbing and heating contractors",
                },
            ],
        },
    )
    manager = CategoryManager(client)
    response = manager.get_categories()
    assert isinstance(response, CustomApiResponse)
    assert response.get_data() == [
        Category(code="1237", description="Accounting services"),
        Category(
            code="1202",
            description="A/c, plumbing and heating contractors",
        ),
    ]
