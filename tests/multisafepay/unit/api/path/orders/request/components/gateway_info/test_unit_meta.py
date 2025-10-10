# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.gateway_info.meta import (
    Meta,
)


def test_initializes_meta_correctly():
    """
    Test that a Meta object is correctly initialized with given data.
    """
    meta = Meta(
        birthday="1990-01-01",
        bank_account="NL91ABNA0417164300",
        phone="+1234567890",
        email_address="test@example.com",
        gender="M",
    )

    assert meta.birthday == "1990-01-01"
    assert meta.bank_account == "NL91ABNA0417164300"
    assert meta.phone == "+1234567890"
    assert meta.email_address == "test@example.com"
    assert meta.gender == "M"


def test_initializes_meta_with_empty_values():
    """
    Test that a Meta object is correctly initialized with empty values.
    """
    meta = Meta()

    assert meta.birthday is None
    assert meta.bank_account is None
    assert meta.phone is None
    assert meta.email_address is None
    assert meta.gender is None


def test_add_birthday_updates_value():
    """
    Test that the add_birthday method updates the birthday attribute to the given value.
    """
    request = Meta()
    request_updated = request.add_birthday("1990-01-01")

    assert request.birthday == "1990-01-01"
    assert isinstance(request_updated, Meta)


def test_add_bank_account_updates_value():
    """
    Test that the add_bank_account method updates the bank_account attribute to the given value.
    """
    request = Meta()
    request_updated = request.add_bank_account("NL91ABNA0417164300")

    assert request.bank_account == "NL91ABNA0417164300"
    assert isinstance(request_updated, Meta)


def test_add_phone_updates_value():
    """
    Test that the add_phone method updates the phone attribute to the given value.
    """
    request = Meta()
    request_updated = request.add_phone("+1234567890")

    assert request.phone == "+1234567890"
    assert isinstance(request_updated, Meta)


def test_add_email_address_updates_value():
    """
    Test that the add_email_address method updates the email_address attribute to the given value.
    """
    request = Meta()
    request_updated = request.add_email_address("test@example.com")

    assert request.email_address == "test@example.com"
    assert isinstance(request_updated, Meta)


def test_add_gender_updates_value():
    """
    Test that the add_gender method updates the gender attribute to the given value.
    """
    request = Meta()
    request_updated = request.add_gender("male")

    assert request.gender == "male"
    assert isinstance(request_updated, Meta)
