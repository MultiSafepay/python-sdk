# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the shopping cart model."""

from multisafepay.api.shared.cart.shopping_cart import ShoppingCart


def test_initializes_with_default_values():
    """
    Test that a ShoppingCart initializes with default values.
    """
    cart = ShoppingCart()
    assert cart.items is None


def test_creates_from_dict_without_items():
    """
    Test that a ShoppingCart can be created from a dictionary without items.
    """
    data = {}
    cart = ShoppingCart.from_dict(data)
    assert cart.items is None


def test_creates_from_none():
    """
    Test that a ShoppingCart is None when created from None.
    """
    cart = ShoppingCart.from_dict(None)
    assert cart is None
