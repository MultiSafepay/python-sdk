# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Order section model for POS receipt response."""

from typing import Optional

from multisafepay.api.paths.pos.receipt.response.components.order_item import (
    ReceiptOrderItem,
)
from multisafepay.api.paths.pos.receipt.response.components.order_tip import (
    ReceiptOrderTip,
)
from multisafepay.model.response_model import ResponseModel


class ReceiptOrder(ResponseModel):
    """Order information included in receipt data."""

    amount: Optional[int]
    amount_refunded: Optional[int]
    completed: Optional[str]
    created: Optional[str]
    currency: Optional[str]
    financial_status: Optional[str]
    modified: Optional[str]
    order_id: Optional[str]
    status: Optional[str]
    transaction_id: Optional[int]
    items: Optional[list[ReceiptOrderItem]]
    tip: Optional[list[ReceiptOrderTip]]

    @staticmethod
    def from_dict(d: dict) -> Optional["ReceiptOrder"]:
        """Create a ReceiptOrder from dictionary data."""
        if d is None:
            return None

        args = d.copy()
        for key, model in (
            ("items", ReceiptOrderItem),
            ("tip", ReceiptOrderTip),
        ):
            value = d.get(key)
            if isinstance(value, list):
                args[key] = [
                    model.from_dict(item)
                    for item in value
                    if isinstance(item, dict)
                ]

        return ReceiptOrder(**args)
