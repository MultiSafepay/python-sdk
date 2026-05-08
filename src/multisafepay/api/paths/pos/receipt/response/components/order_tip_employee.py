# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Tip employee model for POS receipt response."""

from typing import Optional

from multisafepay.model.response_model import ResponseModel


class ReceiptOrderTipEmployee(ResponseModel):
    """Employee info for receipt tip section."""

    id: Optional[str]
    name: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["ReceiptOrderTipEmployee"]:
        """Create a ReceiptOrderTipEmployee from dictionary data."""
        if d is None:
            return None
        return ReceiptOrderTipEmployee(**d)
