# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the gateway response model."""


from multisafepay.api.paths.gateways.response.gateway import Gateway


def test_initializes_with_id_description_and_type():
    """
    Test that the Gateway object initializes correctly with id, description, and type.

    This test verifies that the Gateway object initializes with the correct
    values for the id, description, and type attributes.
    """
    gateway = Gateway(id="123", description="Test Gateway", type="Credit Card")
    assert gateway.id == "123"
    assert gateway.description == "Test Gateway"
    assert gateway.type == "Credit Card"


def test_initializes_with_none_values():
    """
    Test that the Gateway object initializes correctly with None values.

    This test verifies that the Gateway object initializes with None
    for the id, description, and type attributes when no data is provided.
    """
    gateway = Gateway()
    assert gateway.id is None
    assert gateway.description is None
    assert gateway.type is None


def test_from_dict_creates_instance_from_dict():
    """
    Test that the from_dict method initializes a Gateway object with valid data.

    This test verifies that the from_dict method correctly creates a Gateway
    object from a dictionary containing valid data.
    """
    data = {"id": "123", "description": "Test Gateway", "type": "Credit Card"}
    gateway: Gateway | None = Gateway.from_dict(data)
    assert gateway.id == "123"
    assert gateway.description == "Test Gateway"
    assert gateway.type == "Credit Card"


def test_from_dict_returns_none_for_none_input():
    """
    Test that the from_dict method returns None when the input dictionary is None.

    This test verifies that the from_dict method returns None when None is provided
    as the input dictionary.
    """
    gateway = Gateway.from_dict(None)
    assert gateway is None


def test_from_dict_handles_missing_fields():
    """
    Test that the from_dict method handles missing fields by setting them to None.

    This test verifies that the from_dict method correctly creates a Gateway
    object from a dictionary with missing fields, resulting in None values for
    the id, description, and type attributes.
    """
    data = {}
    gateway: Gateway | None = Gateway.from_dict(data)
    assert gateway.id is None
    assert gateway.description is None
    assert gateway.type is None
