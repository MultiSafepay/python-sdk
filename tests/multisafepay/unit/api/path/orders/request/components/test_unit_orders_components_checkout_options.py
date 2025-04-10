# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.paths.orders.request.components.checkout_options import (
    CheckoutOptions,
)


def test_initializes_checkout_options_with_empty_values():
    """
    Test the initialization of CheckoutOptions with empty values.

    This test checks that the default values for tax_tables and validate_cart

    """
    checkout_options = CheckoutOptions()

    assert checkout_options.tax_tables is None
    assert checkout_options.validate_cart is None


def test_initializes_checkout_options_with_validate_cart():
    """
    Test the initialization of CheckoutOptions with validate_cart set to True.

    This test checks that the validate_cart attribute is set to True.

    """
    checkout_options = CheckoutOptions(
        validate_cart=True,
    )

    assert checkout_options.validate_cart is True
    assert checkout_options.tax_tables is None


def test_add_validate_cart_updates_value():
    """
    Test the add_validate_cart method of CheckoutOptions.

    This test checks that the validate_cart attribute is updated correctly.

    """
    checkout_options = CheckoutOptions()
    checkout_options_updated = checkout_options.add_validate_cart(
        True,
    )

    assert checkout_options.validate_cart is True
    assert isinstance(checkout_options_updated, CheckoutOptions)
