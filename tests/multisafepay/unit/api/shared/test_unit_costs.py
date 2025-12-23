# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the shared costs model."""

from decimal import Decimal

from multisafepay.api.shared.costs import Costs


def test_initializes_with_valid_values():
    """Test that a Costs instance initializes with valid values."""
    costs = Costs(
        transaction_id=123,
        description="Service Fee",
        type="Fixed",
        amount=99.99,
        currency="USD",
        status="Pending",
    )
    assert costs.transaction_id == 123
    assert costs.description == "Service Fee"
    assert costs.type == "Fixed"
    assert costs.amount == Decimal("99.99")
    assert costs.currency == "USD"
    assert costs.status == "Pending"


def test_initializes_with_default_values():
    """Test that a Costs instance initializes with default values."""
    costs = Costs()
    assert costs.transaction_id is None
    assert costs.description is None
    assert costs.type is None
    assert costs.amount is None
    assert costs.currency is None
    assert costs.status is None


def test_adds_transaction_id():
    """Test that a transaction ID is added to a Costs instance."""
    costs = Costs().add_transaction_id(123)
    assert costs.transaction_id == 123


def test_adds_description():
    """Test that a description is added to a Costs instance."""
    costs = Costs().add_description("Service Fee")
    assert costs.description == "Service Fee"


def test_adds_type():
    """Test that a type is added to a Costs instance."""
    costs = Costs().add_type("Fixed")
    assert costs.type == "Fixed"


def test_adds_amount():
    """Test that an amount is added to a Costs instance."""
    costs = Costs().add_amount(99.99)
    assert costs.amount == Decimal("99.99")


def test_adds_currency():
    """Test that a currency is added to a Costs instance."""
    costs = Costs().add_currency("USD")
    assert costs.currency == "USD"


def test_adds_status():
    """Test that a status is added to a Costs instance."""
    costs = Costs().add_status("Pending")
    assert costs.status == "Pending"


def test_creates_from_dict_with_all_fields():
    """Test that a Costs instance is created from a dictionary with all fields."""
    data = {
        "transaction_id": 123,
        "description": "Service Fee",
        "type": "Fixed",
        "amount": 99.99,
        "currency": "USD",
        "status": "Pending",
    }
    costs = Costs.from_dict(data)
    assert costs.transaction_id == 123
    assert costs.description == "Service Fee"
    assert costs.type == "Fixed"
    assert costs.amount == Decimal("99.99")
    assert costs.currency == "USD"
    assert costs.status == "Pending"


def test_creates_from_empty_dict():
    """Test that a Costs instance is created from an empty dictionary."""
    data = {}
    costs = Costs.from_dict(data)
    assert costs.transaction_id is None
    assert costs.description is None
    assert costs.type is None
    assert costs.amount is None
    assert costs.currency is None
    assert costs.status is None


def test_creates_from_none():
    """Test that a Costs instance is created from None."""
    costs = Costs.from_dict(None)
    assert costs is None
