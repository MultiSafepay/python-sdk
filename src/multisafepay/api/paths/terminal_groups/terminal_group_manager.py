# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Terminal group manager for `/json/terminal-groups/{terminal_group_id}/terminals`."""

from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.listings.listing_pager import ListingPager
from multisafepay.api.base.listings.pager import Pager
from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.terminals.response.terminal import Terminal
from multisafepay.client.client import Client
from multisafepay.client.credential_resolver import AuthScope
from multisafepay.util.message import MessageList, gen_could_not_created_msg
from pydantic import ValidationError

ALLOWED_OPTIONS = {
    "page": "",
    "limit": "",
}


class TerminalGroupManager(AbstractManager):
    """A class representing the TerminalGroupManager."""

    def __init__(self: "TerminalGroupManager", client: Client) -> None:
        """
        Initialize the TerminalGroupManager with a client.

        Parameters
        ----------
        client (Client): The client used to make API requests.

        """
        super().__init__(client)

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

    def get_terminals_by_group(
        self: "TerminalGroupManager",
        terminal_group_id: str,
        options: dict = None,
    ) -> CustomApiResponse:
        """
        List POS terminals for the given terminal group.

        Parameters
        ----------
        terminal_group_id (str): Terminal group identifier.
        options (dict): Request options (`page`, `limit`). Defaults to None.

        Returns
        -------
        CustomApiResponse: The response containing terminal listing data.

        """
        if options is None:
            options = {}
        options = {k: v for k, v in options.items() if k in ALLOWED_OPTIONS}

        encoded_terminal_group_id = self.encode_path_segment(terminal_group_id)
        endpoint = (
            f"json/terminal-groups/{encoded_terminal_group_id}/terminals"
        )
        context = {"terminal_group_id": terminal_group_id}
        response = self.client.create_get_request(
            endpoint=endpoint,
            params=options,
            context=context,
            auth_scope=AuthScope(
                scope=Client.AUTH_SCOPE_PARTNER_AFFILIATE,
            ),
        )
        return TerminalGroupManager.__custom_terminal_listing_response(
            response,
        )
