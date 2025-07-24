# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

import pytest
from multisafepay.api.shared.checkout.tax_rate import TaxRate
from multisafepay.api.shared.checkout.tax_rule import TaxRule
from multisafepay.api.paths.orders.request.components.checkout_options import (
    CheckoutOptions,
)
from multisafepay.api.shared.checkout.checkout_options import (
    CheckoutOptions as CheckoutOptionsApiModel,
)
from multisafepay.value_object.weight import Weight
from multisafepay.api.shared.cart.cart_item import CartItem
from multisafepay.api.shared.cart.shopping_cart import ShoppingCart


def test_generate_from_shopping_cart():
    """
    Test the generate_from_shopping_cart method of CheckoutOptions.

    This test creates a ShoppingCart with multiple items, including a shipping item,

    """
    shopping_cart = ShoppingCart(
        items=[
            CartItem(
                name="Geometric Candle Holders",
                description="Geometric Candle Holders description",
                unit_price=90,
                quantity=3,
                merchant_item_id="1111",
                tax_table_selector="0.21",
                weight=Weight(value=1.0, unit="kg"),
            ),
            CartItem(
                name="Nice apple",
                description="Nice apple description",
                unit_price=35,
                quantity=1,
                merchant_item_id="666666",
                tax_table_selector="0.09",
                weight=Weight(value=20, unit="kg"),
            ),
            CartItem(
                name="Flat Rate - Fixed",
                description="Shipping",
                unit_price=10,
                quantity=1,
                merchant_item_id="msp-shipping",
                tax_table_selector="0",
                weight=Weight(value=0, unit="kg"),
            ),
        ],
    )
    generated_checkout_options = CheckoutOptions.generate_from_shopping_cart(
        shopping_cart,
    )
    # Sort both lists before comparing
    generated_checkout_options.tax_tables.alternate = sorted(
        generated_checkout_options.tax_tables.alternate,
        key=lambda x: x.name,
    )
    expected_alternate = sorted(
        [
            TaxRule(name="0.21", rules=[TaxRate(rate=0.21)]),
            TaxRule(name="0.09", rules=[TaxRate(rate=0.09)]),
            TaxRule(name="0", rules=[TaxRate(rate=0.0)]),
        ],
        key=lambda x: x.name,
    )

    test_checkout_options = CheckoutOptions(
        tax_tables=CheckoutOptionsApiModel(
            alternate=expected_alternate,
        ),
    )

    assert generated_checkout_options == test_checkout_options


def test_generate_from_shopping_cart_empty():
    """
    Test the generate_from_shopping_cart method of CheckoutOptions with an empty shopping cart.

    This test creates an empty ShoppingCart and checks if the generated CheckoutOptions is None.

    """
    shopping_cart = ShoppingCart(items=[])
    generated_checkout_options = CheckoutOptions.generate_from_shopping_cart(
        shopping_cart,
    )
    assert generated_checkout_options is None


def test_generate_from_shopping_cart_none():
    """
    Test the generate_from_shopping_cart method of CheckoutOptions with a None shopping cart.

    This test checks if an AttributeError is raised when the shopping cart is None.

    """
    shopping_cart = None
    with pytest.raises(AttributeError):
        CheckoutOptions.generate_from_shopping_cart(shopping_cart)


def test_generate_from_shopping_cart_no_items():
    """
    Test the generate_from_shopping_cart method of CheckoutOptions with a shopping cart that has no items.

    This test creates a ShoppingCart with no items and checks if the generated CheckoutOptions is None.

    """
    shopping_cart = ShoppingCart(items=None)
    generated_checkout_options = CheckoutOptions.generate_from_shopping_cart(
        shopping_cart,
    )
    assert generated_checkout_options is None


def test_generate_from_shopping_cart_with_no_tax_table_selector():
    """
    Test the generate_from_shopping_cart method of CheckoutOptions with a shopping cart that has no tax_table_selector.

    This test creates a ShoppingCart with items that have no tax_table_selector and checks if the generated CheckoutOptions is None.

    """
    shopping_cart = ShoppingCart(
        items=[
            CartItem(
                name="Geometric Candle Holders",
                description="Geometric Candle Holders description",
                unit_price=90,
                quantity=3,
                merchant_item_id="1111",
                tax_table_selector=None,
                weight=Weight(value=1.0, unit="kg"),
            ),
        ],
    )
    generated_checkout_options = CheckoutOptions.generate_from_shopping_cart(
        shopping_cart,
    )
    assert generated_checkout_options == CheckoutOptions(
        tax_tables=CheckoutOptionsApiModel(default=None, alternate=[]),
        validate_cart=None,
    )


def test_generate_from_shopping_cart_with_items_with_same_tax_table_selector():
    """
    Test the generate_from_shopping_cart method of CheckoutOptions with a shopping cart that has items with the same tax_table_selector.

    This test creates a ShoppingCart with items that all have the same tax_table_selector (0.21) and checks if the generated CheckoutOptions matches the expected output.

    """
    shopping_cart = ShoppingCart(
        items=[
            CartItem(
                name="Geometric Candle Holders",
                description="Geometric Candle Holders description",
                unit_price=90,
                quantity=3,
                merchant_item_id="1111",
                tax_table_selector=0.21,
                weight=Weight(value=1.0, unit="kg"),
            ),
            CartItem(
                name="Geometric Candle Holders",
                description="Geometric Candle Holders description",
                unit_price=90,
                quantity=3,
                merchant_item_id="1111",
                tax_table_selector=0.21,
                weight=Weight(value=1.0, unit="kg"),
            ),
        ],
    )
    generated_checkout_options = CheckoutOptions.generate_from_shopping_cart(
        shopping_cart,
    )

    test_checkout_options = CheckoutOptions(
        tax_tables=CheckoutOptionsApiModel(
            alternate=[
                TaxRule(
                    name="0.21",
                    rules=[TaxRate(rate=0.21)],
                ),
            ],
        ),
    )

    assert generated_checkout_options == test_checkout_options
