# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.gateway_info.account import (
    Account,
)


def test_initializes_account_correctly():
    """
    Test that an Account object is correctly initialized with given values.
    """
    account = Account(
        account_id="12345",
        account_holder_name="John Doe",
        account_holder_iban="NL91ABNA0417164300",
        emandate="EM123",
    )

    assert account.account_id == "12345"
    assert account.account_holder_name == "John Doe"
    assert account.account_holder_iban == "NL91ABNA0417164300"
    assert account.emandate == "EM123"


def test_initializes_account_with_empty_values():
    """
    Test that an Account object is correctly initialized with empty values.
    """
    account = Account()

    assert account.account_id is None
    assert account.account_holder_name is None
    assert account.account_holder_iban is None
    assert account.emandate is None


def test_add_account_id_updates_value():
    """
    Test that the add_account_id method updates the account_id attribute.
    """
    request = Account()
    request_updated = request.add_account_id("NL91ABNA0417164300")

    assert request.account_id == "NL91ABNA0417164300"
    assert isinstance(request_updated, Account)


def test_add_account_holder_name_updates_value():
    """
    Test that the add_account_holder_name method updates the account_holder_name attribute.
    """
    request = Account()
    request_updated = request.add_account_holder_name("John Doe")

    assert request.account_holder_name == "John Doe"
    assert isinstance(request_updated, Account)


def test_add_account_holder_iban_updates_value():
    """
    Test that the add_account_holder_iban method updates the account_holder_iban attribute.
    """
    request = Account()
    request_updated = request.add_account_holder_iban("NL91ABNA0417164300")

    assert request.account_holder_iban == "NL91ABNA0417164300"
    assert isinstance(request_updated, Account)


def test_add_emandate_updates_value():
    """
    Test that the add_emandate method updates the emandate attribute.
    """
    request = Account()
    request_updated = request.add_emandate("EM123")

    assert request.emandate == "EM123"
    assert isinstance(request_updated, Account)
