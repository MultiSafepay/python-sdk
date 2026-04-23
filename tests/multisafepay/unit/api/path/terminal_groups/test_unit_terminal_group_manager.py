# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for TerminalGroupManager.get_terminals_by_group behavior."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.terminal_groups.terminal_group_manager import (
    TerminalGroupManager,
)
from multisafepay.client.client import Client
from multisafepay.client.credential_resolver import AuthScope

TERMINAL_GROUP_ID = "42"


def _build_listing_api_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": [
                {
                    "terminal_id": "T-001",
                    "name": "POS Terminal 1",
                    "group_id": 42,
                    "active": True,
                    "status": "active",
                    "provider": "CTAP",
                },
            ],
            "pager": {
                "total": 1,
                "offset": 0,
                "limit": 10,
            },
        },
    )


def test_get_terminals_by_group_uses_partner_affiliate_scope() -> None:
    """Send partner_affiliate auth scope for terminal group listing."""
    client = MagicMock()
    client.create_get_request.return_value = _build_listing_api_response()

    manager = TerminalGroupManager(client)
    response = manager.get_terminals_by_group(
        terminal_group_id=TERMINAL_GROUP_ID,
    )

    called_auth_scope = client.create_get_request.call_args.kwargs[
        "auth_scope"
    ]

    assert isinstance(response, CustomApiResponse)
    assert called_auth_scope == AuthScope(
        scope=Client.AUTH_SCOPE_PARTNER_AFFILIATE,
    )


def test_get_terminals_by_group_encodes_group_id_in_endpoint() -> None:
    """Verify terminal_group_id is included in the URL path."""
    client = MagicMock()
    client.create_get_request.return_value = _build_listing_api_response()

    manager = TerminalGroupManager(client)
    manager.get_terminals_by_group(terminal_group_id=TERMINAL_GROUP_ID)

    called_endpoint = client.create_get_request.call_args.kwargs["endpoint"]
    assert TERMINAL_GROUP_ID in called_endpoint
    assert "json/terminal-groups/" in called_endpoint


def test_get_terminals_by_group_filters_options() -> None:
    """Only pass allowed options (page, limit) to the API."""
    client = MagicMock()
    client.create_get_request.return_value = _build_listing_api_response()

    manager = TerminalGroupManager(client)
    manager.get_terminals_by_group(
        terminal_group_id=TERMINAL_GROUP_ID,
        options={"page": 2, "limit": 5, "foo": "bar"},
    )

    called_params = client.create_get_request.call_args.kwargs["params"]
    assert called_params == {"page": 2, "limit": 5}


def test_get_terminals_by_group_defaults_empty_options() -> None:
    """Use empty options dict when no options are provided."""
    client = MagicMock()
    client.create_get_request.return_value = _build_listing_api_response()

    manager = TerminalGroupManager(client)
    manager.get_terminals_by_group(terminal_group_id=TERMINAL_GROUP_ID)

    called_params = client.create_get_request.call_args.kwargs["params"]
    assert called_params == {}
