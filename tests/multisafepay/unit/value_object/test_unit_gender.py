# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Value object for Test Unit Gender data."""

import pytest
from pydantic import ValidationError

from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.value_object.gender import Gender


def test_gender_initialization_valid():
    """
    Test the initialization of a Gender object with a valid gender.

    """
    gender = Gender(gender="male")
    assert gender.gender == "male"


def test_gender_is_not_string():
    """
    Test the initialization of a Gender object with a non-string gender.

    """
    with pytest.raises(ValidationError):
        Gender()


def test_unknown_gender():
    """
    Test the initialization of a Gender object with an unknown gender.

    """
    with pytest.raises(InvalidArgumentException):
        Gender(gender="123")


def test_gender_get():
    """
    Test the get method of the Gender object.


    """
    gender = Gender(gender="mr")
    assert gender.get() == "mr"


def test_gender_initialization_invalid():
    """
    Test the initialization of a Gender object with an invalid gender.

    """
    with pytest.raises(InvalidArgumentException):
        Gender(gender="unknown")
