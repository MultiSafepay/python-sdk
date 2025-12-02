# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.order_id.refund.response.order_refund import (
    OrderRefund,
)


def test_initializes_order_refund_correctly():
    """Test that an OrderRefund object is correctly initialized with given values."""
    order_refund = OrderRefund(
        transaction_id="12345",
        refund_id="54321",
        payment_details=None,
    )

    assert order_refund.transaction_id == "12345"
    assert order_refund.refund_id == "54321"
    assert order_refund.payment_details is None


def test_initializes_order_refund_with_empty_values():
    """Test that an OrderRefund object is correctly initialized with empty values."""
    order_refund = OrderRefund()

    assert order_refund.transaction_id is None
    assert order_refund.refund_id is None
    assert order_refund.payment_details is None


def test_from_dict_initializes_order_refund_correctly():
    """Test that an OrderRefund object is correctly initialized from a dictionary with given values."""
    data = {
        "transaction_id": "12345",
        "refund_id": "54321",
        "payment_details": None,
    }
    order_refund = OrderRefund.from_dict(data)

    assert order_refund.transaction_id == "12345"
    assert order_refund.refund_id == "54321"
    assert order_refund.payment_details is None


def test_from_dict_initializes_order_refund_with_empty_dict():
    """Test that an OrderRefund object is correctly initialized from an empty dictionary."""
    data = {}
    order_refund = OrderRefund.from_dict(data)

    assert order_refund.transaction_id is None
    assert order_refund.refund_id is None
    assert order_refund.payment_details is None


def test_from_dict_returns_none_if_input_is_none():
    """Test that the from_dict method returns None if the input is None."""
    order_refund = OrderRefund.from_dict(None)

    assert order_refund is None
