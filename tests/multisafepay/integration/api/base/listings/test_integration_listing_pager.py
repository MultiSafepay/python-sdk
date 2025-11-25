# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for integration testing."""

from multisafepay.api.base.listings.listing_pager import ListingPager
from multisafepay.api.base.listings.pager import Pager
from multisafepay.api.base.listings.cursor import Cursor


class MockItem:
    """Mock item for testing purposes."""

    def __init__(self: "MockItem", value: object) -> None:
        """
        Initialize a MockItem with a given value.

        """
        self.value = value


def test_initialization_with_valid_data_and_pager():
    """
    Test the initialization of a ListingPager object with valid data and a Pager.

    """
    data = [{"value": 1}, {"value": 2}]
    pager = Pager(
        after="a1",
        before="b1",
        limit=10,
        cursor=Cursor(after="c1", before="c2"),
    )
    listing_pager = ListingPager(data=data, pager=pager, class_type=MockItem)
    assert len(listing_pager) == 2
    assert listing_pager[0].value == 1
    assert listing_pager[1].value == 2
    assert listing_pager.pager.after == "a1"
    assert listing_pager.pager.before == "b1"
    assert listing_pager.pager.limit == 10
    assert listing_pager.pager.cursor.after == "c1"
    assert listing_pager.pager.cursor.before == "c2"


def test_initialization_with_empty_data_and_pager():
    """
    Test the initialization of a ListingPager object with empty data and a Pager.

    """
    data = []
    pager = Pager(
        after="a1",
        before="b1",
        limit=10,
        cursor=Cursor(after="c1", before="c2"),
    )
    listing_pager = ListingPager(data=data, pager=pager, class_type=MockItem)
    assert len(listing_pager) == 0
    assert listing_pager.pager.after == "a1"
    assert listing_pager.pager.before == "b1"
    assert listing_pager.pager.limit == 10
    assert listing_pager.pager.cursor.after == "c1"
    assert listing_pager.pager.cursor.before == "c2"


def test_initialization_with_none_data_and_pager():
    """
    Test the initialization of a ListingPager object with None data and a Pager.

    """
    data = None
    pager = Pager(
        after="a1",
        before="b1",
        limit=10,
        cursor=Cursor(after="c1", before="c2"),
    )
    listing_pager = ListingPager(data=data, pager=pager, class_type=MockItem)
    assert len(listing_pager) == 0
    assert listing_pager.pager.after == "a1"
    assert listing_pager.pager.before == "b1"
    assert listing_pager.pager.limit == 10
    assert listing_pager.pager.cursor.after == "c1"
    assert listing_pager.pager.cursor.before == "c2"


def test_listing_pager_with_no_cursor():
    """
    Test the initialization of a ListingPager object with valid data and a Pager with no Cursor.

    """
    data = [{"value": 1}, {"value": 2}]
    pager = Pager(after="a1", before="b1", limit=10, cursor=None)
    listing_pager = ListingPager(data=data, pager=pager, class_type=MockItem)
    assert len(listing_pager) == 2
    assert listing_pager[0].value == 1
    assert listing_pager[1].value == 2
    assert listing_pager.pager.after == "a1"
    assert listing_pager.pager.before == "b1"
    assert listing_pager.pager.limit == 10
    assert listing_pager.pager.cursor is None
