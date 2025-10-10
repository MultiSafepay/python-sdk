# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.order_id.capture.response.order_capture import (
    OrderCapture,
)


def test_initializes_order_capture_correctly():
    """
    Test that an OrderCapture object is correctly initialized with given data.
    """
    order_capture = OrderCapture(
        transaction_id="TX123",
        order_id="ORD123",
        payment_details=None,
    )
    assert order_capture.transaction_id == "TX123"
    assert order_capture.order_id == "ORD123"
    assert order_capture.payment_details is None


def test_initializes_order_capture_with_empty_values():
    """
    Test that an OrderCapture object is correctly initialized with default values.
    """
    order_capture = OrderCapture()
    assert order_capture.transaction_id is None
    assert order_capture.order_id is None
    assert order_capture.payment_details is None


def test_from_dict_initializes_order_capture_correctly():
    """
    Test that an OrderCapture object is correctly initialized from a dictionary.
    """
    data = {
        "transaction_id": "TX123",
        "order_id": "ORD123",
        "payment_details": None,
    }
    order_capture = OrderCapture.from_dict(data)
    assert order_capture.transaction_id == "TX123"
    assert order_capture.order_id == "ORD123"
    assert order_capture.payment_details is None


def test_from_dict_initializes_order_capture_with_empty_dict():
    """
    Test that an OrderCapture object is correctly initialized from an empty dictionary.
    """
    data = {}
    order_capture = OrderCapture.from_dict(data)
    assert order_capture.transaction_id is None
    assert order_capture.order_id is None
    assert order_capture.payment_details is None


def test_from_dict_returns_none_for_none_input():
    """
    Test that the from_dict method returns None when given None as input.
    """
    order_capture = OrderCapture.from_dict(None)
    assert order_capture is None
