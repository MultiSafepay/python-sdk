# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Terminal manager for `/json/terminals` operations."""

import json

from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.listings.listing_pager import ListingPager
from multisafepay.api.base.listings.pager import Pager
from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.terminals.request.create_terminal_request import (
    CreateTerminalRequest,
)
from multisafepay.api.paths.terminals.response.terminal import Terminal
from multisafepay.client.client import Client
from multisafepay.client.credential_resolver import AuthScope
from multisafepay.util.dict_utils import dict_empty
from multisafepay.util.message import MessageList, gen_could_not_created_msg
from pydantic import ValidationError

ALLOWED_OPTIONS = {
    "page": "",
    "limit": "",
}


class TerminalManager(AbstractManager):
    """A class representing the TerminalManager."""

    def __init__(self: "TerminalManager", client: Client) -> None:
        """
        Initialize the TerminalManager with a client.

        Parameters
        ----------
        client (Client): The client used to make API requests.

        """
        super().__init__(client)

    @staticmethod
    def __custom_terminal_response(response: ApiResponse) -> CustomApiResponse:
        args: dict = {
            **response.dict(),
            "data": None,
        }
        if not dict_empty(response.get_body_data()):
            try:
                args["data"] = Terminal.from_dict(
                    d=response.get_body_data().copy(),
                )
            except ValidationError:
                args["warnings"] = MessageList().add_message(
                    gen_could_not_created_msg("Terminal"),
                )

        return CustomApiResponse(**args)

    @staticmethod
    def __custom_terminal_listing_response(
        response: ApiResponse,
    ) -> CustomApiResponse:
        args: dict = {
            **response.dict(),
            "data": None,
        }

        pager = None
        raw_pager = response.get_pager()
        if isinstance(raw_pager, dict):
            pager = Pager.from_dict(raw_pager.copy())

        try:
            args["data"] = ListingPager(
                data=response.get_body_data().copy(),
                pager=pager,
                class_type=Terminal,
            )
        except (AttributeError, TypeError, ValidationError):
            args["warnings"] = MessageList().add_message(
                gen_could_not_created_msg("Listing Terminal"),
            )

        return CustomApiResponse(**args)

    def create_terminal(
        self: "TerminalManager",
        create_terminal_request: CreateTerminalRequest,
    ) -> CustomApiResponse:
        """
        Create a new POS terminal.

        Parameters
        ----------
        create_terminal_request (CreateTerminalRequest): Request payload.

        Returns
        -------
        CustomApiResponse: The response containing created terminal data.

        """
        json_data = json.dumps(create_terminal_request.to_dict())
        response = self.client.create_post_request(
            "json/terminals",
            request_body=json_data,
        )
        return TerminalManager.__custom_terminal_response(response)

    def get_terminals(
        self: "TerminalManager",
        options: dict = None,
    ) -> CustomApiResponse:
        """
        List POS terminals for the account.

        Parameters
        ----------
        options (dict): Request options (`page`, `limit`). Defaults to None.

        Returns
        -------
        CustomApiResponse: The response containing terminal listing data.

        """
        if options is None:
            options = {}
        options = {k: v for k, v in options.items() if k in ALLOWED_OPTIONS}

        response = self.client.create_get_request(
            "json/terminals",
            options,
            auth_scope=AuthScope(
                scope=Client.AUTH_SCOPE_PARTNER_AFFILIATE,
            ),
        )
        return TerminalManager.__custom_terminal_listing_response(response)
