# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test that the package was installed correctly."""

import multisafepay


def test_package_named_correctly():
    """The package should be imported and named correctly."""
    assert multisafepay.__name__ == "multisafepay"
