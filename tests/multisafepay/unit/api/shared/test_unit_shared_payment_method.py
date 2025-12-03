# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the shared payment method model."""


from multisafepay.api.shared.payment_method import PaymentMethod


def test_initializes_with_valid_values():
    """Test that a PaymentMethod instance initializes with valid values."""
    payment_method = PaymentMethod(
        account_id="12345",
        amount=100.0,
        currency="USD",
        description="Payment for order #12345",
        external_transaction_id="txn_12345",
        payment_description="Order payment",
        status="completed",
        type="credit_card",
    )
    assert payment_method.account_id == "12345"
    assert payment_method.amount == 100.0
    assert payment_method.currency == "USD"
    assert payment_method.description == "Payment for order #12345"
    assert payment_method.external_transaction_id == "txn_12345"
    assert payment_method.payment_description == "Order payment"
    assert payment_method.status == "completed"
    assert payment_method.type == "credit_card"


def test_initializes_with_default_values():
    """Test that a PaymentMethod instance initializes with default values."""
    payment_method = PaymentMethod()
    assert payment_method.account_id is None
    assert payment_method.amount is None
    assert payment_method.currency is None
    assert payment_method.description is None
    assert payment_method.external_transaction_id is None
    assert payment_method.payment_description is None
    assert payment_method.status is None
    assert payment_method.type is None


def test_adds_account_id():
    """Test that an account ID is added to the PaymentMethod instance."""
    payment_method = PaymentMethod().add_account_id("12345")
    assert payment_method.account_id == "12345"


def test_adds_amount():
    """Test that an amount is added to the PaymentMethod instance."""
    payment_method = PaymentMethod().add_amount(100.0)
    assert payment_method.amount == 100.0


def test_adds_currency():
    """Test that a currency is added to the PaymentMethod instance."""
    payment_method = PaymentMethod().add_currency("USD")
    assert payment_method.currency == "USD"


def test_adds_description():
    """Test that a description is added to the PaymentMethod instance."""
    payment_method = PaymentMethod().add_description(
        "Payment for order #12345",
    )
    assert payment_method.description == "Payment for order #12345"


def test_adds_external_transaction_id():
    """Test that an external transaction ID is added to the PaymentMethod instance."""
    payment_method = PaymentMethod().add_external_transaction_id("txn_12345")
    assert payment_method.external_transaction_id == "txn_12345"


def test_adds_payment_description():
    """Test that a payment description is added to the PaymentMethod instance."""
    payment_method = PaymentMethod().add_payment_description("Order payment")
    assert payment_method.payment_description == "Order payment"


def test_adds_status():
    """Test that a status is added to the PaymentMethod instance."""
    payment_method = PaymentMethod().add_status("completed")
    assert payment_method.status == "completed"


def test_adds_type():
    """Test that a type is added to the PaymentMethod instance."""
    payment_method = PaymentMethod().add_type("credit_card")
    assert payment_method.type == "credit_card"


def test_creates_from_dict_with_all_fields():
    """Test that a PaymentMethod instance is created from a dictionary with all fields."""
    data = {
        "account_id": "12345",
        "amount": 100.0,
        "currency": "USD",
        "description": "Payment for order #12345",
        "external_transaction_id": "txn_12345",
        "payment_description": "Order payment",
        "status": "completed",
        "type": "credit_card",
    }
    payment_method = PaymentMethod.from_dict(data)
    assert payment_method.account_id == "12345"
    assert payment_method.amount == 100.0
    assert payment_method.currency == "USD"
    assert payment_method.description == "Payment for order #12345"
    assert payment_method.external_transaction_id == "txn_12345"
    assert payment_method.payment_description == "Order payment"
    assert payment_method.status == "completed"
    assert payment_method.type == "credit_card"


def test_creates_from_empty_dict():
    """Test that a PaymentMethod instance is created from an empty dictionary."""
    data = {}
    payment_method = PaymentMethod.from_dict(data)
    assert payment_method.account_id is None
    assert payment_method.amount is None
    assert payment_method.currency is None
    assert payment_method.description is None
    assert payment_method.external_transaction_id is None
    assert payment_method.payment_description is None
    assert payment_method.status is None
    assert payment_method.type is None


def test_creates_from_none():
    """Test that None is returned when creating a PaymentMethod instance from None."""
    payment_method = PaymentMethod.from_dict(None)
    assert payment_method is None
