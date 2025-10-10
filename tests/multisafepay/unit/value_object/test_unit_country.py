# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Value object for Test Unit Country data."""

import pytest
from pydantic import ValidationError

from multisafepay.value_object.country import Country
from multisafepay.exception.invalid_argument import InvalidArgumentException


def test_country_initialization_with_valid_code():
    """
    Test the initialization of a Country object with a valid country code.

    """
    country = Country(code="US")
    assert country.code == "US"


def test_country_initialization_with_invalid_code_length():
    """
    Test the initialization of a Country object with an invalid country code length.

    """
    with pytest.raises(InvalidArgumentException):
        Country(code="USA")


def test_country_initialization_with_empty_code():
    """
    Test the initialization of a Country object with an empty country code.

    """
    with pytest.raises(ValidationError):
        Country()


def test_country_initialization_with_lowercase_code():
    """
    Test the initialization of a Country object with a lowercase country code.


    """
    country = Country(code="nl")
    assert country.get_code() == "NL"


def test_country_initialization_with_uppercase_code():
    """
    Test the initialization of a Country object with an uppercase country code.

    """
    country = Country(code="DE")
    assert country.get_code() == "DE"
