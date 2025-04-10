# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import pytest
from pydantic import ValidationError

from multisafepay.value_object.phone_number import PhoneNumber


def test_phone_number_initialization():
    """
    Test the initialization of a PhoneNumber object with a valid phone number.


    """
    phone_number = PhoneNumber(phone_number="1234567890")
    assert phone_number.phone_number == "1234567890"


def test_empty_phone_number_initialization():
    """
    Test the initialization of a PhoneNumber object with no phone number.

    Raises
    ------
    ValidationError
        If a ValidationError is not raised when initializing without a phone number.

    """
    with pytest.raises(ValidationError):
        PhoneNumber()


def test_valid_cast_phone_number_initialization():
    """
    Test the initialization of a PhoneNumber object with a valid phone number cast from an integer.

    Raises
    ------
    AssertionError
        If the phone number does not match the expected string value.

    """
    phone_number = PhoneNumber(phone_number=1234567890)
    assert phone_number.phone_number == "1234567890"


def test_invalid_phone_number_initialization():
    """
    Test the initialization of a PhoneNumber object with an invalid phone number (None).

    Raises
    ------
    ValidationError
        If a ValidationError is not raised when initializing with an invalid phone number.

    """
    with pytest.raises(ValidationError):
        PhoneNumber(phone_number=None)


def test_phone_number_get_phone_number():
    """
    Test the get method of the PhoneNumber object.

    Raises
    ------
    AssertionError
        If the returned phone number does not match the expected value.

    """
    phone_number = PhoneNumber(phone_number="1234567890")
    assert phone_number.get() == "1234567890"
