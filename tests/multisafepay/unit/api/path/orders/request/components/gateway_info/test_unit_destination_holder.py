# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.gateway_info.destination_holder import (
    DestinationHolder,
)


def test_initializes_destination_holder_correctly():
    """
    Test that a DestinationHolder object is correctly initialized with given values.
    """
    destination_holder = DestinationHolder(
        name="Jane Doe",
        city="Amsterdam",
        country="NL",
        iban="NL91ABNA0417164300",
        swift="ABNANL2A",
    )

    assert destination_holder.name == "Jane Doe"
    assert destination_holder.city == "Amsterdam"
    assert destination_holder.country == "NL"
    assert destination_holder.iban == "NL91ABNA0417164300"
    assert destination_holder.swift == "ABNANL2A"


def test_initializes_destination_holder_with_empty_values():
    """
    Test that a DestinationHolder object is correctly initialized with empty values.
    """
    destination_holder = DestinationHolder()

    assert destination_holder.name is None
    assert destination_holder.city is None
    assert destination_holder.country is None
    assert destination_holder.iban is None
    assert destination_holder.swift is None


def test_add_name_updates_value():
    """
    Test that the add_name method updates the name attribute.
    """
    request = DestinationHolder()
    request_update = request.add_name("Jane Doe")

    assert request.name == "Jane Doe"
    assert isinstance(request_update, DestinationHolder)


def test_add_city_updates_value():
    """
    Test that the add_city method updates the city attribute.
    """
    request = DestinationHolder()
    request_update = request.add_city("Amsterdam")

    assert request.city == "Amsterdam"
    assert isinstance(request_update, DestinationHolder)


def test_add_country_updates_value():
    """
    Test that the add_country method updates the country attribute.
    """
    request = DestinationHolder()
    request_update = request.add_country("NL")

    assert request.country == "NL"
    assert isinstance(request_update, DestinationHolder)


def test_add_iban_updates_value():
    """
    Test that the add_iban method updates the iban attribute.
    """
    request = DestinationHolder()
    request_update = request.add_iban("NL91ABNA0417164300")

    assert request.iban == "NL91ABNA0417164300"
    assert isinstance(request_update, DestinationHolder)


def test_add_swift_updates_value():
    """
    Test that the add_swift method updates the swift attribute.
    """
    request = DestinationHolder()
    request_update = request.add_swift("ABNANL2A")

    assert request.swift == "ABNANL2A"
    assert isinstance(request_update, DestinationHolder)
