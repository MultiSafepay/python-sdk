# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""POS manager for `/json/pos/...` endpoints."""

from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.pos.receipt.response.receipt import Receipt
from multisafepay.client.client import Client
from multisafepay.client.credential_resolver import (
    AuthScope,
    ScopedCredentialResolver,
)
from multisafepay.util.dict_utils import dict_empty
from multisafepay.util.message import MessageList, gen_could_not_created_msg
from pydantic import ValidationError


class PosManager(AbstractManager):
    """A class representing the PosManager."""

    def __init__(self: "PosManager", client: Client) -> None:
        """
        Initialize the PosManager with a client.

        Parameters
        ----------
        client (Client): The client used to make API requests.

        """
        super().__init__(client)

    @staticmethod
    def __custom_receipt_response(response: ApiResponse) -> CustomApiResponse:
        args: dict = {
            **response.dict(),
            "data": None,
        }
        if not dict_empty(response.get_body_data()):
            try:
                args["data"] = Receipt.from_dict(
                    d=response.get_body_data().copy(),
                )
            except ValidationError:
                args["warnings"] = MessageList().add_message(
                    gen_could_not_created_msg("Receipt"),
                )

        return CustomApiResponse(**args)

    def get_receipt(
        self: "PosManager",
        order_id: str,
        terminal_group_id: str = None,
    ) -> CustomApiResponse:
        """
        Retrieve receipt data for a POS transaction.

        Parameters
        ----------
        order_id (str): Order identifier.
        terminal_group_id (str): Optional terminal group identifier for
            scoped auth.

        Returns
        -------
        CustomApiResponse: The response containing receipt data.

        """
        encoded_order_id = self.encode_path_segment(order_id)
        endpoint = f"json/pos/receipt/{encoded_order_id}"
        context = {"order_id": order_id}
        response = self.client.create_get_request(
            endpoint,
            context=context,
            auth_scope=(
                AuthScope(
                    scope=ScopedCredentialResolver.AUTH_SCOPE_TERMINAL_GROUP,
                    group_id=terminal_group_id,
                )
                if terminal_group_id
                else None
            ),
        )
        return PosManager.__custom_receipt_response(response)
