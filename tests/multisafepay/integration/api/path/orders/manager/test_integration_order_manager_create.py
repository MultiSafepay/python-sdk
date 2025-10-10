# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Manager class for Test Integration Order Manager Create.Py API operations."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.orders.order_manager import OrderManager
from multisafepay.api.paths.orders.request.components.payment_options import (
    PaymentOptions,
)
from multisafepay.api.paths.orders.request.order_request import OrderRequest
from multisafepay.api.paths.orders.response.order_response import Order
from multisafepay.api.shared.customer import Customer


def test_integration_order_manager_create_redirect():
    """
    Test the create method of OrderManager with a redirect order type.

    This test verifies that the create method correctly processes a redirect order request
    and returns a CustomApiResponse object with the expected data.

    """
    client = MagicMock()
    data_response = {
        "order_id": "apitool_4993758",
        "payment_url": "https://testpayv2.multisafepay.com/connect/8035OnwUENVtofBaUh4h2PIL3k7szAQMeK5/?lang=nl_NL",
        "session_id": "8035OnwUENVtofBaUh4h2PIL3k7szAQMeK5",
        "events_token": "eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDQ4MDQ4NjgsImdydCI6WyJtYnVzOnNlc3Npb24ub3JkZXIiLCJtYnVzOnNlc3Npb24ucXIiXSwicGlkIjoiODAzNU9ud1VFTlZ0b2ZCYVVoNGgyUElMM2s3c3pBUU1lSzUiLCJzdWIiOiJwciJ9.wpAntejhmdI_agMD4ZaDxhrlQsrjDj-Kn6BoawiRQpU",
        "events_url": "wss://testapi.multisafepay.com/events/",
        "events_stream_url": "https://testapi.multisafepay.com/events/stream/",
    }
    client.create_post_request.return_value = ApiResponse(
        headers={},
        status_code=200,
        body={"success": True, "data": data_response},
    )
    payment_options = PaymentOptions(
        notification_url="https://example.com/notification",
        redirect_url="https://example.com/redirect",
        cancel_url="https://example.com/cancel",
    )
    customer_dict = {
        "locale": "nl_NL",
        "ip_address": "185.49.169.194",
        "forwarded_ip": "",
        "first_name": "Testperson-nl",
        "last_name": "Approved",
        "address1": "Neherkade",
        "address2": "",
        "house_number": "XI",
        "zip_code": "2521VA",
        "city": "Gravenhage",
        "state": "",
        "country": "NL",
        "birthday": "10071970",
        "gender": "male",
        "phone": "0612345678",
        "email": "example@multisafepay.com",
        "referrer": "http://test.com",
        "user_agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }
    customer = Customer(**customer_dict)
    order_request = (
        OrderRequest()
        .add_type("redirect")
        .add_order_id("apitool_4993758")
        .add_gateway("")
        .add_currency("EUR")
        .add_amount(100)
        .add_description("Test Order Description")
        .add_payment_options(payment_options)
        .add_customer(customer)
    )

    order_manager = OrderManager(client)
    response = order_manager.create(request_order=order_request)

    assert isinstance(response, CustomApiResponse)
    assert isinstance(response.get_data(), Order)
    assert response.get_data() == Order(**data_response)
