# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.base.listings.listing_pager import ListingPager


class MockItem:
    def __init__(self: "MockItem", value: object) -> None:
        """
        Initialize a MockItem with a given value.

        """
        self.value = value


def test_listing_pager_with_not_pager():
    """
    Test the initialization of a ListingPager object with valid data and no Pager.

    """
    data = [{"value": 1}, {"value": 2}]
    listing_pager = ListingPager(data=data, pager=None, class_type=MockItem)
    assert len(listing_pager) == 2
    assert listing_pager[0].value == 1
    assert listing_pager[1].value == 2
    assert listing_pager.get_pager() is None
