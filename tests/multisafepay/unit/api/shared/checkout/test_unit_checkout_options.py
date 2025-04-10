# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.shared.checkout.checkout_options import CheckoutOptions


def test_initializes_with_default_values():
    """
    Test that a CheckoutOptions instance initializes with default values.
    """
    checkout_options = CheckoutOptions()
    assert checkout_options.default is None
    assert checkout_options.alternate is None


def test_creates_from_empty_dict():
    """
    Test that a CheckoutOptions instance is created from an empty dictionary.
    """
    data = {}
    checkout_options = CheckoutOptions.from_dict(data)
    assert checkout_options.default is None
    assert checkout_options.alternate is None


def test_creates_from_none():
    """
    Test that a CheckoutOptions instance is created from None.
    """
    checkout_options = CheckoutOptions.from_dict(None)
    assert checkout_options is None
