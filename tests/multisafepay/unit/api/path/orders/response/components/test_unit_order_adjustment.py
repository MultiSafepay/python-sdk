# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.paths.orders.response.components.order_adjustment import (
    OrderAdjustment,
)


def test_initializes_order_adjustment_correctly():
    """
    Tests that the OrderAdjustment object is initialized correctly with the given values.
    """
    order_adjustment = OrderAdjustment(total_adjustment=10.0, total_tax=2.0)

    assert order_adjustment.total_adjustment == 10.0
    assert order_adjustment.total_tax == 2.0


def test_initializes_order_adjustment_with_empty_values():
    """
    Tests that the OrderAdjustment object is initialized with None values when no arguments are provided.
    """
    order_adjustment = OrderAdjustment()

    assert order_adjustment.total_adjustment is None
    assert order_adjustment.total_tax is None


def test_from_dict_creates_instance_with_correct_values():
    """
    Test that the from_dict method creates an OrderAdjustment instance with the correct values.
    """
    data = {"total_adjustment": 10.0, "total_tax": 2.0}
    order_adjustment = OrderAdjustment.from_dict(data)

    assert order_adjustment.total_adjustment == 10.0
    assert order_adjustment.total_tax == 2.0


def test_from_dict_creates_instance_with_none_values():
    """
    Test that the from_dict method creates an OrderAdjustment instance with None values when no arguments are provided.
    """
    data = {}
    order_adjustment = OrderAdjustment.from_dict(data)

    assert order_adjustment.total_adjustment is None
    assert order_adjustment.total_tax is None


def test_from_dict_returns_none_for_none_input():
    """
    Test that the from_dict method returns None when no arguments are provided.
    """
    order_adjustment = OrderAdjustment.from_dict(None)

    assert order_adjustment is None
