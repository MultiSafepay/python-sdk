# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import pytest
from pydantic import ValidationError

from multisafepay.value_object.amount import Amount


def test_amount_initialization():
    """
    Test the initialization of an Amount object with a valid amount value.

    """
    amount = Amount(amount=100)
    assert amount.amount == 100


def test_empty_amount_initialization():
    """
    Test the initialization of an Amount object without providing an amount value.


    """
    with pytest.raises(ValidationError):
        Amount()


def test_cast_initialization_valid():
    """
    Test the initialization of an Amount object with a valid amount value as a string.

    """
    amount = Amount(amount="100")
    assert amount.amount == 100


def test_amount_initialization_zero():
    """
    Test the initialization of an Amount object with a zero amount value.

    """
    amount = Amount(amount=0)
    assert amount.amount == 0


def test_amount_initialization_negative():
    """
    Test the initialization of an Amount object with a negative amount value.

    """
    amount = Amount(amount=-50)
    assert amount.amount == -50


def test_amount_get():
    """
    Test the get method of the Amount object.

    """
    amount = Amount(amount=100)
    assert amount.get() == 100
