# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the base API decorator utilities."""

from multisafepay.api.base.decorator import Decorator


def test_initialization_with_empty_dependencies():
    """Test the initialization of a Decorator object with empty dependencies."""
    decorator = Decorator()
    assert decorator.get_dependencies() == {}
