# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for the terminal response model."""

from multisafepay.api.paths.terminals.response.terminal import Terminal

TERMINAL_DATA = {
    "id": "term-001",
    "provider": "CTAP",
    "name": "My Terminal",
    "code": "T001",
    "created": "2024-01-01T00:00:00",
    "last_updated": "2024-06-01T00:00:00",
    "manufacturer_id": "MFR-123",
    "serial_number": "SN-456",
    "active": True,
    "group_id": 12345,
    "country": "NL",
}

EMPTY_TERMINAL_DATA = {field: None for field in TERMINAL_DATA}


def _assert_terminal_data(terminal: Terminal, expected: dict) -> None:
    """Assert terminal attributes against expected fixture data."""
    for field, expected_value in expected.items():
        assert getattr(terminal, field) == expected_value


def test_initializes_with_all_fields():
    """
    Test that the Terminal object initializes correctly with all fields.

    This test verifies that the Terminal object stores the correct values for
    all its attributes when instantiated with explicit data.
    """
    terminal = Terminal(**TERMINAL_DATA)

    _assert_terminal_data(terminal, TERMINAL_DATA)


def test_initializes_with_none_values():
    """
    Test that the Terminal object initializes correctly with None values.

    This test verifies that all attributes default to None when the Terminal
    object is instantiated without any arguments.
    """
    terminal = Terminal()

    _assert_terminal_data(terminal, EMPTY_TERMINAL_DATA)


def test_from_dict_creates_instance_from_dict():
    """
    Test that the from_dict method creates a Terminal from a valid dictionary.

    This test verifies that from_dict correctly maps all dictionary keys to
    the corresponding Terminal attributes.
    """
    terminal: Terminal | None = Terminal.from_dict(TERMINAL_DATA)

    assert terminal is not None
    _assert_terminal_data(terminal, TERMINAL_DATA)


def test_from_dict_returns_none_for_none_input():
    """
    Test that the from_dict method returns None when the input is None.

    This test verifies that from_dict returns None when None is provided
    as the input dictionary.
    """
    terminal = Terminal.from_dict(None)
    assert terminal is None


def test_from_dict_handles_missing_fields():
    """
    Test that the from_dict method handles missing fields by setting them to None.

    This test verifies that from_dict correctly creates a Terminal from a
    dictionary with missing fields, resulting in None values for those attributes.
    """
    data = {}
    terminal: Terminal | None = Terminal.from_dict(data)

    assert terminal is not None
    _assert_terminal_data(terminal, EMPTY_TERMINAL_DATA)
