# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the category response model."""

from multisafepay.api.paths.categories.response.category import Category


def test_initializes_with_code_and_description():
    """
    Test that the Category object initializes correctly with code and description.

    This test verifies that the Category object initializes with the correct
    values for the code and description attributes.
    """
    category = Category(code="123", description="Test Category")
    assert category.code == "123"
    assert category.description == "Test Category"


def test_initializes_with_none_values():
    """
    Test that the Category object initializes correctly with None values.

    This test verifies that the Category object initializes with None
    for the code and description attributes when no data is provided.
    """
    category = Category()
    assert category.code is None
    assert category.description is None


def test_from_dict_creates_instance_from_dict():
    """
    Test that the from_dict method initializes a Category object with valid data.

    This test verifies that the from_dict method correctly creates a Category
    object from a dictionary containing valid data.
    """
    data = {"code": "001", "description": "Test Category"}
    category = Category.from_dict(data)
    assert category.code == "001"
    assert category.description == "Test Category"


def test_from_dict_returns_none_for_none_input():
    """
    Test that the from_dict method returns None when the input dictionary is None.

    This test verifies that the from_dict method returns None when None is provided
    as the input dictionary.
    """
    category = Category.from_dict(None)
    assert category is None


def test_from_dict_handles_missing_fields():
    """
    Test that the from_dict method handles missing fields by setting them to None.

    This test verifies that the from_dict method correctly creates a Category
    object from a dictionary with missing fields, resulting in None values for
    the code and description attributes.
    """
    data = {}
    category = Category.from_dict(data)
    assert category.code is None
    assert category.description is None
