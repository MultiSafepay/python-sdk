# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import pytest
from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.value_object.currency import Currency


def test_currency_initialization():
    """
    Test the initialization of a Currency object with a valid currency code.

    """
    currency = Currency(currency="USD")
    assert currency.currency == "USD"


def test_currency_is_not_string():
    """
    Test the initialization of a Currency object with a non-string currency code.


    """
    with pytest.raises(
        InvalidArgumentException,
        match='Value "0" is not a valid currency code',
    ):
        Currency(currency=0)


def test_currency_get():
    """
    Test the get method of the Currency object.

    """
    currency = Currency(currency="USD")
    assert currency.get() == "USD"
