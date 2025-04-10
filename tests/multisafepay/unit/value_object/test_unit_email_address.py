# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import pytest
from pydantic import ValidationError

from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.value_object.email_address import EmailAddress


def test_email_address_initialization():
    """
    Test the initialization of an EmailAddress object with a valid email address.

    """
    email_address = EmailAddress(email_address="test@example.com")
    assert email_address.email_address == "test@example.com"


def test_email_address_initialization_with_invalid_email():
    """
    Test the initialization of an EmailAddress object with an invalid email address.

    """
    with pytest.raises(InvalidArgumentException):
        EmailAddress(email_address="invalid-email")


def test_email_address_initialization_is_not_string():
    """
    Test the initialization of an EmailAddress object with a non-string email address.

    """
    with pytest.raises(ValidationError):
        EmailAddress(email_address=None)


def test_email_address_get():
    """
    Test the get method of the EmailAddress object.


    """
    email_address = EmailAddress(email_address="user@domain.com")
    assert email_address.get() == "user@domain.com"


def test_is_valid_email():
    """
    Test the is_valid_email method of the EmailAddress class.

    """
    assert EmailAddress.is_valid_email("valid.email@example.com")
    assert not EmailAddress.is_valid_email("invalid-email")
    assert not EmailAddress.is_valid_email("invalid@domain")
    assert not EmailAddress.is_valid_email("invalid@domain.")
    assert not EmailAddress.is_valid_email("@domain.com")
