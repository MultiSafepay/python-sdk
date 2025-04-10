# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from pydantic.error_wrappers import ValidationError
import pytest

from multisafepay.value_object.unit_price import UnitPrice


def test_unit_price_initialization():
    """
    Test the initialization of the UnitPrice object with a valid unit price.

    """
    unit_price = UnitPrice(unit_price=19.99)
    assert unit_price.unit_price == 19.99


def test_empty_unit_price_initialization():
    """
    Test the initialization of the UnitPrice object with an empty dictionary.

    """
    with pytest.raises(ValidationError):
        UnitPrice(unit_price={})


def test_valid_cast_unit_price_initialization():
    """
    Test the initialization of the UnitPrice object with a string unit price.

    """
    unit_price = UnitPrice(unit_price="19.99")
    assert unit_price.unit_price == 19.99


def test_unit_price_get_unit_price():
    """
    Test the get method of the UnitPrice object.

    """
    unit_price = UnitPrice(unit_price=19.99)
    assert unit_price.get() == 19.99
