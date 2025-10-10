# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.customer_info import (
    CustomInfo,
)


def test_initializes_custom_info_correctly():
    """
    Tests that the CustomInfo object is initialized correctly with given values.
    """
    custom_info = CustomInfo(
        custom1="value1",
        custom2="value2",
        custom3="value3",
    )

    assert custom_info.custom1 == "value1"
    assert custom_info.custom2 == "value2"
    assert custom_info.custom3 == "value3"


def test_initializes_custom_info_with_empty_values():
    """
    Tests that the CustomInfo object is initialized with None values when no arguments are provided.
    """
    custom_info = CustomInfo()

    assert custom_info.custom1 is None
    assert custom_info.custom2 is None
    assert custom_info.custom3 is None


def test_add_custom1_updates_value():
    """
    Tests that the add_custom1 method updates the custom1 field correctly.
    """
    custom_info = CustomInfo()
    custom_info_updated = custom_info.add_custom1("value1")

    assert custom_info.custom1 == "value1"
    assert isinstance(custom_info_updated, CustomInfo)


def test_add_custom2_updates_value():
    """
    Tests that the add_custom2 method updates the custom2 field correctly.
    """
    custom_info = CustomInfo()
    custom_info_updated = custom_info.add_custom2("value2")

    assert custom_info.custom2 == "value2"
    assert isinstance(custom_info_updated, CustomInfo)


def test_add_custom3_updates_value():
    """
    Tests that the add_custom3 method updates the custom3 field correctly.
    """
    custom_info = CustomInfo()
    custom_info_updated = custom_info.add_custom3("value3")

    assert custom_info.custom3 == "value3"
    assert isinstance(custom_info_updated, CustomInfo)
