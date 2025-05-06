# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import os
import pytest
from dotenv import load_dotenv

from multisafepay.api.paths.me.response.me import Me


from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.sdk import Sdk

from multisafepay.api.paths.me.me_manager import MeManager


@pytest.fixture(scope="module")
def me_manager() -> "MeManager":
    load_dotenv()
    api_key = os.getenv("API_KEY")
    multisafepay_sdk = Sdk(api_key, False)
    return multisafepay_sdk.get_me_manager()


def test_get_me(me_manager: MeManager):
    """
    Test the get_me method of the MeManager.

    This test checks if the user information is retrieved successfully and contains the expected attributes.

    """
    get_me_response = me_manager.get()
    assert isinstance(get_me_response, CustomApiResponse)
    me = get_me_response.get_data()
    assert isinstance(me, Me)
