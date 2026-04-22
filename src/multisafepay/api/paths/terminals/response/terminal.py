# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Response model for POS terminal data."""

from typing import Optional

from multisafepay.model.response_model import ResponseModel


class Terminal(ResponseModel):
    """
    Represents a POS terminal returned by the API.

    Attributes
    ----------
    id (Optional[str]): The terminal identifier.
    provider (Optional[str]): The terminal provider.
    name (Optional[str]): The terminal name.
    code (Optional[str]): The terminal code.
    created (Optional[str]): Terminal creation timestamp.
    last_updated (Optional[str]): Terminal update timestamp.
    manufacturer_id (Optional[str]): Terminal manufacturer identifier.
    serial_number (Optional[str]): Terminal serial number.
    active (Optional[bool]): Whether the terminal is active.
    group_id (Optional[int]): The terminal group identifier.
    country (Optional[str]): The terminal country code.

    """

    id: Optional[str]
    provider: Optional[str]
    name: Optional[str]
    code: Optional[str]
    created: Optional[str]
    last_updated: Optional[str]
    manufacturer_id: Optional[str]
    serial_number: Optional[str]
    active: Optional[bool]
    group_id: Optional[int]
    country: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["Terminal"]:
        """
        Create a Terminal from dictionary data.

        Parameters
        ----------
        d (dict): The terminal data.

        Returns
        -------
        Optional[Terminal]: A terminal instance or None.

        """
        if d is None:
            return None
        return Terminal(**d)
