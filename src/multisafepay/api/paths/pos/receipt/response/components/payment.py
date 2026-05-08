# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Payment section model for POS receipt response."""

from typing import Optional

from multisafepay.model.response_model import ResponseModel


class ReceiptPayment(ResponseModel):
    """Payment information included in receipt data."""

    application_id: Optional[str]
    authorization_code: Optional[int]
    card_acceptor_location: Optional[str]
    card_entry_mode: Optional[str]
    card_expiry_date: Optional[str]
    cardholder_verification_method: Optional[str]
    issuer_bin: Optional[str]
    issuer_country_code: Optional[str]
    last4: Optional[str]
    payment_method: Optional[str]
    response_code: Optional[str]
    terminal_id: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["ReceiptPayment"]:
        """Create a ReceiptPayment model from dictionary data."""
        if d is None:
            return None
        return ReceiptPayment(**d)
