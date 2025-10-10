# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Shared API models and utilities."""

from multisafepay.api.shared.cart.shopping_cart import ShoppingCart
from multisafepay.api.shared.cart.cart_item import CartItem


def test_initializas_with_valid_values():
    """
    Test that a ShoppingCart initializes with valid values.

    This test verifies that the items attribute is correctly initialized with the given items.

    """
    cart = ShoppingCart(
        items=[CartItem(name="Item 1"), CartItem(name="Item 2")],
    )
    assert len(cart.items) == 2
    assert cart.items[0].name == "Item 1"
    assert cart.items[1].name == "Item 2"


def test_adds_single_item_to_empty_cart():
    """
    Test that a single item can be added to an empty ShoppingCart.

    This test verifies that the item is correctly added to the list of items in the ShoppingCart.

    """
    cart = ShoppingCart()
    item = CartItem(name="Item 1")
    cart.add_item(item)
    assert len(cart.items) == 1
    assert cart.items[0].name == "Item 1"


def test_adds_multiple_items_to_empty_cart():
    """
    Test that multiple items can be added to an empty ShoppingCart.

    This test verifies that the items are correctly added to the list of items in the ShoppingCart.

    """
    cart = ShoppingCart()
    items = [CartItem(name="Item 1"), CartItem(name="Item 2")]
    cart.add_items(items)
    assert len(cart.items) == 2
    assert cart.items[0].name == "Item 1"
    assert cart.items[1].name == "Item 2"


def test_adds_single_item_to_non_empty_cart():
    """
    Test that a single item can be added to a non-empty ShoppingCart.

    This test verifies that the item is correctly added to the list of items in the ShoppingCart.

    """
    cart = ShoppingCart(items=[CartItem(name="Item 1")])
    item = CartItem(name="Item 2")
    cart.add_item(item)
    assert len(cart.items) == 2
    assert cart.items[1].name == "Item 2"


def test_creates_from_dict_with_items():
    """
    Test that a ShoppingCart can be created from a dictionary with items.

    This test verifies that a ShoppingCart can be created from a dictionary and that the items attribute is correctly set.

    """
    data = {"items": [{"name": "Item 1"}, {"name": "Item 2"}]}
    cart = ShoppingCart.from_dict(data)
    assert len(cart.items) == 2
    assert cart.items[0].name == "Item 1"
    assert cart.items[1].name == "Item 2"
