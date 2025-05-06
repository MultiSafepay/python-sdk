# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import os
import pytest
from dotenv import load_dotenv
from multisafepay.api.paths.payment_methods.response.payment_method import (
    PaymentMethod,
)

from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.payment_methods.payment_method_manager import (
    PaymentMethodManager,
)
from multisafepay.sdk import Sdk


@pytest.fixture(scope="module")
def payment_method_manager() -> PaymentMethodManager:
    load_dotenv()
    api_key = os.getenv("API_KEY")
    multisafepay_sdk = Sdk(api_key, False)
    return multisafepay_sdk.get_payment_method_manager()


def test_get_by_gateway_code(payment_method_manager: PaymentMethodManager):
    """
    Test the get_by_gateway_code method of the PaymentMethodManager.

    This test checks if the payment method is retrieved successfully and is of the correct type.

    """
    get_by_gateway_code_response = payment_method_manager.get_by_gateway_code(
        "IDEAL",
    )
    assert isinstance(get_by_gateway_code_response, CustomApiResponse)
    payment_method = get_by_gateway_code_response.get_data()
    assert isinstance(payment_method, PaymentMethod)
