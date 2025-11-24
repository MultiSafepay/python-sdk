# Copyright (c) MultiSafepay, Inc. All rights reserved.

"""Shared API models and utilities."""

import pytest
from multisafepay.exception.invalid_argument import InvalidArgumentException

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from multisafepay.api.shared.cart.cart_item import CartItem


def test_initializes_with_default_values():
    """
    Test that a CartItem initializes with default values.
    """
    item = CartItem()
    assert item.cashback is None
    assert item.currency is None
    assert item.description is None
    assert item.image is None
    assert item.merchant_item_id is None
    assert item.name is None
    assert item.options is None
    assert item.product_url is None
    assert item.quantity is None
    assert item.tax_table_selector is None
    assert item.unit_price is None
    assert item.weight is None


def test_adds_cashback():
    """
    Test that cashback can be added to a CartItem.
    """
    item = CartItem()
    item.add_cashback("10%")
    assert item.cashback == "10%"


def test_adds_currency():
    """
    Test that currency can be added to a CartItem.
    """
    item = CartItem()
    item.add_currency("USD")
    assert item.currency == "USD"


def test_adds_description():
    """
    Test that description can be added to a CartItem.
    """
    item = CartItem()
    item.add_description("A nice item")
    assert item.description == "A nice item"


def test_adds_image():
    """
    Test that image URL can be added to a CartItem.
    """
    item = CartItem()
    item.add_image("http://example.com/image.png")
    assert item.image == "http://example.com/image.png"


def test_adds_merchant_item_id():
    """
    Test that merchant item ID can be added to a CartItem.
    """
    item = CartItem()
    item.add_merchant_item_id("12345")
    assert item.merchant_item_id == "12345"


def test_adds_name():
    """
    Test that name can be added to a CartItem.
    """
    item = CartItem()
    item.add_name("Item Name")
    assert item.name == "Item Name"


def test_adds_options():
    """
    Test that options can be added to a CartItem.
    """
    item = CartItem()
    options = [{"color": "red"}, {"size": "M"}]
    item.add_options(options)
    assert item.options == options


def test_adds_product_url():
    """
    Test that product URL can be added to a CartItem.
    """
    item = CartItem()
    item.add_product_url("http://example.com/product")
    assert item.product_url == "http://example.com/product"


def test_adds_quantity():
    """
    Test that quantity can be added to a CartItem.
    """
    item = CartItem()
    item.add_quantity(10)
    assert item.quantity == 10


def test_adds_tax_table_selector():
    """
    Test that tax table selector can be added to a CartItem.
    """
    item = CartItem()
    item.add_tax_table_selector("standard")
    assert item.tax_table_selector == "standard"


def test_adds_unit_price():
    """
    Test that unit price can be added to a CartItem.
    """
    item = CartItem()
    item.add_unit_price(19.99)
    assert item.unit_price == 19.99


def test_creates_from_empty_dict():
    """
    Test that a CartItem can be created from an empty dictionary.
    """
    item = CartItem.from_dict({})
    assert item.cashback is None
    assert item.currency is None
    assert item.description is None
    assert item.image is None
    assert item.merchant_item_id is None
    assert item.name is None
    assert item.options is None
    assert item.product_url is None
    assert item.quantity is None
    assert item.tax_table_selector is None
    assert item.unit_price is None
    assert item.weight is None


def test_creates_from_none():
    """
    Test that a CartItem is None when created from None.
    """
    item = CartItem.from_dict(None)
    assert item is None


def test_add_tax_rate():
    """
    Test that a tax rate can be added to a CartItem.
    """
    item = CartItem()
    item.add_tax_rate(0.21)
    assert item.tax_table_selector == "0.21"


def test_add_tax_rate_invalid_negative():
    """
    Test that an InvalidArgumentException is raised when a negative tax rate is added to a CartItem.

    """
    item = CartItem()
    with pytest.raises(InvalidArgumentException):
        item.add_tax_rate(-0.21)


def test_add_tax_rate_no_possible_string_parse():
    """
    Test that an InvalidArgumentException is raised when a non-numeric string is passed to add_tax_rate.

    """
    item = CartItem()
    with pytest.raises(InvalidArgumentException):
        item.add_tax_rate(float("nan"))


def test_add_tax_rate_infinite():
    """
    Test that an InvalidArgumentException is raised when an infinite value is passed to add_tax_rate.

    """
    item = CartItem()
    with pytest.raises(InvalidArgumentException):
        item.add_tax_rate(float("inf"))


def test_add_tax_rate_percentage_invalid_negative():
    """
    Test that an InvalidArgumentException is raised when a negative tax rate percentage is added to a CartItem.

    """
    item = CartItem()
    with pytest.raises(InvalidArgumentException):
        item.add_tax_rate_percentage(-5.0)


def test_add_tax_rate_percentage_no_possible_string_parse():
    """
    Test that an InvalidArgumentException is raised when NaN is passed as the tax rate percentage to a CartItem.

    """
    item = CartItem()
    with pytest.raises(InvalidArgumentException):
        item.add_tax_rate_percentage(float("nan"))


def test_add_tax_rate_percentage_infinite():
    """
    Test that an InvalidArgumentException is raised when an infinite value is passed as the tax rate percentage to a CartItem.

    """
    item = CartItem()
    with pytest.raises(InvalidArgumentException):
        item.add_tax_rate_percentage(float("inf"))


def test_add_tax_rate_percentage_valid():
    """
    Test that a valid tax rate percentage is correctly set as the tax table selector in a CartItem.

    """
    item = CartItem()
    item.add_tax_rate_percentage(21)
    assert item.tax_table_selector == "0.21"


def test_add_tax_rate_percentage_zero_int():
    """
    Test that a 0 tax rate percentage is correctly set as the tax table selector in a CartItem.

    """
    item = CartItem()
    item.add_tax_rate_percentage(0)
    assert item.tax_table_selector == "0.0"


def test_add_tax_rate_percentage_zero_float():
    """
    Test that a 0.0 tax rate percentage is correctly set as the tax table selector in a CartItem.

    """
    item = CartItem()
    item.add_tax_rate_percentage(0.0)
    assert item.tax_table_selector == "0.0"
