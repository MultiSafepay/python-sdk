# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.gateway_info.issuer import (
    Issuer,
)


def test_initializes_issuer_correctly():
    """
    Test that the Issuer object is initialized correctly with given values.
    """
    issuer = Issuer(issuer_id="12345")

    assert issuer.issuer_id == "12345"


def test_initializes_issuer_with_empty_values():
    """
    Test that the Issuer object is initialized correctly with empty values.
    """
    issuer = Issuer()

    assert issuer.issuer_id is None


def test_add_issuer_id_updates_value():
    """
    Test that the add_issuer_id method updates the issuer_id attribute.
    """
    request = Issuer()
    request_updated = request.add_issuer_id("12345")

    assert request.issuer_id == "12345"
    assert isinstance(request_updated, Issuer)
