# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import pytest
from multisafepay.exception.api_unavailable import ApiUnavailableException
from multisafepay.exception.api import ApiException


def test_api_unavailable_exception_is_subclass():
    """
    Test if ApiUnavailableException is a subclass of ApiException.

    """
    assert issubclass(ApiUnavailableException, ApiException)


def test_raise_api_unavailable_exception():
    """
    Test raising ApiUnavailableException.

    """
    with pytest.raises(ApiUnavailableException):
        raise ApiUnavailableException("API is unavailable")
