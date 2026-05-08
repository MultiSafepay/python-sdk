# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Merchant section for POS receipt response."""

from typing import Optional

from multisafepay.model.response_model import ResponseModel


class ReceiptMerchant(ResponseModel):
    """Merchant information included in receipt data."""

    name: Optional[str]
    address: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["ReceiptMerchant"]:
        """Create a ReceiptMerchant model from dictionary data."""
        if d is None:
            return None
        return ReceiptMerchant(**d)
