# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the issuer response model."""


from multisafepay.api.paths.issuers.response.issuer import Issuer


def test_initializes_correctly():
    """
    Test that the Issuer initializes correctly with given parameters.

    This test verifies that the Issuer object is initialized with the correct
    gateway code, code, and description.
    """
    issuer = Issuer(
        gateway_code="mybank",
        code="123",
        description="Test Issuer",
    )
    assert issuer.gateway_code == "mybank"
    assert issuer.code == "123"
    assert issuer.description == "Test Issuer"


def test_initializes_with_none_values():
    """
    Test that Issuer initializes with None values.

    This test verifies that all attributes all optional.
    """
    issuer = Issuer()
    assert issuer.gateway_code is None
    assert issuer.code is None
    assert issuer.description is None


def test_from_dict_creates_issuer_instance():
    """
    Test that from_dict method creates an Issuer instance correctly.

    This test verifies that the from_dict method of the Issuer class
    creates an Issuer instance with the correct attributes from a dictionary.
    """
    data = {
        "gateway_code": "mybank",
        "code": "123",
        "description": "Test Issuer",
    }
    issuer = Issuer.from_dict(data)
    assert issuer.gateway_code == "mybank"
    assert issuer.code == "123"
    assert issuer.description == "Test Issuer"


def test_from_dict_handles_missing_fields():
    """
    Test that from_dict method handles missing fields.

    This test verifies that the from_dict method of the Issuer class
    returns an Issuer instance with None values for missing fields.
    """
    data = {}
    issuer = Issuer.from_dict(data)
    assert issuer.gateway_code is None
    assert issuer.code is None
    assert issuer.description is None


def test_from_dict_returns_none_for_none_input():
    """
    Test that from_dict method returns None for None input.

    This test verifies that the from_dict method of the Issuer class
    returns None when the input dictionary is None.
    """
    assert Issuer.from_dict(None) is None
