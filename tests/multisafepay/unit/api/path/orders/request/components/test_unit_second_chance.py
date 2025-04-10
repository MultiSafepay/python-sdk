# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.paths.orders.request.components.second_chance import (
    SecondChance,
)


def initializes_second_chance_correctly():
    """
    Tests that the SecondChance object is initialized correctly with the given value.
    """
    second_chance = SecondChance(send_email=True)

    assert second_chance.send_email is True


def initializes_second_chance_with_default_values():
    """
    Tests that the SecondChance object is initialized with the default value when no arguments are provided.
    """
    second_chance = SecondChance()

    assert second_chance.send_email is False


def add_send_email_updates_value():
    """
    Tests that the add_send_email method updates the send_email field to True.
    """
    second_chance = SecondChance()
    second_chance_updated = second_chance.add_send_email(True)

    assert second_chance.send_email is True
    assert isinstance(second_chance_updated, SecondChance)


def add_send_email_updates_value_to_false():
    """
    Tests that the add_send_email method updates the send_email field to False.
    """
    second_chance = SecondChance(send_email=True)
    second_chance_updated = second_chance.add_send_email(False)

    assert second_chance.send_email is False
    assert isinstance(second_chance_updated, SecondChance)
