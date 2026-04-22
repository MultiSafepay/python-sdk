# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Request model for cancel transaction endpoint."""

from multisafepay.model.request_model import RequestModel


class CancelTransactionRequest(RequestModel):
    """
    Represents a request to cancel a POS transaction.

    Attributes
    ----------
    order_id (str): The order identifier used in the endpoint path.

    """

    order_id: str

    def add_order_id(
        self: "CancelTransactionRequest",
        order_id: str,
    ) -> "CancelTransactionRequest":
        """
        Adds order id to the cancellation request.

        Parameters
        ----------
        order_id (str): The order identifier.

        Returns
        -------
        CancelTransactionRequest: The updated request instance.

        """
        self.order_id = order_id
        return self
