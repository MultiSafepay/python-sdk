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
from multisafepay.api.paths.auth.api_token.response.api_token import ApiToken
from multisafepay.api.paths.auth.auth_manager import AuthManager
from multisafepay.sdk import Sdk


@pytest.fixture(scope="module")
def auth_manager() -> AuthManager:
    """Fixture that provides an AuthManager instance for testing."""
    load_dotenv()
    api_key = os.getenv("API_KEY")
    multisafepay_sdk = Sdk(api_key, False)
    return multisafepay_sdk.get_auth_manager()


def test_get_api_token(auth_manager: AuthManager):
    """
    Test the get_api_token method of the AuthManager.

    This test checks if the API token is retrieved successfully and is of the correct type.

    """
    api_token_response = auth_manager.get_api_token()
    assert isinstance(api_token_response, CustomApiResponse)
    api_token = api_token_response.get_data()
    assert isinstance(api_token, ApiToken)
