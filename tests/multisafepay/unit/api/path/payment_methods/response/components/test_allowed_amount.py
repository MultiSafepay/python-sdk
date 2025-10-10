# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.payment_methods.response.components.allowed_amount import (
    AllowedAmount,
)


def test_initializes_correctly():
    """
    Test that the AllowedAmount object initializes correctly with given parameters.

    This test verifies that the AllowedAmount object is initialized with the correct
    min and max values.
    """
    allowed_amount = AllowedAmount(min=10, max=100)
    assert allowed_amount.min == 10
    assert allowed_amount.max == 100


def test_from_dict_creates_allowed_amount_instance_correctly():
    """
    Test that from_dict method creates an AllowedAmount instance correctly.

    This test verifies that the from_dict method of the AllowedAmount class
    creates an AllowedAmount instance with the correct attributes from a dictionary.
    """
    data = {"min": 10, "max": 100}
    allowed_amount = AllowedAmount.from_dict(data)
    assert allowed_amount.min == 10
    assert allowed_amount.max == 100


def test_from_dict_returns_none_for_none_input():
    """
    Test that from_dict method returns None for None input.

    This test verifies that the from_dict method of the AllowedAmount class
    returns None when the input dictionary is None.
    """
    assert AllowedAmount.from_dict(None) is None


def test_from_dict_handles_missing_fields():
    """
    Test that from_dict method handles missing fields correctly.

    This test verifies that the from_dict method of the AllowedAmount class
    creates an AllowedAmount instance with None for missing fields in the input dictionary.
    """
    data = {"min": 10}
    allowed_amount = AllowedAmount.from_dict(data)
    assert allowed_amount.min == 10
    assert allowed_amount.max is None
