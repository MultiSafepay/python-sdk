# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.order_id.refund.request.refund_request import (
    RefundOrderRequest,
)


def test_initializes_refund_order_request_correctly():
    """Test that a RefundOrderRequest object is correctly initialized with given data."""
    request = RefundOrderRequest()
    request.add_currency("USD")
    request.add_amount(1000)
    request.add_description("Refund for order")

    assert request.currency == "USD"
    assert request.amount == 1000
    assert request.description == "Refund for order"


def test_initializes_refund_order_request_with_default_values():
    """Test that a RefundOrderRequest object is correctly initialized with default values."""
    request = RefundOrderRequest()

    assert request.currency is None
    assert request.amount is None
    assert request.description is None
    assert request.checkout_data is None


def add_currency_updates_value():
    """Test that the add_currency method updates the currency attribute to the given value."""
    request = RefundOrderRequest()
    request_updated = request.add_currency("EUR")

    assert request.currency == "EUR"
    assert isinstance(request_updated.currency, RefundOrderRequest)


def add_amount_updates_value():
    """Test that the add_amount method updates the amount attribute to the given value."""
    request = RefundOrderRequest()
    request_updated = request.add_amount(500)

    assert request.amount == 500
    assert isinstance(request_updated.currency, RefundOrderRequest)


def add_description_updates_value():
    """Test that the add_description method updates the description attribute to the given value."""
    request = RefundOrderRequest()
    request_updated = request.add_description("Partial refund")

    assert request.description == "Partial refund"
    assert isinstance(request_updated.currency, RefundOrderRequest)
