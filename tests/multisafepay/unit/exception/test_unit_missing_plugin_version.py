# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import pytest
from multisafepay.exception.missing_plugin_version import (
    MissingPluginVersionException,
)
from multisafepay.exception.invalid_argument import InvalidArgumentException


def test_missing_plugin_version_exception_is_subclass():
    """
    Test if MissingPluginVersionException is a subclass of InvalidArgumentException.

    """
    assert issubclass(MissingPluginVersionException, InvalidArgumentException)


def test_raise_missing_plugin_version_exception():
    """
    Test raising MissingPluginVersionException.

    """
    with pytest.raises(MissingPluginVersionException):
        raise MissingPluginVersionException("Missing plugin version")
