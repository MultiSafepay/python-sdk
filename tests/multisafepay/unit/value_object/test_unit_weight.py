# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Value object for Test Unit Weight data."""

from pydantic.error_wrappers import ValidationError
import pytest

from multisafepay.value_object.weight import Weight


def test_weight_initialization():
    """
    Test the initialization of the Weight object with valid unit and quantity.
    """
    weight = Weight(unit="kg", value=10)
    assert weight.unit == "kg"
    assert weight.value == 10


def test_empty_weight_initialization():
    """
    Test the initialization of the Weight object with no unit or quantity.
    """
    weight = Weight()
    assert weight.unit is None
    assert weight.value is None


def test_cast_allowed_weight_unit():
    """
    Test the initialization of the Weight object with a numeric unit.
    """
    weight = Weight(unit=0, value=10)
    assert weight.unit == "0"


def test_invalid_weight_unit():
    """
    Test the initialization of the Weight object with an invalid unit type.
    """
    with pytest.raises(ValidationError):
        Weight(unit={}, value=10)


def test_invalid_weight_quantity():
    """
    Test the initialization of the Weight object with an invalid quantity type.
    """
    with pytest.raises(ValidationError):
        Weight(unit="kg", value={})


def test_weight_get_unit():
    """
    Test the get_unit method of the Weight object.
    """
    weight = Weight(unit="lb", value=5)
    assert weight.get_unit() == "lb"


def test_weight_get_quantity():
    """
    Test the get_quantity method of the Weight object.
    """
    weight = Weight(unit="g", value=500)
    assert weight.value == 500
