# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Value object for Test Unit Iban Number data."""

import pytest
from pydantic import ValidationError

from multisafepay.value_object.iban_number import IbanNumber
from multisafepay.exception.invalid_argument import InvalidArgumentException


def test_iban_number_initialization_valid():
    """Test the initialization of an IbanNumber object with a valid IBAN number."""
    iban_number = IbanNumber(iban_number="DE89370400440532013000")
    assert iban_number.iban_number == "DE89370400440532013000"


def test_empty_iban_number_initialization():
    """Test the initialization of an IbanNumber object with no IBAN number."""
    with pytest.raises(ValidationError):
        IbanNumber()


def test_iban_number_invalid_argument():
    """Test the initialization of an IbanNumber object with an invalid IBAN number."""
    with pytest.raises(
        InvalidArgumentException,
        match='Value "INVALIDIBAN" is not a valid IBAN number',
    ):
        IbanNumber(iban_number="INVALIDIBAN")


def test_iban_number_get():
    """Test the get method of the IbanNumber object."""
    iban = IbanNumber(iban_number="DE89370400440532013000")
    assert iban.get() == "DE89370400440532013000"


def test_validate_iban_number_valid():
    """Test the validate_iban_number method with a valid IBAN number."""
    assert IbanNumber.validate_iban_number("DE89370400440532013000") is True


def test_validate_iban_number_invalid_length():
    """Test the validate_iban_number method with an IBAN number of invalid length."""
    with pytest.raises(
        InvalidArgumentException,
        match='Value "DE89" is not a valid IBAN number',
    ):
        IbanNumber.validate_iban_number("DE89")


def test_validate_iban_number_invalid_format():
    """Test the validate_iban_number method with an IBAN number of invalid format."""
    with pytest.raises(
        InvalidArgumentException,
        match='Value "INVALIDIBAN" is not a valid IBAN number',
    ):
        IbanNumber.validate_iban_number("INVALIDIBAN")
