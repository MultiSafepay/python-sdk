# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import os
import pytest
from dotenv import load_dotenv
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.gateways.gateway_manager import GatewayManager
from multisafepay.api.paths.gateways.response.gateway import Gateway
from multisafepay.sdk import Sdk


@pytest.fixture(scope="module")
def gateway_manager() -> GatewayManager:
    load_dotenv()
    api_key = os.getenv("API_KEY")
    multisafepay_sdk = Sdk(api_key, False)
    return multisafepay_sdk.get_gateway_manager()


def test_get_by_code(gateway_manager: GatewayManager):
    """
    Test the get_by_code method of the GatewayManager.

    This test checks if the gateway is retrieved successfully and is of the correct type.

    """
    get_by_code_response = gateway_manager.get_by_code("IDEAL")
    assert isinstance(get_by_code_response, CustomApiResponse)
    gateway = get_by_code_response.get_data()
    assert isinstance(gateway, Gateway)
