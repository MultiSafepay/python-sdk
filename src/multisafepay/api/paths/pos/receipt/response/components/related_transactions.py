# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Related transactions section model for POS receipt response."""

from typing import Optional

from multisafepay.model.response_model import ResponseModel


class ReceiptRelatedTransactions(ResponseModel):
    """Represents related transaction data returned for a receipt."""

    amount: Optional[int]
    created: Optional[str]
    currency: Optional[str]
    description: Optional[str]
    items: Optional[str]
    modified: Optional[str]
    order_id: Optional[str]
    reference_transaction_id: Optional[int]
    status: Optional[str]
    transaction_id: Optional[int]
    type: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["ReceiptRelatedTransactions"]:
        """Create a ReceiptRelatedTransactions model from dictionary data."""
        if d is None:
            return None

        return ReceiptRelatedTransactions(**d)
