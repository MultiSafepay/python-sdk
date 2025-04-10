# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.v


from multisafepay.api.paths.payment_methods.response.components.brand import (
    Brand,
)


def test_initializes_correctly():
    """
    Test that the Brand object initializes correctly with given values.

    This test verifies that the Brand object is initialized with the provided
    allowed_countries, icon_urls, id, and name attributes.
    """
    brand = Brand(
        allowed_countries=None,
        icon_urls=None,
        id="brand_id",
        name="brand_name",
    )
    assert brand.allowed_countries is None
    assert brand.icon_urls is None
    assert brand.id == "brand_id"
    assert brand.name == "brand_name"


def test_from_dict_creates_brand_instance_correctly():
    """
    Test that from_dict method creates a Brand instance correctly.

    This test verifies that the from_dict method of the Brand class
    creates a Brand instance with the correct attributes from a dictionary.
    """
    data = {
        "allowed_countries": None,
        "icon_urls": None,
        "id": "brand_id",
        "name": "brand_name",
    }
    brand = Brand.from_dict(data)
    assert brand.allowed_countries is None
    assert brand.icon_urls is None
    assert brand.id == "brand_id"
    assert brand.name == "brand_name"


def test_from_dict_returns_none_for_none_input():
    """
    Test that from_dict method returns None for None input.

    This test verifies that the from_dict method of the Brand class
    returns None when the input dictionary is None.
    """
    assert Brand.from_dict(None) is None
