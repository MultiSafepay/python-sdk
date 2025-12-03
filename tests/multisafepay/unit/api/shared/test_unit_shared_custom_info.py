# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the shared custom info model."""


from multisafepay.api.shared.custom_info import CustomInfo


def test_initializes_with_valid_values():
    """Test that a CustomInfo instance initializes with valid values."""
    custom_info = CustomInfo(
        custom_1="Info 1",
        custom_2="Info 2",
        custom_3="Info 3",
    )
    assert custom_info.custom_1 == "Info 1"
    assert custom_info.custom_2 == "Info 2"
    assert custom_info.custom_3 == "Info 3"


def test_initializes_with_default_values():
    """Test that a CustomInfo instance initializes with default values."""
    custom_info = CustomInfo()
    assert custom_info.custom_1 is None
    assert custom_info.custom_2 is None
    assert custom_info.custom_3 is None


def test_adds_custom_1():
    """Test that custom information is added to the first field."""
    custom_info = CustomInfo().add_custom_1("Info 1")
    assert custom_info.custom_1 == "Info 1"


def test_adds_custom_2():
    """Test that custom information is added to the second field."""
    custom_info = CustomInfo().add_custom_2("Info 2")
    assert custom_info.custom_2 == "Info 2"


def test_adds_custom_3():
    """Test that custom information is added to the third field."""
    custom_info = CustomInfo().add_custom_3("Info 3")
    assert custom_info.custom_3 == "Info 3"


def test_creates_from_dict_with_all_fields():
    """Test that a CustomInfo instance is created from a dictionary with all fields."""
    data = {"custom_1": "Info 1", "custom_2": "Info 2", "custom_3": "Info 3"}
    custom_info = CustomInfo.from_dict(data)
    assert custom_info.custom_1 == "Info 1"
    assert custom_info.custom_2 == "Info 2"
    assert custom_info.custom_3 == "Info 3"


def test_creates_from_dict_with_some_fields():
    """Test that a CustomInfo instance is created from a dictionary with some fields."""
    data = {"custom_1": "Info 1", "custom_3": "Info 3"}
    custom_info = CustomInfo.from_dict(data)
    assert custom_info.custom_1 == "Info 1"
    assert custom_info.custom_2 is None
    assert custom_info.custom_3 == "Info 3"


def test_creates_from_empty_dict():
    """Test that a CustomInfo instance is created from an empty dictionary."""
    data = {}
    custom_info = CustomInfo.from_dict(data)
    assert custom_info.custom_1 is None
    assert custom_info.custom_2 is None
    assert custom_info.custom_3 is None


def test_creates_from_none():
    """Test that a CustomInfo instance is created from None."""
    custom_info = CustomInfo.from_dict(None)
    assert custom_info is None
