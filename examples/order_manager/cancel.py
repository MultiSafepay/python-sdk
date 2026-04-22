# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Create a Cloud POS order, wait 5 seconds, and cancel it."""

import os
import time

from dotenv import load_dotenv

from multisafepay import Sdk
from multisafepay.api.paths.orders.request import OrderRequest
from multisafepay.client import ScopedCredentialResolver

# Load environment variables from a .env file
load_dotenv()

DEFAULT_ACCOUNT_API_KEY = (os.getenv("API_KEY") or "").strip()
PARTNER_AFFILIATE_API_KEY = (os.getenv("PARTNER_API_KEY") or "").strip()
TERMINAL_GROUP_DEFAULT_API_KEY = (
    os.getenv("TERMINAL_GROUP_API_KEY_GROUP_DEFAULT") or ""
).strip()
CLOUD_POS_TERMINAL_GROUP_ID = os.getenv(
    "CLOUD_POS_TERMINAL_GROUP_ID",
    "Default",
)

if __name__ == "__main__":
    # This example executes Cloud POS calls with terminal-group scope.
    scoped_terminal_group_id = CLOUD_POS_TERMINAL_GROUP_ID
    resolver_kwargs = {
        "default_api_key": DEFAULT_ACCOUNT_API_KEY,
        "partner_affiliate_api_key": PARTNER_AFFILIATE_API_KEY,
    }
    if scoped_terminal_group_id:
        resolver_kwargs["terminal_group_api_keys"] = {
            scoped_terminal_group_id: TERMINAL_GROUP_DEFAULT_API_KEY,
        }

    credential_resolver = ScopedCredentialResolver(**resolver_kwargs)

    multisafepay_sdk = Sdk(
        is_production=False,
        credential_resolver=credential_resolver,
    )
    order_manager = multisafepay_sdk.get_order_manager()

    # Temporary override for local runs; comment this line to force literal placeholder.
    terminal_id = os.getenv("CLOUD_POS_TERMINAL_ID", "<terminal_id>")

    order_request = (
        OrderRequest()
        .add_type("redirect")
        .add_order_id(f"cloud-pos-cancel-{int(time.time())}")
        .add_description("Cloud POS cancel order")
        .add_amount(100)
        .add_currency("EUR")
        .add_gateway_info(
            {
                "terminal_id": terminal_id,
            },
        )
    )

    create_response = order_manager.create(
        order_request,
        terminal_group_id=scoped_terminal_group_id,
    )
    order = create_response.get_data()

    if order is None or not order.order_id:
        raise RuntimeError("Order creation did not return order_id")

    order_id = order.order_id
    print(f"Created Cloud POS order: {order_id}")
    print("Waiting 5 seconds before cancel...")
    time.sleep(5)

    cancel_response = order_manager.cancel_transaction(
        order_id,
        terminal_group_id=scoped_terminal_group_id,
    )

    print(f"Canceled Cloud POS order: {order_id}")
    print(cancel_response.get_data())
