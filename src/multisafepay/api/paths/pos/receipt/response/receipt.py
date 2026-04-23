# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Response model for POS receipt data."""

from typing import Optional

from multisafepay.api.paths.pos.receipt.response.components.merchant import (
    ReceiptMerchant,
)
from multisafepay.api.paths.pos.receipt.response.components.order import (
    ReceiptOrder,
)
from multisafepay.api.paths.pos.receipt.response.components.payment import (
    ReceiptPayment,
)
from multisafepay.api.paths.pos.receipt.response.components.related_transactions import (
    ReceiptRelatedTransactions,
)
from multisafepay.model.response_model import ResponseModel


class Receipt(ResponseModel):
    """
    Represents receipt payload data returned by the POS receipt endpoint.

    Attributes
    ----------
    merchant (Optional[ReceiptMerchant]): Information about the merchant.
    order (Optional[ReceiptOrder]): Information about the order.
    payment (Optional[ReceiptPayment]): Information about the payment.
    printed_on (Optional[str]): Timestamp when the receipt was printed.
    related_transactions (Optional[ReceiptRelatedTransactions]): Linked transaction information.

    """

    merchant: Optional[ReceiptMerchant]
    order: Optional[ReceiptOrder]
    payment: Optional[ReceiptPayment]
    printed_on: Optional[str]
    related_transactions: Optional[ReceiptRelatedTransactions]

    @staticmethod
    def from_dict(d: dict) -> Optional["Receipt"]:
        """
        Create a Receipt from dictionary data.

        Parameters
        ----------
        d (dict): The receipt data.

        Returns
        -------
        Optional[Receipt]: A receipt instance or None.

        """
        if d is None:
            return None

        args = d.copy()
        if isinstance(d.get("merchant"), dict):
            args["merchant"] = ReceiptMerchant.from_dict(d.get("merchant"))
        if isinstance(d.get("order"), dict):
            args["order"] = ReceiptOrder.from_dict(d.get("order"))
        if isinstance(d.get("payment"), dict):
            args["payment"] = ReceiptPayment.from_dict(d.get("payment"))
        if isinstance(d.get("related_transactions"), dict):
            args["related_transactions"] = (
                ReceiptRelatedTransactions.from_dict(
                    d.get("related_transactions"),
                )
            )

        return Receipt(**args)
