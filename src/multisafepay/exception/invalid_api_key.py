# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Invalid API key exception for authentication errors."""


class InvalidApiKeyException(Exception):
    """
    Exception raised for invalid API key.

    This exception is raised when the provided API key is invalid.
    """
