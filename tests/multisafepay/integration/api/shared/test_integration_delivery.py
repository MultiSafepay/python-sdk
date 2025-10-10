# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Shared API models and utilities."""

from multisafepay.api.shared.delivery import Delivery
from multisafepay.value_object.country import Country
from multisafepay.value_object.email_address import EmailAddress
from multisafepay.value_object.phone_number import PhoneNumber


def test_adds_country():
    """
    Test that a country is added to the Delivery instance.

    This test verifies that the country is correctly set.


    """
    country = Country(code="NL")
    delivery = Delivery().add_country(country)
    assert delivery.country == "NL"


def test_adds_country_code_as_string():
    """
    Test that a country code as a string is added to the Delivery instance.

    This test verifies that the country is correctly set.

    """
    delivery = Delivery().add_country("NL")
    assert delivery.country == "NL"


def test_adds_phone():
    """
    Test that a phone number is added to the Delivery instance.

    This test verifies that the phone number is correctly set.

    """
    phone = PhoneNumber(phone_number="555-1234")
    delivery = Delivery().add_phone(phone)
    assert delivery.phone == "555-1234"


def test_adds_phone_number_as_string():
    """
    Test that a phone number as a string is added to the Delivery instance.

    This test verifies that the phone number is correctly set.

    """
    delivery = Delivery().add_phone("555-1234")
    assert delivery.phone == "555-1234"


def test_adds_email():
    """
    Test that an email address is added to the Delivery instance.

    This test verifies that the email address is correctly set.

    """
    email = EmailAddress(email_address="john.doe@example.com")
    delivery = Delivery().add_email(email)
    assert delivery.email == "john.doe@example.com"


def test_adds_email_address_as_string():
    """
    Test that an email address as a string is added to the Delivery instance.

    This test verifies that the email address is correctly set.

    """
    delivery = Delivery().add_email("john.doe@multisafepay.com")
    assert delivery.email == "john.doe@multisafepay.com"
