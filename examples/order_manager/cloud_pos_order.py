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

# Load environment variables from a .env file
load_dotenv()


def _get_first_env(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value

    return ""


def _require_first_env(*names: str) -> str:
    value = _get_first_env(*names)
    if value:
        return value

    raise RuntimeError(
        f"Missing required environment variable. Set one of: {', '.join(names)}",
    )


DEFAULT_ACCOUNT_API_KEY = _require_first_env("API_KEY", "E2E_API_KEY")
TERMINAL_GROUP_DEFAULT_API_KEY = _require_first_env(
    "TERMINAL_GROUP_API_KEY_GROUP_DEFAULT",
    "E2E_TERMINAL_GROUP_API_KEY_GROUP_DEFAULT",
)
CLOUD_POS_TERMINAL_GROUP_ID = (
    os.getenv("CLOUD_POS_TERMINAL_GROUP_ID", "Default").strip()
    or "Default"
)
TERMINAL_ID = _require_first_env(
    "CLOUD_POS_TERMINAL_ID",
    "E2E_CLOUD_POS_TERMINAL_ID",
)

if __name__ == "__main__":
    # This example executes Cloud POS calls with terminal-group scope.
    scoped_terminal_group_id = CLOUD_POS_TERMINAL_GROUP_ID
    resolver_kwargs = {
        "default_api_key": DEFAULT_ACCOUNT_API_KEY,
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
                "terminal_id": TERMINAL_ID,
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

    if order.payment_url:
        print(f"Payment URL: {order.payment_url}")
