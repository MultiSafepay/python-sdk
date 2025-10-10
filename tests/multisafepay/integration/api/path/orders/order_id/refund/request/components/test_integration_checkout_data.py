# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for integration testing."""

from multisafepay.api.paths.orders.order_id.refund.request.components.checkout_data import (
    CheckoutData,
)
from multisafepay.api.shared.cart.cart_item import CartItem
from multisafepay.api.shared.cart.shopping_cart import ShoppingCart
from multisafepay.exception.invalid_argument import InvalidArgumentException


def test_initializes_checkout_data_correctly():
    """
    Test that a CheckoutData object is correctly initialized with given data.

    This test verifies that the tax table and items are correctly added to the CheckoutData object.

    """
    checkout_data = CheckoutData()
    checkout_data.add_items([CartItem(), CartItem()])

    assert len(checkout_data.items) == 2
    assert all(isinstance(item, CartItem) for item in checkout_data.items)


def test_initializes_checkout_data_with_default_values():
    """
    Test that a CheckoutData object is correctly initialized with default values.

    This test verifies that the items and tax table are set to None when no data is provided.

    """
    checkout_data = CheckoutData()

    assert checkout_data.items is None


def test_add_single_item_to_checkout_data():
    """
    Test that a single item is correctly added to the CheckoutData object.

    This test verifies that the item is correctly added to the list of items in the CheckoutData object.

    """
    checkout_data = CheckoutData()
    item = CartItem()
    checkout_data.add_item(item)

    assert len(checkout_data.items) == 1
    assert checkout_data.items[0] == item


def test_get_items_returns_all_items():
    """
    Test that all items are correctly returned from the CheckoutData object.

    This test verifies that the list of items is correctly returned from the CheckoutData object.

    """
    checkout_data = CheckoutData()
    items = [CartItem(), CartItem()]
    checkout_data.add_items(items)

    assert checkout_data.get_items() == items


def test_get_item_by_index():
    """
    Test that an item is correctly retrieved by its index from the CheckoutData object.

    This test verifies that the item is correctly retrieved by its index from the list of items in the
    CheckoutData object.

    """
    checkout_data = CheckoutData()
    item = CartItem()
    checkout_data.add_item(item)

    assert checkout_data.get_item(0) == item


def test_generate_from_shopping_cart():
    """
    Test that checkout data is correctly generated from a shopping cart.

    This test verifies that the items in the shopping cart are correctly added to the CheckoutData object.

    """
    shopping_cart = ShoppingCart()
    shopping_cart.add_item(CartItem())
    checkout_data = CheckoutData()
    checkout_data.generate_from_shopping_cart(shopping_cart)

    assert len(checkout_data.items) == 1
    assert isinstance(checkout_data.items[0], CartItem)


def refund_by_merchant_item_id_raises_exception_if_no_items():
    """
    Test that an exception is raised if no items are provided in the checkout data when processing a refund by
    merchant item ID.

    This test verifies that an InvalidArgumentException is raised if no items are provided in the checkout data.

    """
    checkout_data = CheckoutData()

    try:
        checkout_data.refund_by_merchant_item_id("item_id")
    except InvalidArgumentException as e:
        assert str(e) == "No items provided in checkout data"


def refund_by_merchant_item_id_raises_exception_if_item_not_found():
    """
    Test that an exception is raised if the item is not found when processing a refund by merchant item ID.

    This test verifies that an InvalidArgumentException is raised if the item is not found in the list of items.

    """
    checkout_data = CheckoutData()
    checkout_data.add_item(CartItem(merchant_item_id="different_id"))

    try:
        checkout_data.refund_by_merchant_item_id("item_id")
    except InvalidArgumentException as e:
        assert str(e) == 'No item found with merchant_item_id "item_id"'


def refund_by_merchant_item_id_processes_refund_correctly():
    """
    Test that a refund is correctly processed by merchant item ID.

    This test verifies that the refund is correctly processed by merchant item ID and that the item is correctly updated.

    """
    item = CartItem(merchant_item_id="item_id", quantity=5, unit_price=100)
    checkout_data = CheckoutData()
    checkout_data.add_item(item)
    checkout_data.refund_by_merchant_item_id("item_id", quantity=2)

    assert len(checkout_data.items) == 2
    assert checkout_data.items[1].quantity == 2
    assert checkout_data.items[1].unit_price == -100
