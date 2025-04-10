# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from multisafepay.api.base.listings.pager import Pager


def test_initialization_with_empty_data():
    """
    Test the initialization of a Pager object with empty data.

    """
    pager = Pager()
    assert pager.after is None
    assert pager.before is None
    assert pager.cursor is None


def test_initialization_with_none_cursor():
    """
    Test the initialization of a Pager object with None cursor.

    """
    pager = Pager(after="asd", before="dsa", cursor=None)
    assert pager.after == "asd"
    assert pager.before == "dsa"
    assert pager.cursor is None


def test_initialization_with_none_data():
    """
    Test the initialization of a Pager object from None data.

    """
    data = None
    pager = Pager.from_dict(data)
    assert pager is None


def test_cursor_initialization_with_valid_data():
    """
    Test the initialization of a Cursor object from a dictionary with valid data.

    """
    data = {
        "after": "a1",
        "before": "b1",
        "limit": 10,
        "cursor": None,
    }
    pager = Pager.from_dict(data)
    assert pager.after == "a1"
    assert pager.before == "b1"
    assert pager.limit == 10
    assert pager.cursor is None
