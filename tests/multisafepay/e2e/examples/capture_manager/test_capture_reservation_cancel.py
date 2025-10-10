# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for e2e testing."""

import os
import time
import pytest
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from multisafepay.api.paths.capture.response.capture import CancelReservation
from multisafepay.api.paths.capture.request.capture_request import (
    CaptureRequest,
)

from multisafepay.api.paths.orders.order_id.capture.request.capture_request import (
    CaptureOrderRequest,
)
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

if TYPE_CHECKING:
    from multisafepay.api.paths.capture.capture_manager import CaptureManager
    from multisafepay.api.paths.orders.order_id.capture.response.order_capture import (
        OrderCapture,
    )


@pytest.fixture(scope="module")
def sdk() -> Sdk:
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return Sdk(api_key, False)


def test_capture_reservation_cancel(sdk: Sdk):
    """
    Test the capture reservation cancel method of the CaptureManager.

    This test checks if the capture reservation cancel is successful and if the response is of the correct type.

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

    # Create an order request object
    order_request = (
        OrderRequest()
        .add_capture("manual")
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

    order_manager = sdk.get_order_manager()

    create_response = order_manager.create(order_request)
    assert isinstance(create_response, CustomApiResponse)
    order = create_response.get_data()
    assert isinstance(order, Order)

    capture_id: str = "capture_" + order_id

    # Create a capture order request object
    capture_order_request = (
        CaptureOrderRequest()
        .add_amount(10)
        .add_reason("Order captured")
        .add_new_order_id(capture_id)
        .add_new_order_status("completed")
    )

    capture_response = order_manager.capture(order_id, capture_order_request)
    assert isinstance(capture_response, CustomApiResponse)
    order_capture: OrderCapture = capture_response.get_data()
    assert order_capture is not None
    assert order_capture.order_id == capture_id

    capture_request = (
        CaptureRequest().add_status("cancelled").add_reason("<reason>")
    )

    capture_manager: CaptureManager = sdk.get_capture_manager()

    capture_reservation_cancel_response: CustomApiResponse = (
        capture_manager.capture_reservation_cancel(order_id, capture_request)
    )

    assert isinstance(capture_reservation_cancel_response, CustomApiResponse)
    assert capture_reservation_cancel_response.get_status_code() == 200
    assert capture_reservation_cancel_response.get_body_success() == True
    capture_reservation = capture_reservation_cancel_response.get_data()
    assert isinstance(capture_reservation, CancelReservation)
