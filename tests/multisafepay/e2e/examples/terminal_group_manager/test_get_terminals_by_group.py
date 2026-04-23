# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""E2E coverage for examples/terminal_group_manager/get_terminals_by_group.py."""

import pytest

from multisafepay.api.base.listings.listing_pager import ListingPager
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.terminal_groups.terminal_group_manager import (
    TerminalGroupManager,
)
from multisafepay.sdk import Sdk


@pytest.fixture(scope="module")
def terminal_group_manager(terminals_sdk: Sdk) -> TerminalGroupManager:
    """Fixture that provides a TerminalGroupManager instance for testing."""
    return terminals_sdk.get_terminal_group_manager()


def test_get_terminals_by_group(
    terminal_group_manager: TerminalGroupManager,
    terminals_group_id: str,
) -> None:
    """List terminals for a specific group using the example template flow."""
    response = terminal_group_manager.get_terminals_by_group(
        terminal_group_id=terminals_group_id,
        options={
            "limit": 10,
            "page": 1,
        },
    )

    assert isinstance(response, CustomApiResponse)
    assert response.get_status_code() == 200
    assert response.get_body_success() is True
    assert isinstance(response.get_data(), ListingPager)
