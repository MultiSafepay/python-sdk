# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.payment_methods.response.payment_method import (
    PaymentMethod,
)


def test_initializes_correctly():
    """
    Test that the PaymentMethod object initializes correctly with given data.

    This test verifies that the PaymentMethod object initializes with the correct
    values for all attributes when valid data is provided.
    """
    payment_method = PaymentMethod(
        additional_data={"key": "value"},
        allowed_amount=None,
        allowed_countries=["NL", "US"],
        allowed_currencies=["EUR", "USD"],
        apps=None,
        brands=None,
        description="Test Payment Method",
        icon_urls=None,
        id="test_id",
        label="Test Label",
        name="Test Name",
        preferred_countries=["NL"],
        required_customer_data=["email"],
        tokenization=None,
        type="test_type",
    )
    assert payment_method.additional_data == {"key": "value"}
    assert payment_method.allowed_amount is None
    assert payment_method.allowed_countries == ["NL", "US"]
    assert payment_method.allowed_currencies == ["EUR", "USD"]
    assert payment_method.apps is None
    assert payment_method.brands is None
    assert payment_method.description == "Test Payment Method"
    assert payment_method.icon_urls is None
    assert payment_method.id == "test_id"
    assert payment_method.label == "Test Label"
    assert payment_method.name == "Test Name"
    assert payment_method.preferred_countries == ["NL"]
    assert payment_method.required_customer_data == ["email"]
    assert payment_method.tokenization is None
    assert payment_method.type == "test_type"


def test_from_dict_creates_payment_method_instance_correctly():
    """
    Test that the from_dict method initializes a PaymentMethod object with valid data.

    This test verifies that the from_dict method correctly creates a PaymentMethod
    object from a dictionary containing valid data.
    """
    data = {
        "additional_data": {"key": "value"},
        "allowed_amount": None,
        "allowed_countries": ["NL", "US"],
        "allowed_currencies": ["EUR", "USD"],
        "apps": None,
        "brands": None,
        "description": "Test Payment Method",
        "icon_urls": None,
        "id": "test_id",
        "label": "Test Label",
        "name": "Test Name",
        "preferred_countries": ["NL"],
        "required_customer_data": ["email"],
        "tokenization": None,
        "type": "test_type",
    }
    payment_method = PaymentMethod.from_dict(data)
    assert payment_method.additional_data == {"key": "value"}
    assert payment_method.allowed_amount is None
    assert payment_method.allowed_countries == ["NL", "US"]
    assert payment_method.allowed_currencies == ["EUR", "USD"]
    assert payment_method.apps is None
    assert payment_method.brands is None
    assert payment_method.description == "Test Payment Method"
    assert payment_method.icon_urls is None
    assert payment_method.id == "test_id"
    assert payment_method.label == "Test Label"
    assert payment_method.name == "Test Name"
    assert payment_method.preferred_countries == ["NL"]
    assert payment_method.required_customer_data == ["email"]
    assert payment_method.tokenization is None
    assert payment_method.type == "test_type"
