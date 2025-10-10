# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the shared customer model."""


from multisafepay.api.shared.customer import Customer


def test_initializes_with_valid_values():
    """
    Test that a Customer instance initializes with valid values.
    """
    customer = Customer(
        locale="en_US",
        ip_address="10.1.0.1",
        forwarded_ip="10.1.0.1",
        referrer="http://example.com",
        user_agent="Mozilla/5.0",
        first_name="John",
        last_name="Doe",
        address1="123 Main St",
        address2="Apt 4",
        house_number="123",
        zip_code="12345",
        city="Anytown",
        state="CA",
        country="USA",
        phone="555-1234",
        email="example@multisafepay.com",
    )

    assert customer.locale == "en_US"
    assert customer.ip_address == "10.1.0.1"
    assert customer.forwarded_ip == "10.1.0.1"
    assert customer.referrer == "http://example.com"
    assert customer.user_agent == "Mozilla/5.0"
    assert customer.first_name == "John"
    assert customer.last_name == "Doe"
    assert customer.address1 == "123 Main St"
    assert customer.address2 == "Apt 4"
    assert customer.house_number == "123"
    assert customer.zip_code == "12345"
    assert customer.city == "Anytown"
    assert customer.state == "CA"
    assert customer.country == "USA"
    assert customer.phone == "555-1234"
    assert customer.email == "example@multisafepay.com"


def test_initializes_with_default_values():
    """
    Test that a Customer instance initializes with default values.
    """
    customer = Customer()
    assert customer.locale is None
    assert customer.ip_address is None
    assert customer.forwarded_ip is None
    assert customer.referrer is None
    assert customer.user_agent is None


def test_adds_locale():
    """
    Test that a locale is added to the Customer instance.
    """
    customer = Customer().add_locale("en_US")
    assert customer.locale == "en_US"


def test_adds_referrer():
    """
    Test that a referrer URL is added to the Customer instance.
    """
    customer = Customer().add_referrer("http://example.com")
    assert customer.referrer == "http://example.com"


def test_adds_user_agent():
    """
    Test that a user agent string is added to the Customer instance.
    """
    customer = Customer().add_user_agent("Mozilla/5.0")
    assert customer.user_agent == "Mozilla/5.0"


def test_adds_first_name():
    """
    Test that a first name is added to the Customer instance.
    """
    customer = Customer().add_first_name("John")
    assert customer.first_name == "John"


def test_adds_last_name():
    """
    Test that a last name is added to the Customer instance.
    """
    customer = Customer().add_last_name("Doe")
    assert customer.last_name == "Doe"


def test_adds_address1():
    """
    Test that an address1 is added to the Customer instance.
    """
    customer = Customer().add_address1("123 Main St")
    assert customer.address1 == "123 Main St"


def test_adds_address2():
    """
    Test that an address2 is added to the Customer instance.
    """
    customer = Customer().add_address2("Apt 4")
    assert customer.address2 == "Apt 4"


def test_adds_house_number():
    """
    Test that a house number is added to the Customer instance.
    """
    customer = Customer().add_house_number("123")
    assert customer.house_number == "123"


def test_adds_zip_code():
    """
    Test that a zip code is added to the Customer instance.
    """
    customer = Customer().add_zip_code("12345")
    assert customer.zip_code == "12345"


def test_adds_city():
    """
    Test that a city is added to the Customer instance.
    """
    customer = Customer().add_city("Anytown")
    assert customer.city == "Anytown"


def test_adds_state():
    """
    Test that a state is added to the Customer instance.
    """
    customer = Customer().add_state("CA")
    assert customer.state == "CA"


def test_creates_from_dict_with_all_fields():
    """
    Test that a Customer instance is created from a dictionary with all fields.
    """
    data = {
        "locale": "en_US",
        "ip_address": "192.168.0.1",
        "forwarded_ip": "10.0.0.1",
        "referrer": "http://example.com",
        "user_agent": "Mozilla/5.0",
        "first_name": "John",
        "last_name": "Doe",
        "address1": "123 Main St",
        "address2": "Apt 4",
        "house_number": "123",
        "zip_code": "12345",
        "city": "Anytown",
        "state": "CA",
        "country": "USA",
        "phone": "555-1234",
        "email": "john.doe@example.com",
    }
    customer = Customer.from_dict(data)
    assert customer.locale == "en_US"
    assert customer.ip_address == "192.168.0.1"
    assert customer.forwarded_ip == "10.0.0.1"
    assert customer.referrer == "http://example.com"
    assert customer.user_agent == "Mozilla/5.0"
    assert customer.first_name == "John"
    assert customer.last_name == "Doe"
    assert customer.address1 == "123 Main St"
    assert customer.address2 == "Apt 4"
    assert customer.house_number == "123"
    assert customer.zip_code == "12345"
    assert customer.city == "Anytown"
    assert customer.state == "CA"
    assert customer.country == "USA"
    assert customer.phone == "555-1234"
    assert customer.email == "john.doe@example.com"


def test_creates_from_empty_dict():
    """
    Test that a Customer instance is created from an empty dictionary.
    """
    data = {}
    customer = Customer.from_dict(data)
    assert customer.locale is None
    assert customer.ip_address is None
    assert customer.forwarded_ip is None
    assert customer.referrer is None
    assert customer.user_agent is None


def test_creates_from_none():
    """
    Test that a Customer instance is created from None.
    """
    customer = Customer.from_dict(None)
    assert customer is None
