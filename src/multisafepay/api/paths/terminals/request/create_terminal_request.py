# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Request model for creating POS terminals."""

from typing import Optional

from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.model.request_model import RequestModel

CTAP_PROVIDER = "CTAP"
ALLOWED_PROVIDERS = [
    CTAP_PROVIDER,
]


class CreateTerminalRequest(RequestModel):
    """
    Request body for the create terminal endpoint.

    Attributes
    ----------
    provider (Optional[str]): The terminal provider.
    group_id (Optional[int]): The terminal group id.
    name (Optional[str]): The terminal name.

    """

    provider: Optional[str] = None
    group_id: Optional[int] = None
    name: Optional[str] = None

    def add_provider(
        self: "CreateTerminalRequest",
        provider: Optional[str],
    ) -> "CreateTerminalRequest":
        """
        Add a terminal provider.

        Parameters
        ----------
        provider (Optional[str]): The provider value.

        Raises
        ------
        InvalidArgumentException: If provider is not one of the allowed values.

        Returns
        -------
        CreateTerminalRequest: The current request object.

        """
        if provider is not None and provider not in ALLOWED_PROVIDERS:
            msg = (
                f'Provider "{provider}" is not a known provider. '
                f'Available providers: {", ".join(ALLOWED_PROVIDERS)}'
            )
            raise InvalidArgumentException(msg)

        self.provider = provider
        return self

    def add_group_id(
        self: "CreateTerminalRequest",
        group_id: str,
    ) -> "CreateTerminalRequest":
        """
        Add a terminal group id.

        Parameters
        ----------
        group_id (str): The terminal group identifier.

        Returns
        -------
        CreateTerminalRequest: The current request object.

        """
        self.group_id = group_id
        return self

    def add_name(
        self: "CreateTerminalRequest",
        name: Optional[str],
    ) -> "CreateTerminalRequest":
        """
        Add a terminal name.

        Parameters
        ----------
        name (Optional[str]): The terminal name.

        Returns
        -------
        CreateTerminalRequest: The current request object.

        """
        self.name = name
        return self
