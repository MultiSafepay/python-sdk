# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

import pytest
from multisafepay.exception.invalid_api_key import InvalidApiKeyException


def test_invalid_api_key_exception_is_subclass():
    """
    Test if InvalidApiKeyException is a subclass of Exception.

    """
    assert issubclass(InvalidApiKeyException, Exception)


def test_raise_invalid_api_key_exception():
    """
    Test raising InvalidApiKeyException.

    """
    with pytest.raises(InvalidApiKeyException):
        raise InvalidApiKeyException("Invalid API key provided")
