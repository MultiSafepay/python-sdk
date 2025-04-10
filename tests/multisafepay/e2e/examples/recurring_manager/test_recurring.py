# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import os
import time

import pytest
from dotenv import load_dotenv
from multisafepay.api.paths.orders.request.components.payment_options import (
    PaymentOptions,
)
from multisafepay.api.paths.orders.request.components.plugin import Plugin

from multisafepay.api.paths.orders.request.order_request import OrderRequest
from multisafepay.api.shared.customer import Customer
from multisafepay.sdk import Sdk
from multisafepay.value_object.amount import Amount
from multisafepay.value_object.currency import Currency
from multisafepay.api.shared.description import Description
from multisafepay.value_object.ip_address import IpAddress
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.orders.response.order_response import Order
from multisafepay.api.paths.recurring.customer_reference.token.token import (
    Token,
)


@pytest.fixture(scope="module")
def sdk() -> Sdk:
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return Sdk(api_key, False)


def test_recurring(sdk):
    """
    Test the recurring manager.

    This test checks if the recurring manager can create, retrieve, and delete a token successfully.

    """
    # Values related to the order

    reference = "shopper-456"
    order_id = f"{time.time()!s}"
    amount = Amount(amount=1000)
    currency = Currency(currency="EUR")
    description = Description(description="Order description")
    ip_address = IpAddress(ip_address="192.0.0.1")

    # Create a customer object
    customer = (
        Customer()
        .add_locale("nl_NL")
        .add_ip_address(ip_address)
        .add_first_name("John")
        .add_last_name("Smith")
        .add_address1("Neherkade")
        .add_address2("Ken")
        .add_user_agent("Mozilla/5.0")
        .add_reference(reference)
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
    )

    # Create an order request object
    order_request = (
        OrderRequest()
        .add_type("direct")
        .add_order_id(order_id)
        .add_description(description)
        .add_amount(amount)
        .add_currency(currency)
        .add_gateway("CREDITCARD")
        .add_customer(customer)
        .add_delivery(customer)
        .add_plugin(plugin)
        .add_payment_options(payment_options)
        .add_gateway_info(
            {
                "card_number": "4111111111111111",
                "card_holder_name": "Test Holder Name",
                "card_expiry_date": "2612",
                "card_cvc": "123",
            },
        )
        .add_recurring_model("cardOnFile")
    )

    order_manager = sdk.get_order_manager()
    create_response = order_manager.create(order_request)
    assert isinstance(create_response, CustomApiResponse)
    order = create_response.get_data()

    assert isinstance(order, Order)

    recurring_manager = sdk.get_recurring_manager()
    response = recurring_manager.get_list(reference)

    assert isinstance(response, CustomApiResponse)
    token_list = response.get_data()

    assert isinstance(token_list, list)
    assert len(token_list) > 0

    index = next(
        (
            i
            for i, token in enumerate(token_list)
            if token.token == order.payment_details.recurring_id
        ),
        -1,
    )

    assert index is not -1
    assert isinstance(token_list[index], Token)
    token = token_list[index]

    response = recurring_manager.get(token.token, reference)

    assert isinstance(response, CustomApiResponse)
    token_response = response.get_data()

    assert isinstance(token_response, Token)
    assert token_response.token == token.token

    # Delete the token
    delete_response = recurring_manager.delete(reference, token.token)

    assert isinstance(delete_response, CustomApiResponse)
    delete_data_response = delete_response.get_body_data()
    assert isinstance(delete_data_response, dict)
    assert delete_data_response.get("removed") == True
