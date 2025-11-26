# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for e2e testing."""

import os
import time
import pytest
from dotenv import load_dotenv
from multisafepay.api.paths.orders.order_manager import OrderManager
from multisafepay.value_object.weight import Weight
from multisafepay.api.shared.cart.cart_item import CartItem
from multisafepay.api.paths.orders.request.components.checkout_options import (
    CheckoutOptions,
)
from multisafepay.api.paths.orders.request.components.payment_options import (
    PaymentOptions,
)
from multisafepay.api.paths.orders.request.components.plugin import Plugin
from multisafepay.api.paths.orders.request.order_request import OrderRequest
from multisafepay.api.shared.cart.shopping_cart import ShoppingCart
from multisafepay.api.shared.customer import Customer
from multisafepay.sdk import Sdk
from multisafepay.value_object.amount import Amount
from multisafepay.value_object.country import Country
from multisafepay.value_object.currency import Currency
from multisafepay.api.shared.description import Description
from multisafepay.value_object.email_address import EmailAddress
from multisafepay.value_object.ip_address import IpAddress
from multisafepay.value_object.phone_number import PhoneNumber
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.orders.response.order_response import Order


@pytest.fixture(scope="module")
def order_manager() -> OrderManager:
    """Fixture that provides an OrderManager instance for testing."""
    load_dotenv()
    api_key = os.getenv("API_KEY")
    multisafepay_sdk = Sdk(api_key, False)
    return multisafepay_sdk.get_order_manager()


def test_refund_by_shopping_cart(order_manager: OrderManager):
    """
    Test the create_refund_request method of the OrderManager.

    This test checks if the order is refunded successfully and if the response is of the correct type.

    """
    # Values related to the order
    order_id = f"{time.time()!s}"
    amount = Amount(amount=37485)
    currency = Currency(currency="EUR")
    country = Country(code="NL")
    description = Description(description="Order description")
    email = EmailAddress(email_address="example@multisafepay.com")
    phone_number = PhoneNumber(phone_number="0208500500")
    ip_address = IpAddress(ip_address="46.6.18.113")

    # Create a customer object
    customer = (
        Customer()
        .add_first_name("John")
        .add_last_name("Doe")
        .add_address1("Neherkade")
        .add_address2("39")
        .add_house_number("XI")
        .add_zip_code("2521VA")
        .add_city("Gravenhage")
        .add_country(country)
        .add_email(email)
        .add_locale("nl_NL")
        .add_phone(phone_number)
        .add_ip_address(ip_address)
        .add_forwarded_ip(ip_address)
        .add_referrer("https://www.example.com")
        .add_user_agent("Mozilla/5.0")
    )

    # Create a plugin object
    plugin = (
        Plugin()
        .add_plugin_version("1.0.0")
        .add_shop("CMS - Framework name")
        .add_shop_version("1.0.0")
        .add_partner("MultiSafepay")
        .add_shop_root_url("https://www.multisafepay.com")
    )

    # Create a payment options object
    payment_options = (
        PaymentOptions()
        .add_notification_url("https://multisafepay.com/notification_url")
        .add_redirect_url("https://multisafepay.com/redirect_url")
        .add_cancel_url("https://multisafepay.com/cancel_url")
        .add_close_window(True)
    )

    # Create a cart item object
    cart_items = [
        CartItem()
        .add_name("Geometric Candle Holders")
        .add_description("Geometric Candle Holders description")
        .add_unit_price(90)
        .add_quantity(3)
        .add_merchant_item_id("1111")
        .add_tax_rate_percentage(21)
        .add_weight(Weight(value=1.0, unit="kg")),
        CartItem()
        .add_name("Nice apple")
        .add_description("Nice apple description")
        .add_unit_price(35)
        .add_quantity(1)
        .add_merchant_item_id("666666")
        .add_tax_rate_percentage(9)
        .add_weight(Weight(value=20, unit="kg")),
        CartItem()
        .add_name("Flat Rate - Fixed")
        .add_description("Shipping")
        .add_unit_price(10)
        .add_quantity(1)
        .add_merchant_item_id("msp-shipping")
        .add_tax_rate_percentage(0)
        .add_weight(Weight(value=0, unit="kg")),
    ]

    # Create a shopping cart object
    shopping_cart = ShoppingCart().add_items(cart_items)

    # Create an order request object
    order_request = (
        OrderRequest()
        .add_type("direct")
        .add_order_id(order_id)
        .add_description(description)
        .add_amount(amount)
        .add_currency(currency)
        .add_gateway("VISA")
        .add_customer(customer)
        .add_plugin(plugin)
        .add_payment_options(payment_options)
        .add_shopping_cart(shopping_cart)
        .add_checkout_options(
            CheckoutOptions.generate_from_shopping_cart(shopping_cart),
        )
        .add_gateway_info(
            {
                "card_number": "4111111111111111",
                "card_holder_name": "Test Holder Name",
                "card_expiry_date": "3012",
                "card_cvc": "123",
            },
        )
    )

    create_response = order_manager.create(order_request)
    assert isinstance(create_response, CustomApiResponse)
    order = create_response.get_data()
    assert isinstance(order, Order)

    # Create a refund request based on the shopping cart for the created order
    refund_request = order_manager.create_refund_request(order)

    # Request a refund for the created order
    refund_response = order_manager.refund(order_id, refund_request)

    assert isinstance(refund_response, CustomApiResponse)
    refund_data = refund_response.get_data()
    assert refund_data.refund_id is not None
    assert refund_data.transaction_id is not None
