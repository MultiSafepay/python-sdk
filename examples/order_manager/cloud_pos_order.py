# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Create a Cloud POS order using terminal-group scoped authentication."""

import os
import time

from dotenv import load_dotenv

from multisafepay import Sdk
from multisafepay.api.paths.orders.request import OrderRequest
from multisafepay.client import ScopedCredentialResolver

load_dotenv()

DEFAULT_ACCOUNT_API_KEY = os.getenv("API_KEY", "")
TERMINAL_GROUP_DEFAULT_API_KEY = os.getenv("TERMINAL_GROUP_API_KEY_GROUP_DEFAULT", "")
CLOUD_POS_TERMINAL_GROUP_ID = os.getenv("CLOUD_POS_TERMINAL_GROUP_ID", "Default")
TERMINAL_ID = os.getenv("CLOUD_POS_TERMINAL_ID", "")

if __name__ == "__main__":
    credential_resolver = ScopedCredentialResolver(
        default_api_key=DEFAULT_ACCOUNT_API_KEY,
        terminal_group_api_keys={
            CLOUD_POS_TERMINAL_GROUP_ID: TERMINAL_GROUP_DEFAULT_API_KEY,
        },
    )

    multisafepay_sdk = Sdk(
        is_production=False,
        credential_resolver=credential_resolver,
    )
    order_manager = multisafepay_sdk.get_order_manager()

    order_request = (
        OrderRequest()
        .add_type("redirect")
        .add_order_id(f"cloud-pos-{int(time.time())}")
        .add_description("Cloud POS order")
        .add_amount(100)
        .add_currency("EUR")
        .add_gateway_info({"terminal_id": TERMINAL_ID})
    )

    create_response = order_manager.create(
        order_request,
        terminal_group_id=CLOUD_POS_TERMINAL_GROUP_ID,
    )
    order = create_response.get_data()

    print(f"Created Cloud POS order: {order.order_id}")
    if order.payment_url:
        print(f"Payment URL: {order.payment_url}")
