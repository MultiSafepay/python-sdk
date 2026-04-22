# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Create a Cloud POS order and print its event stream credentials."""

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
    # Reuse one SDK for mixed traffic. The resolver is the source of truth for
    # which key is used per endpoint/scope.
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

    terminal_id = "<terminal_id>"
    # Uncomment this line to override with CLOUD_POS_TERMINAL_ID from .env.
    # terminal_id = os.getenv("CLOUD_POS_TERMINAL_ID", terminal_id)

    order_id = f"cloud-pos-{int(time.time())}"

    order_request = (
        OrderRequest()
        .add_type("redirect")
        .add_order_id(order_id)
        .add_description("Cloud POS order")
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

    if order is None:
        raise RuntimeError("Order creation did not return order data")

    print(f"Created Cloud POS order: {order.order_id}")

    events_token = order.events_token or order.event_token
    events_stream_url = order.events_stream_url or order.event_stream_url

    if events_token and events_stream_url:
        print("Event stream credentials:")
        print(f"EVENTS_TOKEN={events_token}")
        print(f"EVENTS_STREAM_URL={events_stream_url}")
