# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""JSON encoder utilities for API serialization."""

import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that converts Decimal objects to float for API serialization.

    This encoder ensures that Decimal values used for precise calculations
    are properly serialized when sending data to the API.
    """

    def default(
        self: "DecimalEncoder",
        o: object,
    ) -> object:  # pylint: disable=invalid-name
        """
        Convert Decimal to float, otherwise use default encoder.

        Parameters
        ----------
        o : object
            The object to serialize.

        Returns
        -------
        object
            The serialized object (float for Decimal, default for others).

        """
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)
