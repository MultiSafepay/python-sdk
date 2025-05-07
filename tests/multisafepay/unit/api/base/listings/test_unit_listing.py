# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from typing import Any

from multisafepay.api.base.listings.listing import Listing


class MockItem:
    def __init__(self: "MockItem", value: Any) -> None:
        self.value = value


def test_initialization_with_valid_data():
    """
    Test the initialization of a Listing object with valid data.

    """
    data = [{"value": 1}, {"value": 2}]
    listing = Listing(data=data, class_type=MockItem)
    assert len(listing) == 2
    assert listing[0].value == 1
    assert listing[1].value == 2


def test_initialization_with_empty_data():
    """
    Test the initialization of a Listing object with empty data.

    """
    data = []
    listing = Listing(data=data, class_type=MockItem)
    assert len(listing) == 0


def test_initialization_with_none_data():
    """
    Test the initialization of a Listing object with None data.

    """
    data = None
    listing = Listing(data=data, class_type=MockItem)
    assert len(listing) == 0


def test_initialization_with_mixed_data():
    """
    Test the initialization of a Listing object with mixed data (valid and None).

    """
    data = [{"value": 1}, None, {"value": 2}]
    listing = Listing(data=data, class_type=MockItem)
    assert len(listing) == 2
    assert listing[0].value == 1
    assert listing[1].value == 2


def test_get_data_returns_correct_list():
    """
    Test the get_data method of a Listing object.

    """
    data = [{"value": 1}, {"value": 2}]
    listing = Listing(data=data, class_type=MockItem)
    data_list = listing.get_data()
    assert len(data_list) == 2
    assert data_list[0].value == 1
    assert data_list[1].value == 2


def test_append_adds_item_to_list():
    """
    Test the append method of a Listing object.

    """
    data = [{"value": 1}]
    listing = Listing(data=data, class_type=MockItem)
    new_item = MockItem(value=2)
    listing.append(new_item)
    assert len(listing) == 2
    assert listing[1].value == 2
