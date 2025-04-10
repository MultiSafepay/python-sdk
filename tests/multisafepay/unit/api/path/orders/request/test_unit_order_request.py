# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

import pytest

from multisafepay.api.paths.orders.request.order_request import OrderRequest
from multisafepay.exception.invalid_argument import InvalidArgumentException


def test_initializes_order_request_correctly():
    """
    Tests that the OrderRequest object is initialized correctly with the given values.
    """
    order_request = OrderRequest(
        type="direct",
        gateway="test_gateway",
        order_id="12345",
        currency="USD",
        amount="1000",
        payment_options=None,
        customer=None,
        delivery=None,
        gateway_info={"info": "test"},
        description="Test description",
        recurring_id="rec123",
        google_analytics=None,
        shopping_cart=None,
        checkout_options=None,
        seconds_active=3600,
        days_active=30,
        plugin=None,
        recurring_model="subscription",
        custom_info=None,
        second_chance=None,
        var1="var1",
        var2="var2",
        var3="var3",
    )

    assert order_request.type == "direct"
    assert order_request.gateway == "test_gateway"
    assert order_request.order_id == "12345"
    assert order_request.currency == "USD"
    assert order_request.amount == 1000
    assert order_request.gateway_info == {"info": "test"}
    assert order_request.description == "Test description"
    assert order_request.recurring_id == "rec123"
    assert order_request.seconds_active == 3600
    assert order_request.days_active == 30
    assert order_request.recurring_model == "subscription"
    assert order_request.var1 == "var1"
    assert order_request.var2 == "var2"
    assert order_request.var3 == "var3"


def test_initializes_order_request_with_default_values():
    """
    Tests that the OrderRequest object is initialized with default values when no arguments are provided.
    """
    order_request = OrderRequest()

    assert order_request.type is None
    assert order_request.gateway is None
    assert order_request.order_id is None
    assert order_request.currency is None
    assert order_request.amount is None
    assert order_request.payment_options is None
    assert order_request.customer is None
    assert order_request.delivery is None
    assert order_request.gateway_info is None
    assert order_request.description is None
    assert order_request.recurring_id is None
    assert order_request.google_analytics is None
    assert order_request.shopping_cart is None
    assert order_request.checkout_options is None
    assert order_request.seconds_active is None
    assert order_request.days_active is None
    assert order_request.plugin is None
    assert order_request.recurring_model is None
    assert order_request.custom_info is None
    assert order_request.second_chance is None
    assert order_request.var1 is None
    assert order_request.var2 is None
    assert order_request.var3 is None


def test_add_type_updates_value():
    """
    Tests that the add_type method updates the type field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_type("direct")

    assert order_request.type == "direct"
    assert isinstance(order_request_updated, OrderRequest)


def test_add_type_raises_exception_for_invalid_value():
    """
    Tests that the add_type method raises an InvalidArgumentException for an invalid type value.
    """
    order_request = OrderRequest()
    with pytest.raises(InvalidArgumentException) as excinfo:
        order_request.add_type("invalid_type")
    assert (
        str(excinfo.value)
        == 'Type "invalid_type" is not a known type. Available types: direct, redirect, paymentlink'
    )


def test_add_recurring_model_updates_value():
    """
    Tests that the add_recurring_model method updates the recurring_model field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_recurring_model("subscription")

    assert order_request.recurring_model == "subscription"
    assert isinstance(order_request_updated, OrderRequest)


def test_add_recurring_model_raises_exception_for_invalid_value():
    """
    Tests that the add_recurring_model method raises an InvalidArgumentException for an invalid recurring_model value.
    """
    order_request = OrderRequest()
    with pytest.raises(InvalidArgumentException) as excinfo:
        order_request.add_recurring_model("invalid_model")
    assert (
        str(excinfo.value)
        == 'Type "invalid_model" is not a known type. Available types: cardOnFile, subscription, unscheduled'
    )


def test_add_order_id_updates_value():
    """
    Tests that the add_order_id method updates the order_id field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_order_id("12345")

    assert order_request.order_id == "12345"
    assert isinstance(order_request_updated, OrderRequest)


def test_add_currency_updates_value():
    """
    Tests that the add_currency method updates the currency field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_currency("USD")

    assert order_request.currency == "USD"
    assert isinstance(order_request_updated, OrderRequest)


def test_add_amount_updates_value():
    """
    Tests that the add_amount method updates the amount field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_amount(1000)

    assert order_request.amount == 1000
    assert isinstance(order_request_updated, OrderRequest)


def test_add_gateway_updates_value():
    """
    Tests that the add_gateway method updates the gateway field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_gateway("test_gateway")

    assert order_request.gateway == "test_gateway"
    assert isinstance(order_request_updated, OrderRequest)


def test_add_gateway_info_updates_value():
    """
    Tests that the add_gateway_info method updates the gateway_info field correctly.
    """
    order_request = OrderRequest()
    gateway_info = {"info": "test"}
    order_request_updated = order_request.add_gateway_info(gateway_info)

    assert order_request.gateway_info == gateway_info
    assert isinstance(order_request_updated, OrderRequest)


def test_add_description_updates_value():
    """
    Tests that the add_description method updates the description field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_description("Test description")

    assert order_request.description == "Test description"
    assert isinstance(order_request_updated, OrderRequest)


def test_add_recurring_id_updates_value():
    """
    Tests that the add_recurring_id method updates the recurring_id field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_recurring_id("rec123")

    assert order_request.recurring_id == "rec123"
    assert isinstance(order_request_updated, OrderRequest)


def test_add_seconds_active_updates_value():
    """
    Tests that the add_seconds_active method updates the seconds_active field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_seconds_active(3600)

    assert order_request.seconds_active == 3600
    assert isinstance(order_request_updated, OrderRequest)


def test_add_days_active_updates_value():
    """
    Tests that the add_days_active method updates the days_active field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_days_active(30)

    assert order_request.days_active == 30
    assert isinstance(order_request_updated, OrderRequest)


def test_add_var1_updates_value():
    """
    Tests that the add_var1 method updates the var1 field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_var1("var1")

    assert order_request.var1 == "var1"
    assert isinstance(order_request_updated, OrderRequest)


def test_add_var2_updates_value():
    """
    Tests that the add_var2 method updates the var2 field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_var2("var2")

    assert order_request.var2 == "var2"
    assert isinstance(order_request_updated, OrderRequest)


def test_add_var3_updates_value():
    """
    Tests that the add_var3 method updates the var3 field correctly.
    """
    order_request = OrderRequest()
    order_request_updated = order_request.add_var3("var3")

    assert order_request.var3 == "var3"
    assert isinstance(order_request_updated, OrderRequest)
