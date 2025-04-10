# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

import pytest
from multisafepay.exception.invalid_argument import InvalidArgumentException


def test_invalid_argument_exception():
    """
    Test raising InvalidArgumentException.

    """
    with pytest.raises(InvalidArgumentException):
        raise InvalidArgumentException("Invalid argument")
