# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for CheckoutData refund component."""

import pytest

from multisafepay.api.paths.orders.order_id.refund.request.components.checkout_data import (
    CheckoutData,
)
from multisafepay.api.shared.cart.cart_item import CartItem
from multisafepay.api.shared.cart.shopping_cart import ShoppingCart
from multisafepay.exception.invalid_argument import InvalidArgumentException


def _make_item(
    merchant_item_id: str = "item-1",
    quantity: int = 2,
    unit_price: int = 500,
) -> CartItem:
    return CartItem(
        merchant_item_id=merchant_item_id,
        name="Widget",
        quantity=quantity,
        unit_price=unit_price,
    )


def test_add_items_appends_to_list() -> None:
    """add_items appends multiple items to checkout data."""
    cd = CheckoutData(items=None)
    item1 = _make_item("a")
    item2 = _make_item("b")
    cd.add_items([item1, item2])
    assert len(cd.get_items()) == 2


def test_add_items_with_none_is_noop() -> None:
    """add_items with None leaves items unchanged."""
    cd = CheckoutData(items=None)
    cd.add_items(None)
    assert cd.get_items() is None


def test_add_item_creates_list_when_none() -> None:
    """add_item initializes list when items is None."""
    cd = CheckoutData(items=None)
    cd.add_item(_make_item())
    assert len(cd.get_items()) == 1


def test_add_item_with_none_is_noop() -> None:
    """add_item with None leaves items unchanged."""
    cd = CheckoutData(items=None)
    cd.add_item(None)
    assert cd.get_items() is None


def test_get_item_by_index() -> None:
    """get_item retrieves item by index."""
    item = _make_item()
    cd = CheckoutData(items=[item])
    assert cd.get_item(0).merchant_item_id == item.merchant_item_id


def test_get_item_returns_none_when_no_items() -> None:
    """get_item returns None when items is None."""
    cd = CheckoutData(items=None)
    assert cd.get_item(0) is None


def test_generate_from_shopping_cart() -> None:
    """generate_from_shopping_cart populates items from cart."""
    item = _make_item()
    cart = ShoppingCart(items=[item])
    cd = CheckoutData(items=None)
    cd.generate_from_shopping_cart(cart)
    assert len(cd.get_items()) == 1


def test_generate_from_shopping_cart_with_tax_selector() -> None:
    """generate_from_shopping_cart sets tax_table_selector on items."""
    item = _make_item()
    cart = ShoppingCart(items=[item])
    cd = CheckoutData(items=None)
    cd.generate_from_shopping_cart(cart, tax_table_selector="BTW21")
    assert cd.get_items()[0].tax_table_selector == "BTW21"


def test_generate_from_shopping_cart_with_none_cart() -> None:
    """generate_from_shopping_cart with None cart is noop."""
    cd = CheckoutData(items=None)
    cd.generate_from_shopping_cart(None)
    assert cd.get_items() is None


def test_refund_by_merchant_item_id() -> None:
    """refund_by_merchant_item_id creates a negative refund item."""
    item = _make_item(merchant_item_id="item-1", quantity=3, unit_price=500)
    cd = CheckoutData(items=[item])
    cd.refund_by_merchant_item_id("item-1", quantity=2)
    assert len(cd.get_items()) == 2
    refund_item = cd.get_items()[1]
    assert refund_item.unit_price == -500
    assert refund_item.quantity == 2


def test_refund_by_merchant_item_id_defaults_to_full_quantity() -> None:
    """refund_by_merchant_item_id uses full quantity when quantity=0."""
    item = _make_item(merchant_item_id="item-1", quantity=5, unit_price=100)
    cd = CheckoutData(items=[item])
    cd.refund_by_merchant_item_id("item-1", quantity=0)
    refund_item = cd.get_items()[1]
    assert refund_item.quantity == 5


def test_refund_by_merchant_item_id_raises_without_items() -> None:
    """Raise when refunding with no items."""
    cd = CheckoutData(items=None)
    with pytest.raises(InvalidArgumentException):
        cd.refund_by_merchant_item_id("item-1")


def test_get_item_by_merchant_item_id_raises_when_not_found() -> None:
    """Raise when merchant_item_id is not found."""
    item = _make_item(merchant_item_id="item-1")
    cd = CheckoutData(items=[item])
    with pytest.raises(InvalidArgumentException, match="No item found"):
        cd.get_item_by_merchant_item_id("nonexistent")


def test_get_item_by_merchant_item_id_raises_without_items() -> None:
    """Raise when items is None."""
    cd = CheckoutData(items=None)
    with pytest.raises(InvalidArgumentException, match="No items provided"):
        cd.get_item_by_merchant_item_id("item-1")
