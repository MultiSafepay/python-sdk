# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for the terminal create request model."""

import pytest

from multisafepay.api.paths.terminals.request.create_terminal_request import (
    CTAP_PROVIDER,
    CreateTerminalRequest,
)
from multisafepay.exception.invalid_argument import InvalidArgumentException


def test_initializes_with_default_values() -> None:
    """Initialize request model with empty/default values."""
    request = CreateTerminalRequest()

    assert request.provider is None
    assert request.group_id is None
    assert request.name is None


def test_add_provider_updates_value() -> None:
    """Store a valid provider and return the current request object."""
    request = CreateTerminalRequest()

    returned = request.add_provider(CTAP_PROVIDER)

    assert request.provider == CTAP_PROVIDER
    assert returned is request


def test_add_provider_raises_for_invalid_provider() -> None:
    """Reject provider values that are not whitelisted."""
    request = CreateTerminalRequest()

    with pytest.raises(InvalidArgumentException, match="not a known provider"):
        request.add_provider("UNKNOWN")


def test_add_group_id_updates_value() -> None:
    """Store terminal group id and return current request object."""
    request = CreateTerminalRequest()

    returned = request.add_group_id("1234")

    assert request.group_id == "1234"
    assert returned is request


def test_add_name_updates_value() -> None:
    """Store terminal display name and return current request object."""
    request = CreateTerminalRequest()

    returned = request.add_name("Demo POS Terminal")

    assert request.name == "Demo POS Terminal"
    assert returned is request
