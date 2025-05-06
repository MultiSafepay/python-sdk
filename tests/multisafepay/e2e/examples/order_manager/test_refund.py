# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import os
import time
import pytest
from dotenv import load_dotenv
from multisafepay.api.paths.orders.order_manager import OrderManager
from multisafepay.api.paths.orders.request.components.payment_options import (
    PaymentOptions,
)
from multisafepay.api.paths.orders.request.components.plugin import Plugin
from multisafepay.api.paths.orders.request.order_request import OrderRequest
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
from multisafepay.api.paths.orders.order_id.refund.request.refund_request import (
    RefundOrderRequest,
)


@pytest.fixture(scope="module")
def order_manager() -> OrderManager:
    load_dotenv()
    api_key = os.getenv("API_KEY")
    multisafepay_sdk = Sdk(api_key, False)
    return multisafepay_sdk.get_order_manager()


def test_refund(order_manager: OrderManager):
    """
    Test the refund method of the OrderManager.

    This test checks if the order is refunded successfully and if the response is of the correct type.

    """
    # Values related to the order
    order_id = f"{time.time()!s}"
    amount = Amount(amount=1000)
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

    # Create a shopping cart object
    payment_options = (
        PaymentOptions()
        .add_notification_url("https://multisafepay.com/notification_url")
        .add_redirect_url("https://multisafepay.com/redirect_url")
        .add_cancel_url("https://multisafepay.com/cancel_url")
        .add_close_window(True)
    )

    # Create a cart item object
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

    # Request a refund for the created order
    refund_request = (
        RefundOrderRequest()
        .add_amount(Amount(amount=100))
        .add_currency(Currency(currency="EUR"))
        .add_description(
            Description(description=f"Refund for order #{order_id}"),
        )
    )

    refund_response = order_manager.refund(order_id, refund_request)
    assert isinstance(refund_response, CustomApiResponse)
    refund_data = refund_response.get_data()
    assert refund_data.refund_id is not None
    assert refund_data.transaction_id is not None
