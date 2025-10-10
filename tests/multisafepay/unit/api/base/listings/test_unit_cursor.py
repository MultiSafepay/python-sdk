# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the cursor listing helper."""


from multisafepay.api.base.listings.cursor import Cursor


def test_initialization_with_valid_data():
    """
    Test the initialization of a Cursor object with valid data.

    """
    cursor = Cursor(after="123", before="456")
    assert cursor.after == "123"
    assert cursor.before == "456"


def test_initialization_with_none_data():
    """
    Test the initialization of a Cursor object with None data.
    """
    cursor = Cursor()
    assert cursor.after is None
    assert cursor.before is None


def test_from_dict_with_valid_data():
    """
    Test the creation of a Cursor object from a dictionary with valid data.
    """
    data = {"after": "123", "before": "456"}
    cursor = Cursor.from_dict(data)
    assert cursor.after == "123"
    assert cursor.before == "456"


def test_from_dict_with_none_data():
    """
    Test the creation of a Cursor object from a dictionary with None data.

    """
    data = {"after": None, "before": None}
    cursor = Cursor.from_dict(data)
    assert cursor.after is None
    assert cursor.before is None


def test_from_dict_with_missing_keys():
    """
    Test the creation of a Cursor object from a dictionary with missing keys.
    """
    data = {}
    cursor = Cursor.from_dict(data)
    assert cursor.after is None
    assert cursor.before is None


def test_from_dict_with_none_object():
    """
    Test the creation of a Cursor object from a None object.
    """
    cursor = Cursor.from_dict(None)
    assert cursor is None
