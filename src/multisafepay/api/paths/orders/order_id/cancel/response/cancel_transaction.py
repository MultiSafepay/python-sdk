# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Response model for order cancellation endpoint payload."""

from typing import Optional

from multisafepay.api.base.decorator import Decorator
from multisafepay.api.paths.orders.response.components.payment_details import (
    PaymentDetails,
)
from multisafepay.api.shared.costs import Costs
from multisafepay.api.shared.custom_info import CustomInfo
from multisafepay.api.shared.customer import Customer
from multisafepay.api.shared.payment_method import PaymentMethod
from multisafepay.model.response_model import ResponseModel


class CancelTransaction(ResponseModel):
    """
    Represents the `data` payload returned by cancel order transaction.

    Attributes
    ----------
    costs (Optional[list[Costs]]): The costs of the order.
    created (Optional[str]): Creation timestamp.
    modified (Optional[str]): Last modification timestamp.
    custom_info (Optional[CustomInfo]): Additional custom info.
    customer (Optional[Customer]): The customer data.
    fastcheckout (Optional[str]): Fastcheckout flag/status.
    financial_status (Optional[str]): Financial status.
    items (Optional[str]): Rendered items payload.
    payment_details (Optional[PaymentDetails]): Payment details.
    payment_methods (Optional[list[PaymentMethod]]): Payment methods.
    status (Optional[str]): Order status.

    """

    costs: Optional[list[Costs]]
    created: Optional[str]
    modified: Optional[str]
    custom_info: Optional[CustomInfo]
    customer: Optional[Customer]
    fastcheckout: Optional[str]
    financial_status: Optional[str]
    items: Optional[str]
    payment_details: Optional[PaymentDetails]
    payment_methods: Optional[list[PaymentMethod]]
    status: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["CancelTransaction"]:
        """
        Create a CancelTransaction from dictionary data.

        Parameters
        ----------
        d (dict): The cancellation response data.

        Returns
        -------
        Optional[CancelTransaction]: A cancellation response instance or None.

        """
        if d is None:
            return None
        cancel_dependency_adapter = Decorator(dependencies=d)
        dependencies = (
            cancel_dependency_adapter.adapt_costs(d.get("costs"))
            .adapt_custom_info(d.get("custom_info"))
            .adapt_payment_details(d.get("payment_details"))
            .adapt_payment_methods(d.get("payment_methods"))
            .get_dependencies()
        )
        return CancelTransaction(**dependencies)
