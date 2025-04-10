# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.paths.gateways.gateway_manager import ALLOWED_OPTIONS


def test_allowed_options_contains_expected_keys():
    """
    Test that ALLOWED_OPTIONS contains the expected keys.

    This test verifies that the keys 'country', 'currency', 'amount', and 'include'
    are present in the ALLOWED_OPTIONS dictionary.
    """
    assert "country" in ALLOWED_OPTIONS
    assert "currency" in ALLOWED_OPTIONS
    assert "amount" in ALLOWED_OPTIONS
    assert "include" in ALLOWED_OPTIONS


def test_allowed_options_values_are_empty_strings():
    """
    Test that the values in ALLOWED_OPTIONS are empty strings.

    This test verifies that all values in the ALLOWED_OPTIONS dictionary are empty strings.
    """
    for key in ALLOWED_OPTIONS:
        assert ALLOWED_OPTIONS[key] == ""
