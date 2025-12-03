# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.gateway_info.wallet import (
    Wallet,
)


def test_initializes_wallet_correctly():
    """Test that the Wallet object is initialized correctly with a given payment_token."""
    wallet = Wallet(payment_token="token123")

    assert wallet.payment_token == "token123"


def test_initializes_wallet_with_empty_value():
    """Test that the Wallet object is initialized correctly with an empty value."""
    wallet = Wallet()

    assert wallet.payment_token is None


def test_add_payment_token_updates_value():
    """Test that the add_payment_token method updates the payment_token attribute to the given value."""
    wallet = Wallet()
    wallet_updated = wallet.add_payment_token("token123")

    assert wallet.payment_token == "token123"
    assert isinstance(wallet_updated, Wallet)
