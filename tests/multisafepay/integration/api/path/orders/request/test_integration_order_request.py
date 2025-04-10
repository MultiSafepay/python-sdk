# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

import pytest

from multisafepay.api.paths.orders.request.components.payment_options import (
    PaymentOptions,
)
from multisafepay.api.paths.orders.request.components.plugin import (
    Plugin,
)
from multisafepay.api.paths.orders.request.order_request import OrderRequest
from multisafepay.api.shared.cart.cart_item import CartItem
from multisafepay.api.shared.cart.shopping_cart import ShoppingCart
from multisafepay.api.shared.checkout.checkout_options import CheckoutOptions

from multisafepay.api.paths.orders.request.components.checkout_options import (
    CheckoutOptions as CheckoutOptionsRequest,
)
from multisafepay.api.shared.checkout.default_tax_rate import DefaultTaxRate
from multisafepay.api.shared.checkout.tax_rate import TaxRate
from multisafepay.api.shared.checkout.tax_rule import TaxRule

from multisafepay.api.shared.customer import Customer
from multisafepay.api.shared.description import Description
from multisafepay.exception.invalid_total_amount import (
    InvalidTotalAmountException,
)
from multisafepay.value_object.amount import Amount
from multisafepay.value_object.country import Country
from multisafepay.value_object.currency import Currency
from multisafepay.value_object.email_address import EmailAddress
from multisafepay.value_object.ip_address import IpAddress
from multisafepay.value_object.phone_number import PhoneNumber
from multisafepay.value_object.weight import Weight


def test_initializes_order_request_correctly():
    """
    Tests that the OrderRequest object is initialized correctly with the given values.

    This test verifies that the OrderRequest object is correctly initialized with the given values.

    """
    amount = Amount(amount=10000)
    currency = Currency(currency="EUR")
    country_tmp = Country(code="NL")
    description = Description(description="Order description")
    email = EmailAddress(email_address="example@multisafepay.com")
    phone_number = PhoneNumber(phone_number="0208500500")
    ip_address = IpAddress(ip_address="192.0.0.1")
    customer = (
        Customer()
        .add_first_name("John")
        .add_last_name("Doe")
        .add_address1("Kraanspoor")
        .add_address2("39")
        .add_zip_code("1033SC")
        .add_city("Amsterdam")
        .add_country(country_tmp)
        .add_email(email)
        .add_house_number("39")
        .add_locale("en_US")
        .add_phone(phone_number)
        .add_ip_address(ip_address)
        .add_forwarded_ip(ip_address)
        .add_referrer("https://www.example.com")
        .add_user_agent("Mozilla/5.0")
    )

    # Create a PluginDetails object and add the plugin details
    plugin = (
        Plugin()
        .add_plugin_version("example python-sdk")
        .add_shop("example-SDK Test")
        .add_shop_version("1.0.0")
        .add_partner("Me")
        .add_shop_root_url("http://example.com")
    )

    payment_options = (
        PaymentOptions()
        .add_notification_url("https://multisafepay.com/notification_url")
        .add_redirect_url("https://multisafepay.com/redirect_url")
        .add_cancel_url("https://multisafepay.com/cancel_url")
        .add_close_window(True)
    )

    order_request = (
        OrderRequest()
        .add_type("redirect")
        .add_order_id("order")
        .add_description(description)
        .add_amount(amount)
        .add_currency(currency)
        .add_gateway("IDEAL")
        .add_customer(customer)
        .add_delivery(customer)
        .add_plugin(plugin)
        .add_payment_options(payment_options)
    )

    assert order_request.type == "redirect"
    assert order_request.order_id == "order"
    assert order_request.description == description.description
    assert order_request.amount == amount.amount
    assert order_request.currency == currency.currency
    assert order_request.gateway == "IDEAL"
    assert order_request.customer == customer
    assert order_request.delivery == customer
    assert order_request.plugin == plugin
    assert order_request.payment_options == payment_options


def test_initializes_order_request_validate_amount_valid():
    """
    Tests that the OrderRequest object is initialized correctly with the given values.

    This test verifies that the OrderRequest object is correctly initialized with the given values.

    """
    amount = Amount(amount=37485)
    currency = Currency(currency="EUR")

    order_request = (
        OrderRequest()
        .add_type("redirect")
        .add_order_id("order")
        .add_amount(amount)
        .add_currency(currency)
        .add_gateway("IDEAL")
        .add_shopping_cart(
            shopping_cart=ShoppingCart(
                items=[
                    CartItem(
                        name="Geometric Candle Holders",
                        description="Geometric Candle Holders description",
                        unit_price=90,
                        quantity=3,
                        merchant_item_id="1111",
                        tax_table_selector="BTW21",
                        weight=Weight(value=1.0, unit="kg"),
                    ),
                    CartItem(
                        name="Nice apple",
                        description="Nice apple description",
                        unit_price=35,
                        quantity=1,
                        merchant_item_id="666666",
                        tax_table_selector="BTW9",
                        weight=Weight(value=20, unit="kg"),
                    ),
                    CartItem(
                        name="Flat Rate - Fixed",
                        description="Shipping",
                        unit_price=10,
                        quantity=1,
                        merchant_item_id="msp-shipping",
                        tax_table_selector="none",
                        weight=Weight(value=0, unit="kg"),
                    ),
                ],
            ),
        )
        .add_checkout_options(
            CheckoutOptionsRequest(
                tax_tables=CheckoutOptions(
                    default=DefaultTaxRate(rate=0.21, shipping_taxed=True),
                    alternate=[
                        TaxRule(
                            name="BTW21",
                            standalone=True,
                            rules=[TaxRate(rate=0.21)],
                        ),
                        TaxRule(
                            name="BTW9",
                            standalone=True,
                            rules=[TaxRate(rate=0.09)],
                        ),
                        TaxRule(
                            name="BTW6",
                            standalone=True,
                            rules=[TaxRate(rate=0.06)],
                        ),
                        TaxRule(
                            name="BTW0",
                            standalone=True,
                            rules=[TaxRate(rate=0)],
                        ),
                        TaxRule(
                            name="none",
                            standalone=False,
                            rules=[TaxRate(rate=0)],
                        ),
                        TaxRule(
                            name="FEE",
                            standalone=False,
                            rules=[TaxRate(rate=0)],
                        ),
                    ],
                ),
            ),
        )
        .validate_amount()
    )
    assert isinstance(order_request, OrderRequest)
    assert order_request.amount > 0
    assert isinstance(order_request.shopping_cart, ShoppingCart)
    assert isinstance(order_request.checkout_options, CheckoutOptionsRequest)


def test_initializes_order_request_validate_amount_invalid():
    """
    Tests that the OrderRequest object is initialized correctly with the given values.

    This test verifies that the OrderRequest object is correctly initialized with the given values.

    """
    amount = Amount(amount=10000)
    currency = Currency(currency="EUR")

    with pytest.raises(InvalidTotalAmountException):
        (
            OrderRequest()
            .add_type("redirect")
            .add_order_id("order")
            .add_amount(amount)
            .add_currency(currency)
            .add_gateway("IDEAL")
            .add_shopping_cart(
                shopping_cart=ShoppingCart(
                    items=[
                        CartItem(
                            name="Geometric Candle Holders",
                            description="Geometric Candle Holders description",
                            unit_price=90,
                            quantity=3,
                            merchant_item_id="1111",
                            tax_table_selector="BTW21",
                            weight=Weight(value=1.0, unit="kg"),
                        ),
                        CartItem(
                            name="Nice apple",
                            description="Nice apple description",
                            unit_price=35,
                            quantity=1,
                            merchant_item_id="666666",
                            tax_table_selector="BTW9",
                            weight=Weight(value=20, unit="kg"),
                        ),
                        CartItem(
                            name="Flat Rate - Fixed",
                            description="Shipping",
                            unit_price=10,
                            quantity=1,
                            merchant_item_id="msp-shipping",
                            tax_table_selector="none",
                            weight=Weight(value=0, unit="kg"),
                        ),
                    ],
                ),
            )
            .add_checkout_options(
                CheckoutOptionsRequest(
                    tax_tables=CheckoutOptions(
                        default=DefaultTaxRate(rate=0.21, shipping_taxed=True),
                        alternate=[
                            TaxRule(
                                name="BTW21",
                                standalone=True,
                                rules=[TaxRate(rate=0.21)],
                            ),
                            TaxRule(
                                name="BTW9",
                                standalone=True,
                                rules=[TaxRate(rate=0.09)],
                            ),
                            TaxRule(
                                name="BTW6",
                                standalone=True,
                                rules=[TaxRate(rate=0.06)],
                            ),
                            TaxRule(
                                name="BTW0",
                                standalone=True,
                                rules=[TaxRate(rate=0)],
                            ),
                            TaxRule(
                                name="none",
                                standalone=False,
                                rules=[TaxRate(rate=0)],
                            ),
                            TaxRule(
                                name="FEE",
                                standalone=False,
                                rules=[TaxRate(rate=0)],
                            ),
                        ],
                    ),
                ),
            )
            .validate_amount()
        )
