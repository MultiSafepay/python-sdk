# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Order item model for POS receipt response."""

from typing import Optional

from multisafepay.model.response_model import ResponseModel


class ReceiptOrderItem(ResponseModel):
    """Represents one printed order item on the receipt."""

    currency: Optional[str]
    item_price: Optional[int]
    name: Optional[str]
    quantity: Optional[int]
    unit_price: Optional[int]

    @staticmethod
    def from_dict(d: dict) -> Optional["ReceiptOrderItem"]:
        """Create a ReceiptOrderItem from dictionary data."""
        if d is None:
            return None
        return ReceiptOrderItem(**d)
