# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.shared.delivery import Delivery


def test_initializes_with_valid_values():
    """
    Test that a Delivery instance initializes with valid values.
    """
    delivery = Delivery(
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
        street_name="Main St",
        street_name_additional="Near the park",
        house_number_suffix="A",
    )
    assert delivery.first_name == "John"
    assert delivery.last_name == "Doe"
    assert delivery.address1 == "123 Main St"
    assert delivery.address2 == "Apt 4"
    assert delivery.house_number == "123"
    assert delivery.zip_code == "12345"
    assert delivery.city == "Anytown"
    assert delivery.state == "CA"
    assert delivery.country == "USA"
    assert delivery.phone == "555-1234"
    assert delivery.email == "example@multisafepay.com"
    assert delivery.street_name == "Main St"
    assert delivery.street_name_additional == "Near the park"
    assert delivery.house_number_suffix == "A"


def test_initializes_with_default_values():
    """
    Test that a Delivery instance initializes with default values.
    """
    delivery = Delivery()
    assert delivery.first_name is None
    assert delivery.last_name is None
    assert delivery.address1 is None
    assert delivery.address2 is None
    assert delivery.house_number is None
    assert delivery.zip_code is None
    assert delivery.city is None
    assert delivery.state is None
    assert delivery.country is None
    assert delivery.phone is None
    assert delivery.email is None
    assert delivery.street_name is None
    assert delivery.street_name_additional is None
    assert delivery.house_number_suffix is None


def test_adds_first_name():
    """
    Test that a first name is added to the Delivery instance.
    """
    delivery = Delivery().add_first_name("John")
    assert delivery.first_name == "John"


def test_adds_last_name():
    """
    Test that a last name is added to the Delivery instance.
    """
    delivery = Delivery().add_last_name("Doe")
    assert delivery.last_name == "Doe"


def test_adds_address1():
    """
    Test that a primary address line is added to the Delivery instance.
    """
    delivery = Delivery().add_address1("123 Main St")
    assert delivery.address1 == "123 Main St"


def test_adds_address2():
    """
    Test that a secondary address line is added to the Delivery instance.
    """
    delivery = Delivery().add_address2("Apt 4")
    assert delivery.address2 == "Apt 4"


def test_adds_house_number():
    """
    Test that a house number is added to the Delivery instance.
    """
    delivery = Delivery().add_house_number("123")
    assert delivery.house_number == "123"


def test_adds_zip_code():
    """
    Test that a postal code is added to the Delivery instance.
    """
    delivery = Delivery().add_zip_code("12345")
    assert delivery.zip_code == "12345"


def test_adds_city():
    """
    Test that a city is added to the Delivery instance.
    """
    delivery = Delivery().add_city("Anytown")
    assert delivery.city == "Anytown"


def test_adds_state():
    """
    Test that a state or province is added to the Delivery instance.
    """
    delivery = Delivery().add_state("CA")
    assert delivery.state == "CA"


def test_adds_street_name():
    """
    Test that a street name is added to the Delivery instance.
    """
    delivery = Delivery().add_street_name("Main St")
    assert delivery.street_name == "Main St"


def test_adds_street_name_as_string():
    """
    Test that a street name as a string is added to the Delivery instance.
    """
    delivery = Delivery().add_street_name("Main St")
    assert delivery.street_name == "Main St"


def test_adds_street_name_additional():
    """
    Test that additional street name information is added to the Delivery instance.
    """
    delivery = Delivery().add_street_name_additional("Near the park")
    assert delivery.street_name_additional == "Near the park"


def test_adds_house_number_suffix():
    """
    Test that a house number suffix is added to the Delivery instance.
    """
    delivery = Delivery().add_house_number_suffix("A")
    assert delivery.house_number_suffix == "A"


def test_creates_from_dict_with_all_fields():
    """
    Test that a Delivery instance is created from a dictionary with all fields.
    """
    data = {
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
        "street_name": "Main St",
        "street_name_additional": "Near the park",
        "house_number_suffix": "A",
    }
    delivery = Delivery.from_dict(data)
    assert delivery.first_name == "John"
    assert delivery.last_name == "Doe"
    assert delivery.address1 == "123 Main St"
    assert delivery.address2 == "Apt 4"
    assert delivery.house_number == "123"
    assert delivery.zip_code == "12345"
    assert delivery.city == "Anytown"
    assert delivery.state == "CA"
    assert delivery.country == "USA"
    assert delivery.phone == "555-1234"
    assert delivery.email == "john.doe@example.com"
    assert delivery.street_name == "Main St"
    assert delivery.street_name_additional == "Near the park"
    assert delivery.house_number_suffix == "A"


def test_creates_from_empty_dict():
    """
    Test that a Delivery instance is created from an empty dictionary.
    """
    data = {}
    delivery = Delivery.from_dict(data)
    assert delivery.first_name is None
    assert delivery.last_name is None
    assert delivery.address1 is None
    assert delivery.address2 is None
    assert delivery.house_number is None
    assert delivery.zip_code is None
    assert delivery.city is None
    assert delivery.state is None
    assert delivery.country is None
    assert delivery.phone is None
    assert delivery.email is None
    assert delivery.street_name is None
    assert delivery.street_name_additional is None
    assert delivery.house_number_suffix is None


def test_creates_from_none():
    """
    Test that a Delivery instance is created from None.
    """
    delivery = Delivery.from_dict(None)
    assert delivery is None
