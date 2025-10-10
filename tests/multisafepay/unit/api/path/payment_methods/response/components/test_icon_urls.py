# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.payment_methods.response.components.icon_urls import (
    IconUrls,
)


def test_initializes_correctly():
    """
    Test that the IconUrls object initializes correctly with given values.

    This test verifies that the IconUrls object is initialized with the provided
    large, medium, and vector attributes.
    """
    icon_urls = IconUrls(
        large="large_url",
        medium="medium_url",
        vector="vector_url",
    )
    assert icon_urls.large == "large_url"
    assert icon_urls.medium == "medium_url"
    assert icon_urls.vector == "vector_url"


def test_from_dict_creates_icon_urls_instance_correctly():
    """
    Test that from_dict method creates an IconUrls instance correctly.

    This test verifies that the from_dict method of the IconUrls class
    creates an IconUrls instance with the correct attributes from a dictionary.
    """
    data = {
        "large": "large_url",
        "medium": "medium_url",
        "vector": "vector_url",
    }
    icon_urls = IconUrls.from_dict(data)
    assert icon_urls.large == "large_url"
    assert icon_urls.medium == "medium_url"
    assert icon_urls.vector == "vector_url"


def test_from_dict_returns_none_for_none_input():
    """
    Test that from_dict method returns None for None input.

    This test verifies that the from_dict method of the IconUrls class
    returns None when the input dictionary is None.
    """
    assert IconUrls.from_dict(None) is None


def test_from_dict_handles_missing_fields():
    """
    Test that from_dict method handles missing fields correctly.

    This test verifies that the from_dict method of the IconUrls class
    handles missing fields in the input dictionary correctly.
    """
    data = {"large": "large_url"}
    icon_urls = IconUrls.from_dict(data)
    assert icon_urls.large == "large_url"
    assert icon_urls.medium is None
    assert icon_urls.vector is None
