# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Order section models for POS receipt response."""

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
        items_data = d.get("items")
        if isinstance(items_data, list):
            args["items"] = [
                ReceiptOrderItem.from_dict(item)
                for item in items_data
                if isinstance(item, dict)
            ]

        tip_data = d.get("tip")
        if isinstance(tip_data, list):
            args["tip"] = [
                ReceiptOrderTip.from_dict(tip)
                for tip in tip_data
                if isinstance(tip, dict)
            ]

        return ReceiptOrder(**args)
