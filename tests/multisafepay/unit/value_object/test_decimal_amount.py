# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Value object for Test DecimalAmount data."""

from decimal import Decimal

from pydantic.error_wrappers import ValidationError
import pytest

from multisafepay.value_object.decimal_amount import DecimalAmount


def test_decimal_amount_initialization():
    """Test the initialization of the DecimalAmount object with a valid amount."""
    decimal_amount = DecimalAmount(amount=19.99)
    assert decimal_amount.amount == Decimal("19.99")


def test_empty_decimal_amount_initialization():
    """Test the initialization of the DecimalAmount object with an empty dictionary."""
    with pytest.raises(ValidationError):
        DecimalAmount(amount={})


def test_valid_cast_decimal_amount_initialization():
    """Test the initialization of the DecimalAmount object with a string amount."""
    decimal_amount = DecimalAmount(amount="19.99")
    assert decimal_amount.amount == Decimal("19.99")


def test_decimal_amount_get_amount():
    """Test the get method of the DecimalAmount object."""
    decimal_amount = DecimalAmount(amount=19.99)
    assert decimal_amount.get() == Decimal("19.99")
