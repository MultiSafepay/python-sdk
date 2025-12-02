# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Value object for Test Unit Bank Account data."""

import pytest
from multisafepay.value_object.bank_account import BankAccount


def test_bank_account_initialization():
    """Test the initialization of a BankAccount object with a valid bank account number."""
    bank_account = BankAccount(bank_account="NL91ABNA0417164300")
    assert bank_account.bank_account == "NL91ABNA0417164300"


def test_bank_account_initialization_invalid_no_validation():
    """Test the initialization of a BankAccount object with an invalid bank account number."""
    bank_account = BankAccount(bank_account="INVALID_ACCOUNT")
    assert bank_account.bank_account == "INVALID_ACCOUNT"


def test_bank_account_initialization_is_not_string():
    """Test the initialization of a BankAccount object with a non-string bank account number."""
    with pytest.raises(ValueError):
        BankAccount(bank_account=None)


def test_bank_account_get():
    """Test the get method of the BankAccount object."""
    bank_account = BankAccount(bank_account="NL91ABNA0417164300")
    assert bank_account.get() == "NL91ABNA0417164300"
