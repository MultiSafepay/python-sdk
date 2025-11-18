# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Customer data model for order and payment customer information."""

from typing import Optional, Union

from multisafepay.api.shared.delivery import Delivery
from multisafepay.value_object.ip_address import IpAddress


class Customer(Delivery):
    """
    A class to represent a customer, inheriting from Delivery.

    Attributes
    ----------
    locale (Optional[str]): The locale of the customer.
    ip_address (Optional[str]): The IP address of the customer.
    forwarded_ip (Optional[str]): The forwarded IP address of the customer.
    referrer (Optional[str]): The referrer URL.
    user_agent (Optional[str]): The user agent string.

    """

    locale: Optional[str]
    ip_address: Optional[str]
    forwarded_ip: Optional[str]
    referrer: Optional[str]
    user_agent: Optional[str]
    reference: Optional[str]

    def add_locale(self: "Customer", locale: Optional[str]) -> "Customer":
        """
        Add a locale to the customer.

        Parameters
        ----------
        locale (Optional[str]): The locale to add.

        Returns
        -------
        Customer: The updated Customer instance.

        """
        self.locale = locale
        return self

    def add_ip_address(
        self: "Customer",
        ip_address: Optional[Union[IpAddress, str]],
    ) -> "Customer":
        """
        Add an IP address to the customer.

        Parameters
        ----------
        ip_address (Optional[IpAddress] | str): The IP address to add.

        Returns
        -------
        Customer: The updated Customer instance.

        """
        if isinstance(ip_address, str):
            ip_address = IpAddress(ip_address=ip_address)
        self.ip_address = ip_address.get() if ip_address is not None else None
        return self

    def add_forwarded_ip(
        self: "Customer",
        forwarded_ip: Optional[Union[IpAddress, str]],
    ) -> "Customer":
        """
        Add a forwarded IP address to the customer.

        Parameters
        ----------
        forwarded_ip (Optional[IpAddress] | str): The forwarded IP address to add.

        Returns
        -------
        Customer: The updated Customer instance.

        """
        if isinstance(forwarded_ip, str):
            forwarded_ip = IpAddress(ip_address=forwarded_ip)
        self.forwarded_ip = (
            forwarded_ip.get() if forwarded_ip is not None else None
        )
        return self

    def add_referrer(self: "Customer", referrer: Optional[str]) -> "Customer":
        """
        Add a referrer URL to the customer.

        Parameters
        ----------
        referrer (Optional[str]): The referrer URL to add.

        Returns
        -------
        Customer: The updated Customer instance.

        """
        self.referrer = referrer
        return self

    def add_user_agent(
        self: "Customer",
        user_agent: Optional[str],
    ) -> "Customer":
        """
        Add a user agent string to the customer.

        Parameters
        ----------
        user_agent (Optional[str]): The user agent string to add.

        Returns
        -------
        Customer: The updated Customer instance.

        """
        self.user_agent = user_agent
        return self

    def add_reference(
        self: "Customer",
        reference: Optional[str],
    ) -> "Customer":
        """
        Add a reference to the customer.

        Parameters
        ----------
        reference (Optional[str]): The reference to add.

        Returns
        -------
        Customer: The updated Customer instance.

        """
        self.reference = reference
        return self

    @staticmethod
    def from_dict(d: dict) -> Optional["Customer"]:
        """
        Create a Customer instance from a dictionary.

        Parameters
        ----------
        d (dict): A dictionary containing the customer details.

        Returns
        -------
        Optional[Customer]: A Customer instance if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        return Customer(**d)
