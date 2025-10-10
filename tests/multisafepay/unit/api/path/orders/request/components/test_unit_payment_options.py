# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.payment_options import (
    PaymentOptions,
)
from multisafepay.exception.invalid_argument import InvalidArgumentException


def test_initializes_payment_options_correctly():
    payment_options = PaymentOptions(
        notification_url="https://example.com/notify",
        settings={"key": "value"},
        notification_method="POST",
        redirect_url="https://example.com/redirect",
        cancel_url="https://example.com/cancel",
        close_window=True,
    )

    assert payment_options.notification_url == "https://example.com/notify"
    assert payment_options.settings == {"key": "value"}
    assert payment_options.notification_method == "POST"
    assert payment_options.redirect_url == "https://example.com/redirect"
    assert payment_options.cancel_url == "https://example.com/cancel"
    assert payment_options.close_window is True


def test_initializes_payment_options_with_empty_values():
    payment_options = PaymentOptions()

    assert payment_options.notification_url is None
    assert payment_options.settings is None
    assert payment_options.notification_method is None
    assert payment_options.redirect_url is None
    assert payment_options.cancel_url is None
    assert payment_options.close_window is None


def test_add_notification_url_updates_value():
    payment_options = PaymentOptions()
    payment_options_updated = payment_options.add_notification_url(
        "https://example.com/notify",
    )

    assert payment_options.notification_url == "https://example.com/notify"
    assert isinstance(payment_options_updated, PaymentOptions)


def test_add_settings_updates_value():
    payment_options = PaymentOptions()
    payment_options_updated = payment_options.add_settings({"key": "value"})

    assert payment_options.settings == {"key": "value"}
    assert isinstance(payment_options_updated, PaymentOptions)


def test_add_notification_method_updates_value():
    payment_options = PaymentOptions()
    payment_options_updated = payment_options.add_notification_method("GET")

    assert payment_options.notification_method == "GET"
    assert isinstance(payment_options_updated, PaymentOptions)


def test_add_notification_method_raises_exception_for_invalid_value():
    payment_options = PaymentOptions()

    try:
        payment_options.add_notification_method("INVALID")
    except InvalidArgumentException as e:
        assert str(e) == 'Notification method can only be "GET" or "POST"'


def test_add_redirect_url_updates_value():
    payment_options = PaymentOptions()
    payment_options_updated = payment_options.add_redirect_url(
        "https://example.com/redirect",
    )

    assert payment_options.redirect_url == "https://example.com/redirect"
    assert isinstance(payment_options_updated, PaymentOptions)


def test_add_cancel_url_updates_value():
    payment_options = PaymentOptions()
    payment_options_updated = payment_options.add_cancel_url(
        "https://example.com/cancel",
    )

    assert payment_options.cancel_url == "https://example.com/cancel"
    assert isinstance(payment_options_updated, PaymentOptions)


def test_add_close_window_updates_value():
    payment_options = PaymentOptions()
    payment_options_updated = payment_options.add_close_window(True)

    assert payment_options.close_window is True
    assert isinstance(payment_options_updated, PaymentOptions)
