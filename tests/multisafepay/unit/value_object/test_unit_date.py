# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import pytest
from datetime import datetime

from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.value_object.date import Date


def test_date_initialization():
    """
    Test the initialization of a Date object with a valid date string.

    """
    date_str = "2023-10-10"
    date = Date(date=date_str)
    assert date.str_date == date_str
    assert (
        date.timestamp == datetime.strptime(date_str, "%Y-%m-%d").timestamp()
    )


def test_date_initialization_is_not_string():
    """
    Test the initialization of a Date object with a non-string date.


    """
    with pytest.raises(TypeError):
        Date()


def test_date_initialization_no_format():
    """
    Test the initialization of a Date object with an invalid date string.


    """
    with pytest.raises(
        InvalidArgumentException,
        match='Value "invalid-date" is an invalid date format',
    ):
        Date(date="invalid-date")


def test_date_initialization_invalid_format():
    """
    Test the initialization of a Date object with a date string in an invalid format.


    """
    with pytest.raises(
        InvalidArgumentException,
        match='Value "10-10-2023" is an invalid date format',
    ):
        Date(date="10-10-2023")


def test_date_get_default_format():
    """
    Test the get method of the Date object with the default format.

    """
    date_str = "2023-10-10"
    date_obj = Date(date_str)
    assert date_obj.get() == date_str


def test_date_get_custom_format():
    """
    Test the get method of the Date object with a custom format.


    """
    date_str = "2023-10-10"
    date_obj = Date(date_str)
    assert date_obj.get("%d-%m-%Y") == "10-10-2023"


def test_date_get_custom_format_2():
    """
    Test the get method of the Date object with another custom format.


    """
    date_str = "2023-10-10"
    date_obj = Date(date_str)
    assert date_obj.get("%Y/%m/%d") == "2023/10/10"


def test_date_get_custom_format_3():
    """
    Test the get method of the Date object with a custom format for a date-time string.


    """
    date_str = "2025-03-02T00:34:46"
    date_obj = Date(date_str)
    assert date_obj.get("%Y-%m-%d") == "2025-03-02"
