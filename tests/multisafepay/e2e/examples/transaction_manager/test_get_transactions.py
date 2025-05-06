# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import os
import pytest
from dotenv import load_dotenv
from multisafepay.api.base.listings.listing_pager import ListingPager

from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.transactions.response.transaction import (
    Transaction,
)
from multisafepay.api.paths.transactions.transaction_manager import (
    TransactionManager,
)
from multisafepay.sdk import Sdk


@pytest.fixture(scope="module")
def transaction_manager():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    multisafepay_sdk = Sdk(api_key, False)
    return multisafepay_sdk.get_transaction_manager()


def test_retrieves_all_transactions(transaction_manager: TransactionManager):
    """
    Test the get_transactions method of the TransactionManager.

    This test checks if the list of transactions is retrieved successfully and each item is of the correct type.

    """
    transaction_response = transaction_manager.get_transactions()
    transactions = transaction_response.get_data()

    assert isinstance(transaction_response, CustomApiResponse)
    assert isinstance(transactions, ListingPager)
    assert all(
        isinstance(transaction, Transaction) for transaction in transactions
    )
