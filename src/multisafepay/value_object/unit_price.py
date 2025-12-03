# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit price value object for item pricing in shopping carts."""

from decimal import Decimal
from typing import Type, Union

from multisafepay.model.inmutable_model import InmutableModel
from pydantic import validator


class UnitPrice(InmutableModel):
    """
    A class to represent the unit price of an item.

    Attributes
    ----------
    unit_price (Decimal): The unit price of the item as a precise decimal value.

    """

    unit_price: Decimal

    @validator("unit_price", pre=True)
    def convert_to_decimal(
        cls: Type["UnitPrice"],
        value: Union[str, float, Decimal],
    ) -> Decimal:
        """
        Convert the input value to Decimal for precise calculations.

        Parameters
        ----------
        value (Union[str, float, Decimal]): The value to convert.

        Returns
        -------
        Decimal: The converted Decimal value.

        Raises
        ------
        TypeError: If the value cannot be converted to Decimal.

        """
        if isinstance(value, Decimal):
            return value
        if not isinstance(value, (str, float)):
            raise TypeError(
                f"Cannot convert {type(value).__name__} to Decimal",
            )
        return Decimal(str(value))

    def get(self: "UnitPrice") -> Decimal:
        """
        Get the unit price of the item.

        Returns
        -------
        Decimal: The unit price of the item.

        """
        return self.unit_price
