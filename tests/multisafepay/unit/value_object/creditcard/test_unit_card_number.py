# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.value_object.creditcard.card_number import CardNumber


def test_card_number_initialization_valid():
    """
    Test the initialization of a CardNumber object with a valid card number.

    Raises
    ------
    AssertionError
        If the card number does not match the expected value.

    """
    card_number = CardNumber(card_number="1234567812345678")
    assert card_number.card_number == "1234567812345678"


def test_card_number_get():
    """
    Test the get_card_number method of the CardNumber object.

    Raises
    ------
    AssertionError
        If the returned card number does not match the expected value.

    """
    card_number = CardNumber(card_number="1234567812345678")
    assert card_number.get_card_number() == "1234567812345678"
