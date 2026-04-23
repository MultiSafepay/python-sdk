# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for TerminalManager.create_terminal and get_terminals behavior."""

from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.terminals.request.create_terminal_request import (
    CreateTerminalRequest,
)
from multisafepay.api.paths.terminals.response.terminal import Terminal
from multisafepay.api.paths.terminals.terminal_manager import TerminalManager
from multisafepay.client.client import Client
from multisafepay.client.credential_resolver import AuthScope


def _build_terminal_api_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": {
                "terminal_id": "T-001",
                "name": "Demo POS Terminal",
                "group_id": 42,
                "active": True,
                "status": "active",
                "provider": "CTAP",
            },
        },
    )


def _build_listing_api_response() -> ApiResponse:
    return ApiResponse(
        headers={},
        status_code=200,
        body={
            "success": True,
            "data": [
                {
                    "terminal_id": "T-001",
                    "name": "Terminal 1",
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


def test_create_terminal_sends_post_to_correct_endpoint() -> None:
    """create_terminal posts to json/terminals with no auth scope."""
    client = MagicMock()
    client.create_post_request.return_value = _build_terminal_api_response()

    request = (
        CreateTerminalRequest()
        .add_provider("CTAP")
        .add_group_id(42)
        .add_name("Demo POS Terminal")
    )

    manager = TerminalManager(client)
    response = manager.create_terminal(request)

    called_endpoint = client.create_post_request.call_args.args[0]

    assert isinstance(response, CustomApiResponse)
    assert isinstance(response.get_data(), Terminal)
    assert response.get_data().terminal_id == "T-001"
    assert called_endpoint == "json/terminals"


def test_create_terminal_serializes_request_body() -> None:
    """Verify the request body is serialized as JSON."""
    client = MagicMock()
    client.create_post_request.return_value = _build_terminal_api_response()

    request = (
        CreateTerminalRequest()
        .add_provider("CTAP")
        .add_group_id(42)
        .add_name("Demo POS Terminal")
    )

    manager = TerminalManager(client)
    manager.create_terminal(request)

    called_body = client.create_post_request.call_args.kwargs["request_body"]
    assert '"provider": "CTAP"' in called_body
    assert '"group_id": 42' in called_body


def test_get_terminals_uses_partner_affiliate_scope() -> None:
    """get_terminals sends partner_affiliate auth scope."""
    client = MagicMock()
    client.create_get_request.return_value = _build_listing_api_response()

    manager = TerminalManager(client)
    response = manager.get_terminals(options={"page": 1, "limit": 10})

    called_auth_scope = client.create_get_request.call_args.kwargs.get(
        "auth_scope",
    )

    assert isinstance(response, CustomApiResponse)
    assert called_auth_scope == AuthScope(
        scope=Client.AUTH_SCOPE_PARTNER_AFFILIATE,
    )


def test_get_terminals_filters_options() -> None:
    """Only pass allowed options (page, limit) to the API."""
    client = MagicMock()
    client.create_get_request.return_value = _build_listing_api_response()

    manager = TerminalManager(client)
    manager.get_terminals(options={"page": 1, "limit": 5, "invalid": "x"})

    called_params = client.create_get_request.call_args.args[1]
    assert called_params == {"page": 1, "limit": 5}


def test_get_terminals_defaults_empty_options() -> None:
    """Use empty options dict when no options are provided."""
    client = MagicMock()
    client.create_get_request.return_value = _build_listing_api_response()

    manager = TerminalManager(client)
    manager.get_terminals()

    called_params = client.create_get_request.call_args.args[1]
    assert called_params == {}
