# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""E2E coverage for examples/terminal_manager/get_terminals.py."""

import pytest

from multisafepay.api.base.listings.listing_pager import ListingPager
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.terminals.terminal_manager import TerminalManager
from multisafepay.sdk import Sdk


@pytest.fixture(scope="module")
def terminal_manager(terminals_sdk: Sdk) -> TerminalManager:
    """Fixture that provides a TerminalManager instance for testing."""
    return terminals_sdk.get_terminal_manager()


def test_get_terminals(terminal_manager: TerminalManager) -> None:
    """List terminals using the same flow as the terminal manager example."""
    response = terminal_manager.get_terminals(
        options={
            "limit": 10,
            "page": 1,
        },
    )

    assert isinstance(response, CustomApiResponse)
    assert response.get_status_code() == 200
    assert response.get_body_success() is True
    assert isinstance(response.get_data(), ListingPager)
