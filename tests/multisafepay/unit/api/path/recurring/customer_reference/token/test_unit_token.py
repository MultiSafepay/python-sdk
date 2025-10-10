# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.recurring.customer_reference.token.token import (
    Token,
)


def test_initialization_with_valid_data():
    """
    Test that the Token object initializes correctly with valid data.

    This test verifies that the Token object initializes with the correct
    values for all attributes.
    """
    token = Token(
        token="token_value",
        code="code_value",
        display="display_value",
        bin="bin_value",
        name_holder="name_holder_value",
        expiry_date="expiry_date_value",
        is_expired=False,
        last_four="1234",
        model="model_value",
    )
    assert token.token == "token_value"
    assert token.code == "code_value"
    assert token.display == "display_value"
    assert token.bin == "bin_value"
    assert token.name_holder == "name_holder_value"
    assert token.expiry_date == "expiry_date_value"
    assert token.is_expired is False
    assert token.last_four == "1234"
    assert token.model == "model_value"


def test_initialization_with_no_data():
    """
    Test that the Token object initializes correctly with None values.

    This test verifies that the Token object initializes with None
    for all attributes.
    """
    token = Token()
    assert token.token is None
    assert token.code is None
    assert token.display is None
    assert token.bin is None
    assert token.name_holder is None
    assert token.expiry_date is None
    assert token.is_expired is None
    assert token.last_four is None
    assert token.model is None


def test_from_dict_returns_none_for_none_input():
    """
    Test that from_dict returns None when the input dictionary is None.

    This test verifies that the from_dict method returns None when None is provided.
    """
    token = Token.from_dict(None)
    assert token is None


def test_from_dict_initializes_token_with_valid_data():
    """
    Test that from_dict initializes a Token instance with valid data.

    This test verifies that the Token object is correctly created
    from a dictionary containing valid data.
    """
    data = {
        "token": "token_value",
        "code": "code_value",
        "display": "display_value",
        "bin": "bin_value",
        "name_holder": "name_holder_value",
        "expiry_date": "expiry_date_value",
        "is_expired": False,
        "last_four": "1234",
        "model": "model_value",
    }
    token = Token.from_dict(data)
    assert token.token == "token_value"
    assert token.code == "code_value"
    assert token.display == "display_value"
    assert token.bin == "bin_value"
    assert token.name_holder == "name_holder_value"
    assert token.expiry_date == "expiry_date_value"
    assert token.is_expired is False
    assert token.last_four == "1234"
    assert token.model == "model_value"


def test_from_dict_handles_missing_fields():
    """
    Test that from_dict handles missing fields by setting them to None.

    This test verifies that the Token object is correctly created
    from a dictionary with missing fields, resulting in None values for
    all attributes.
    """
    data = {}
    token = Token.from_dict(data)
    assert token.token is None
    assert token.code is None
    assert token.display is None
    assert token.bin is None
    assert token.name_holder is None
    assert token.expiry_date is None
    assert token.is_expired is None
    assert token.last_four is None
    assert token.model is None
