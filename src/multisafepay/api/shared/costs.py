# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Transaction costs model for handling fees and charges in payment processing."""

from decimal import Decimal
from typing import Optional, Type, Union

from multisafepay.model.api_model import ApiModel
from pydantic import validator


class Costs(ApiModel):
    """
    A class to represent the costs associated with a transaction.

    Attributes
    ----------
    transaction_id (Optional[int]): The ID of the transaction.
    description (Optional[str]): The description of the cost.
    type (Optional[str]): The type of the cost.
    amount (Optional[Decimal]): The amount of the cost as a precise Decimal value.
    currency (Optional[str]): The currency of the cost.
    status (Optional[str]): The status of the cost.

    """

    transaction_id: Optional[int]
    description: Optional[str]
    type: Optional[str]
    amount: Optional[Decimal]
    currency: Optional[str]
    status: Optional[str]

    @validator("amount", pre=True)
    def convert_amount_to_decimal(
        cls: Type["Costs"],
        value: Union[str, float, Decimal, None],
    ) -> Optional[Decimal]:
        """
        Convert amount to Decimal for precise monetary calculations.

        Parameters
        ----------
        value (Union[str, int, float, Decimal, None]): The value to convert.

        Returns
        -------
        Optional[Decimal]: The converted Decimal value or None.

        """
        if value is None:
            return None
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))

    def add_transaction_id(self: "Costs", transaction_id: int) -> "Costs":
        """
        Add a transaction ID to the Costs instance.

        Parameters
        ----------
        transaction_id (int): The ID of the transaction.

        Returns
        -------
        Costs: The updated Costs instance.

        """
        self.transaction_id = transaction_id
        return self

    def add_description(self: "Costs", description: str) -> "Costs":
        """
        Add a description to the Costs instance.

        Parameters
        ----------
        description (str): The description of the cost.

        Returns
        -------
        Costs: The updated Costs instance.

        """
        self.description = description
        return self

    def add_type(self: "Costs", type_: str) -> "Costs":
        """
        Add a type to the Costs instance.

        Parameters
        ----------
        type_ (str): The type of the cost.

        Returns
        -------
        Costs: The updated Costs instance.

        """
        self.type = type_
        return self

    def add_amount(
        self: "Costs",
        amount: Union[Decimal, float, str],
    ) -> "Costs":
        """
        Add an amount to the Costs instance with precise Decimal conversion.

        Parameters
        ----------
        amount (Union[Decimal, float, int, str]): The amount of the cost.

        Returns
        -------
        Costs: The updated Costs instance.

        """
        if isinstance(amount, Decimal):
            self.amount = amount
        else:
            self.amount = Decimal(str(amount))
        return self

    def add_currency(self: "Costs", currency: str) -> "Costs":
        """
        Add a currency to the Costs instance.

        Parameters
        ----------
        currency (str): The currency of the cost.

        Returns
        -------
        Costs: The updated Costs instance.

        """
        self.currency = currency
        return self

    def add_status(self: "Costs", status: str) -> "Costs":
        """
        Add a status to the Costs instance.

        Parameters
        ----------
        status (str): The status of the cost.

        Returns
        -------
        Costs: The updated Costs instance.

        """
        self.status = status
        return self

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["Costs"]:
        """
        Create a Costs instance from a dictionary.

        Parameters
        ----------
        d (Optional[dict]): A dictionary containing the cost details.

        Returns
        -------
        Optional[Costs]: A Costs instance if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        return Costs(**d)
