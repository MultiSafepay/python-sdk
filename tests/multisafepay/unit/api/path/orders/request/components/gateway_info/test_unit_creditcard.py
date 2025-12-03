# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.gateway_info.creditcard import (
    Creditcard,
)


def test_initializes_creditcard_correctly():
    """Test that a Creditcard object is correctly initialized with given values."""
    creditcard = Creditcard(
        card_number="4111111111111111",
        card_holder_name="John Doe",
        card_expiry_date="12/25",
        cvc="123",
        flexible_3d=True,
        term_url="https://example.com/term",
    )

    assert creditcard.card_number == "4111111111111111"
    assert creditcard.card_holder_name == "John Doe"
    assert creditcard.card_expiry_date == "12/25"
    assert creditcard.cvc == "123"
    assert creditcard.flexible_3d is True
    assert creditcard.term_url == "https://example.com/term"


def test_initializes_creditcard_with_empty_values():
    """Test that a Creditcard object is correctly initialized with empty values."""
    creditcard = Creditcard()

    assert creditcard.card_number is None
    assert creditcard.card_holder_name is None
    assert creditcard.card_expiry_date is None
    assert creditcard.cvc is None
    assert creditcard.flexible_3d is None
    assert creditcard.term_url is None


def test_add_card_number_updates_value():
    """Test that the add_card_number method updates the card_number attribute."""
    request = Creditcard()
    request_updated = request.add_card_number("4111111111111111")

    assert request.card_number == "4111111111111111"
    assert isinstance(request_updated, Creditcard)


def test_add_card_holder_name_updates_value():
    """Test that the add_card_holder_name method updates the card_holder_name attribute."""
    request = Creditcard()
    request_updated = request.add_card_holder_name("John Doe")

    assert request.card_holder_name == "John Doe"
    assert isinstance(request_updated, Creditcard)


def test_add_card_expiry_date_updates_value():
    """Test that the add_card_expiry_date method updates the card_expiry_date attribute."""
    request = Creditcard()
    request_updated = request.add_card_expiry_date("12/25")

    assert request.card_expiry_date == "12/25"
    assert isinstance(request_updated, Creditcard)


def test_add_cvc_updates_value():
    """Test that the add_cvc method updates the cvc attribute."""
    request = Creditcard()
    request_updated = request.add_cvc("123")

    assert request.cvc == "123"
    assert isinstance(request_updated, Creditcard)


def test_add_flexible_3d_updates_value():
    """Test that the add_flexible_3d method updates the flexible_3d attribute."""
    request = Creditcard()
    request_updated = request.add_flexible_3d(True)

    assert request.flexible_3d is True
    assert isinstance(request_updated, Creditcard)


def test_add_term_url_updates_value():
    """Test that the add_term_url method updates the term_url attribute."""
    request = Creditcard()
    request_updated = request.add_term_url("https://example.com/term")

    assert request.term_url == "https://example.com/term"
    assert isinstance(request_updated, Creditcard)
