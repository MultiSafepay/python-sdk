# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for e2e testing."""

import os
import pytest
from dotenv import load_dotenv

from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.categories.response.category import Category
from multisafepay.sdk import Sdk

from multisafepay.api.paths.categories.category_manager import (
    CategoryManager,
)


@pytest.fixture(scope="module")
def category_manager() -> "CategoryManager":
    load_dotenv()
    api_key = os.getenv("API_KEY")
    multisafepay_sdk = Sdk(api_key, False)
    return multisafepay_sdk.get_category_manager()


def test_get_categories(category_manager: CategoryManager):
    """
    Test the get_categories method of the CategoryManager.

    This test checks if the list of categories is retrieved successfully and each item is of the correct type.

    """
    get_categories_response = category_manager.get_categories()
    assert isinstance(get_categories_response, CustomApiResponse)
    categories = get_categories_response.get_data()
    assert all(isinstance(category, Category) for category in categories)
