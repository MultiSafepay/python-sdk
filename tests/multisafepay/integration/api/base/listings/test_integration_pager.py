# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.base.listings.cursor import Cursor
from multisafepay.api.base.listings.pager import Pager


def test_initialization_with_valid_data():
    """
    Test the initialization of a Pager object with valid data.

    """
    cursor = Cursor(after="c1", before="c2")
    pager = Pager(after="asd", before="dsa", cursor=cursor)
    assert pager.after == "asd"
    assert pager.before == "dsa"
    assert pager.cursor.after == "c1"
    assert pager.cursor.before == "c2"


def test_cursor_initialization_with_valid_data():
    """
    Test the initialization of a Cursor object from a dictionary with valid data.

    """
    data = {
        "after": "a1",
        "before": "b1",
        "limit": 10,
        "cursor": {"after": "c1", "before": "c2"},
    }
    pager = Pager.from_dict(data)
    cursor = pager.cursor
    assert pager.after == "a1"
    assert pager.before == "b1"
    assert pager.limit == 10
    assert cursor.after == "c1"
    assert cursor.before == "c2"
