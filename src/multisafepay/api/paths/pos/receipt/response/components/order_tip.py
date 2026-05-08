# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Tip model for POS receipt response."""

from typing import Optional

from multisafepay.api.paths.pos.receipt.response.components.order_tip_employee import (
    ReceiptOrderTipEmployee,
)
from multisafepay.model.response_model import ResponseModel


class ReceiptOrderTip(ResponseModel):
    """Tip information on the printed receipt."""

    amount: Optional[int]
    employee: Optional[list[ReceiptOrderTipEmployee]]

    @staticmethod
    def from_dict(d: dict) -> Optional["ReceiptOrderTip"]:
        """Create a ReceiptOrderTip from dictionary data."""
        if d is None:
            return None

        args = d.copy()
        employee_data = d.get("employee")
        if isinstance(employee_data, list):
            args["employee"] = [
                ReceiptOrderTipEmployee.from_dict(employee)
                for employee in employee_data
                if isinstance(employee, dict)
            ]

        return ReceiptOrderTip(**args)
