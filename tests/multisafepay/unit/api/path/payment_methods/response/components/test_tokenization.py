# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.payment_methods.response.components.tokenization import (
    Tokenization,
)


def test_initializes_correctly():
    """
    Test that the Tokenization object initializes correctly with given values.

    This test verifies that the Tokenization object is initialized with the provided
    is_enabled and models attributes.
    """
    tokenization = Tokenization(is_enabled=True, models=None)
    assert tokenization.is_enabled is True
    assert tokenization.models is None


def test_from_dict_creates_tokenization_instance_correctly():
    """
    Test that from_dict method creates a Tokenization instance correctly.

    This test verifies that the from_dict method of the Tokenization class
    creates a Tokenization instance with the correct attributes from a dictionary.
    """
    data = {"is_enabled": True, "models": None}
    tokenization = Tokenization.from_dict(data)
    assert tokenization.is_enabled is True
    assert tokenization.models is None


def test_from_dict_returns_none_for_none_input():
    """
    Test that from_dict method returns None for None input.

    This test verifies that the from_dict method of the Tokenization class
    returns None when the input dictionary is None..
    """
    assert Tokenization.from_dict(None) is None


def test_from_dict_handles_missing_fields():
    """
    Test that from_dict method handles missing fields correctly.

    This test verifies that the from_dict method of the Tokenization class
    handles missing fields in the input dictionary correctly.
    """
    data = {}
    tokenization = Tokenization.from_dict(data)
    assert tokenization.is_enabled is None
    assert tokenization.models is None
