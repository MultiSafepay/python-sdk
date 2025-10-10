# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.gateway_info.terminal import (
    Terminal,
)


def test_initializes_terminal_correctly():
    """
    Test that the Terminal object is initialized correctly with a given terminal_id.
    """
    terminal = Terminal(terminal_id="12345")

    assert terminal.terminal_id == "12345"


def test_initializes_terminal_with_empty_value():
    """
    Test that the Terminal object is initialized correctly with an empty value.
    """
    terminal = Terminal()

    assert terminal.terminal_id is None


def test_add_terminal_id_updates_value():
    """
    Test that the add_terminal_id method updates the terminal_id attribute to the given value.
    """
    terminal = Terminal()
    terminal_updated = terminal.add_terminal_id("12345")

    assert terminal.terminal_id == "12345"
    assert isinstance(terminal_updated, Terminal)


def test_add_terminal_id_with_empty_string():
    """
    Test that the add_terminal_id method updates the terminal_id attribute to an empty string.
    """
    terminal = Terminal()
    terminal_updated = terminal.add_terminal_id("")

    assert terminal.terminal_id == ""
    assert isinstance(terminal_updated, Terminal)
