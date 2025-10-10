# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.payment_methods.response.components.apps import (
    Apps,
)


def test_initializes_correctly():
    """
    Test that the Apps object initializes correctly with None values.

    This test verifies that the Apps object is initialized with None
    for both fastcheckout and payment_components attributes.
    """
    apps = Apps(fastcheckout=None, payment_components=None)
    assert apps.fastcheckout is None
    assert apps.payment_components is None


def test_from_dict_creates_apps_instance_correctly():
    """
    Test that from_dict method creates an Apps instance correctly.

    This test verifies that the from_dict method of the Apps class
    creates an Apps instance with the correct attributes from a dictionary.
    """
    data = {}
    apps = Apps.from_dict(data)
    assert apps.fastcheckout is None
    assert apps.payment_components is None


def test_from_dict_returns_none_for_none_input():
    """
    Test that from_dict method returns None for None input.

    This test verifies that the from_dict method of the Apps class
    returns None when the input dictionary is None.
    """
    assert Apps.from_dict(None) is None
