# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

import pytest
from pydantic import ValidationError

from multisafepay.client.api_key import ApiKey
from multisafepay.exception.invalid_api_key import InvalidApiKeyException


def test_valid_api_key_initialization():
    """
    Test the initialization of a valid API key.

    """
    api_key = ApiKey(api_key="valid_api_key")
    assert api_key.api_key == "valid_api_key"


def test_invalid_api_key_initialization_no_argument():
    """
    Test raising ValidationError for missing API key.

    """
    with pytest.raises(ValidationError):
        ApiKey()


def test_invalid_api_key_initialization_empty():
    """
    Test raising ValidationError for missing API key.

    """
    with pytest.raises(InvalidApiKeyException, match="Invalid API key"):
        ApiKey(api_key="")


def test_invalid_api_key_initialization_none():
    """
    Test raising InvalidApiKeyException for an invalid API key.

    """
    with pytest.raises(ValidationError):
        ApiKey(api_key=None)


def test_invalid_api_key_initialization_short():
    """
    Test raising InvalidApiKeyException for an invalid API key.

    """
    with pytest.raises(InvalidApiKeyException, match="Invalid API key"):
        ApiKey(api_key="1234")


def test_api_key_retrieval():
    """
    Test the retrieval of a valid API key.

    """
    api_key = ApiKey(api_key="another_valid_key")
    assert api_key.get() == "another_valid_key"
