# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.paths.auth.api_token.response.api_token import ApiToken


def test_initialization_api_token():
    """
    Test that the ApiToken object initializes correctly with a given token.

    This test verifies that the ApiToken object initializes with the correct
    value for the api_token attribute.

    """
    api_token = ApiToken(api_token="test_token")
    assert api_token.api_token == "test_token"


def test_initialization_api_token_none():
    """
    Test that the ApiToken object initializes correctly with no token.

    This test verifies that the ApiToken object initializes with None
    for the api_token attribute when no token is provided.

    """
    api_token = ApiToken()
    assert api_token.api_token is None


def test_initialization_with_valid_data():
    """
    Test that the from_dict method initializes an ApiToken object with valid data.

    This test verifies that the from_dict method correctly creates an ApiToken
    object from a dictionary containing valid data.

    """
    data = {"api_token": "valid_token"}
    api_token = ApiToken.from_dict(data)
    assert api_token.api_token == "valid_token"


def test_initialization_with_empty_data():
    """
    Test that the from_dict method initializes an ApiToken object with empty data.

    This test verifies that the from_dict method correctly creates an ApiToken
    object from an empty dictionary, resulting in None for the api_token attribute.

    """
    data = {}
    api_token = ApiToken.from_dict(data)
    assert api_token.api_token is None


def test_initialization_with_none_data():
    """
    Test that the from_dict method returns None when the input dictionary is None.

    This test verifies that the from_dict method returns None when None is provided
    as the input dictionary.

    """
    data = None
    api_token = ApiToken.from_dict(data)
    assert api_token is None


def test_initialization_with_partial_data():
    """
    Test that the from_dict method handles partial data by setting api_token to None.

    This test verifies that the from_dict method correctly creates an ApiToken
    object from a dictionary with missing fields, resulting in None for the
    api_token attribute.


    """
    data = {"some_other_key": "value"}
    api_token = ApiToken.from_dict(data)
    assert api_token.api_token is None
