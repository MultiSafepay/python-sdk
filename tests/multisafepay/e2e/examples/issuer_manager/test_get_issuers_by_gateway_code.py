# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for e2e testing."""

import os
import pytest
from dotenv import load_dotenv
from multisafepay.api.paths.issuers.response.issuer import Issuer

from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.issuers.issuer_manager import IssuerManager
from multisafepay.sdk import Sdk


@pytest.fixture(scope="module")
def issuer_manager() -> IssuerManager:
    """Fixture that provides an IssuerManager instance for testing."""
    load_dotenv()
    api_key = os.getenv("API_KEY")
    multisafepay_sdk = Sdk(api_key, False)
    return multisafepay_sdk.get_issuer_manager()


def test_get_issuers_by_gateway_code(issuer_manager: IssuerManager):
    """
    Test the get_issuers_by_gateway_code method of the IssuerManager.

    This test checks if the list of issuers is retrieved successfully and is of the correct type.

    """
    get_issuers_by_gateway_code_response = (
        issuer_manager.get_issuers_by_gateway_code("MYBANK")
    )
    assert isinstance(get_issuers_by_gateway_code_response, CustomApiResponse)
    issuers_by_gateway_code = get_issuers_by_gateway_code_response.get_data()
    assert isinstance(issuers_by_gateway_code, list)
    if issuers_by_gateway_code:
        assert all(
            isinstance(issuer, Issuer) for issuer in issuers_by_gateway_code
        )
