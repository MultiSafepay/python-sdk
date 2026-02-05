# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""DecimalAmount value object for monetary amounts."""

from decimal import Decimal
from typing import Type, Union

from multisafepay.model.inmutable_model import InmutableModel
from pydantic import validator


class DecimalAmount(InmutableModel):
    """
    A class to represent a monetary amount with decimal precision.

    Attributes
    ----------
    amount (Decimal): The amount as a precise decimal value.

    """

    amount: Decimal

    @validator("amount", pre=True)
    def convert_to_decimal(
        cls: Type["DecimalAmount"],
        value: Union[str, float, int, Decimal],
    ) -> Decimal:
        """
        Convert the input value to Decimal for precise calculations.

        Parameters
        ----------
        value (Union[str, float, int, Decimal]): The value to convert.

        Returns
        -------
        Decimal: The converted Decimal value.

        Raises
        ------
        TypeError: If the value cannot be converted to Decimal.

        """
        if isinstance(value, Decimal):
            return value
        if not isinstance(value, (str, float, int)):
            raise TypeError(
                f"Cannot convert {type(value).__name__} to Decimal",
            )
        return Decimal(str(value))

    def get(self: "DecimalAmount") -> Decimal:
        """
        Get the monetary amount.

        Returns
        -------
        Decimal: The amount.

        """
        return self.amount
