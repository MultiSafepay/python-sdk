# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Destination holder model for gateway-specific destination account information."""

from typing import Optional, Union

from multisafepay.model.request_model import RequestModel
from multisafepay.value_object.country import Country
from multisafepay.value_object.iban_number import IbanNumber


class DestinationHolder(RequestModel):
    """
    Represents a destination holder with various attributes.

    Attributes
    ----------
    name (Optional[str]): The name of the destination holder.
    city (Optional[str]): The city of the destination holder.
    country (Optional[str]): The country of the destination holder.
    iban (Optional[str]): The IBAN of the destination holder.
    swift (Optional[str]): The SWIFT code of the destination holder.

    """

    name: Optional[str]
    city: Optional[str]
    country: Optional[str]
    iban: Optional[str]
    swift: Optional[str]

    def add_name(
        self: "DestinationHolder",
        name: Optional[str],
    ) -> "DestinationHolder":
        """
        Adds a name to the destination holder.

        Parameters
        ----------
        name (Optional[str]): The name to add.

        Returns
        -------
        DestinationHolder: The updated destination holder.

        """
        self.name = name
        return self

    def add_city(
        self: "DestinationHolder",
        city: Optional[str],
    ) -> "DestinationHolder":
        """
        Adds a city to the destination holder.

        Parameters
        ----------
        city (Optional[str]): The city to add.

        Returns
        -------
        DestinationHolder: The updated destination holder.

        """
        self.city = city
        return self

    def add_country(
        self: "DestinationHolder",
        country: Optional[Union[Country, str]],
    ) -> "DestinationHolder":
        """
        Adds a country to the destination holder.

        Parameters
        ----------
        country (Optional[Country | str]): The country to add. Can be a Country object or a string.

        Returns
        -------
        DestinationHolder: The updated destination holder.

        """
        if isinstance(country, str):
            country = Country(code=country)
        self.country = country.get_code() if country is not None else None
        return self

    def add_iban(
        self: "DestinationHolder",
        iban: Optional[Union[IbanNumber, str]],
    ) -> "DestinationHolder":
        """
        Adds an IBAN to the destination holder.

        Parameters
        ----------
        iban (Optional[IbanNumber | str]): The IBAN to add. Can be an IbanNumber object or a string.

        Returns
        -------
        DestinationHolder: The updated destination holder.

        """
        if isinstance(iban, str):
            iban = IbanNumber(iban_number=iban)
        self.iban = iban.get() if iban is not None else None
        return self

    def add_swift(
        self: "DestinationHolder",
        swift: Optional[str],
    ) -> "DestinationHolder":
        """
        Adds a SWIFT code to the destination holder.

        Parameters
        ----------
        swift (Optional[str]): The SWIFT code to add.

        Returns
        -------
        DestinationHolder: The updated destination holder.

        """
        self.swift = swift
        return self
