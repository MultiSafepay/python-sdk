# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Shared API models and utilities."""

from multisafepay.api.shared.cart.cart_item import CartItem
from multisafepay.value_object.weight import Weight


def test_initializes_with_valid_values():
    """
    Test that a CartItem initializes with valid values.

    This test verifies that the CartItem initializes with the correct values.

    """
    item = CartItem(
        cashback="10%",
        currency="USD",
        description="A nice item",
        image="http://example.com/image.png",
        merchant_item_id="12345",
        name="Item Name",
        options=[{"color": "red"}, {"size": "M"}],
        product_url="http://example.com/product",
        quantity=10,
        tax_table_selector="standard",
        tax_rate=0.2,
        unit_price=19.99,
        weight=Weight(
            value=100,
            unit="grams",
        ),
    )
    assert item.cashback == "10%"
    assert item.currency == "USD"
    assert item.description == "A nice item"
    assert item.image == "http://example.com/image.png"
    assert item.merchant_item_id == "12345"
    assert item.name == "Item Name"
    assert item.options == [{"color": "red"}, {"size": "M"}]
    assert item.product_url == "http://example.com/product"
    assert item.quantity == 10
    assert item.tax_table_selector == "standard"
    assert item.tax_rate == 0.2
    assert item.unit_price == 19.99
    assert item.weight.value == 100
    assert item.weight.unit == "grams"


def test_adds_weight():
    """
    Test that weight can be added to a CartItem.

    This test verifies that a weight can be added to a CartItem.

    """
    item = CartItem()
    item.add_weight(Weight(value=100, unit="grams"))
    assert item.weight.value == 100
    assert item.weight.unit == "grams"


def test_clones_cart_item():
    """
    Test that a CartItem can be cloned.

    This test verifies that a CartItem can be cloned and that the clone is equal to the original item.

    """
    item = CartItem()
    item.add_name("Item Name")
    clone = item.clone()
    assert clone.name == "Item Name"
    assert item == clone


def test_creates_from_dict():
    """
    Test that a CartItem can be created from a dictionary.

    This test verifies that a CartItem can be created from a dictionary and that the attributes are set correctly.

    """
    data = {
        "cashback": "10%",
        "currency": "USD",
        "description": "A nice item",
        "image": "http://example.com/image.png",
        "merchant_item_id": "12345",
        "name": "Item Name",
        "options": [{"color": "red"}, {"size": "M"}],
        "product_url": "http://example.com/product",
        "quantity": 10,
        "tax_table_selector": "standard",
        "tax_rate": 0.2,
        "unit_price": 19.99,
        "weight": {"value": 100.0, "unit": "grams"},
    }
    item = CartItem.from_dict(data)
    assert item.cashback == "10%"
    assert item.currency == "USD"
    assert item.description == "A nice item"
    assert item.image == "http://example.com/image.png"
    assert item.merchant_item_id == "12345"
    assert item.name == "Item Name"
    assert item.options == [{"color": "red"}, {"size": "M"}]
    assert item.product_url == "http://example.com/product"
    assert item.quantity == 10
    assert item.tax_table_selector == "standard"
    assert item.tax_rate == 0.2
    assert item.unit_price == 19.99
    assert item.weight.unit == "grams"
    assert item.weight.value == 100.0
