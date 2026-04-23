# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Fetch the receipt for an existing Cloud POS order."""

import os

from dotenv import load_dotenv

from multisafepay import Sdk
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
ORDER_ID = _require_first_env("CLOUD_POS_ORDER_ID", "POS_ORDER_ID")

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
    pos_manager = multisafepay_sdk.get_pos_manager()

    receipt_response = pos_manager.get_receipt(
        order_id=ORDER_ID,
        terminal_group_id=CLOUD_POS_TERMINAL_GROUP_ID,
    )
    print(receipt_response.get_data())# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

import os
import time

from dotenv import load_dotenv

from multisafepay import Sdk
from multisafepay.api.paths.orders.request import OrderRequest
from multisafepay.client import ScopedCredentialResolver

# Load environment variables from a .env file
load_dotenv()

default_account_api_key = (os.getenv("API_KEY") or "").strip()
terminal_group_default_api_key = (os.getenv("TERMINAL_GROUP_API_KEY_GROUP_DEFAULT") or "").strip()
partner_affiliate_api_key = (os.getenv("PARTNER_API_KEY") or "").strip()
terminal_group_id = os.getenv("CLOUD_POS_TERMINAL_GROUP_ID", "Default")
terminal_id = os.getenv("CLOUD_POS_TERMINAL_ID", "<terminal_id>")


def _payload_get(payload: object, key: str) -> object:
    """Read a payload field from either a dict or a response model."""
    if isinstance(payload, dict):
        return payload.get(key)
    return getattr(payload, key, None)


def _is_completed_event(event: object) -> bool:
    """Return True when the SSE payload indicates a completed payment."""
    payload = getattr(event, "data", None)
    status = _payload_get(payload, "status")
    if isinstance(status, str) and status.lower() == "completed":
        return True

    nested_payload = _payload_get(payload, "data")
    nested_status = _payload_get(nested_payload, "status")
    if (
        isinstance(nested_status, str)
        and nested_status.lower() == "completed"
    ):
        return True

    return False

if __name__ == "__main__":
    # This example executes Cloud POS calls with terminal-group scope.
    scoped_terminal_group_id = terminal_group_id
    resolver_kwargs = {
        "default_api_key": default_account_api_key,
        "partner_affiliate_api_key": partner_affiliate_api_key,
    }
    if scoped_terminal_group_id:
        resolver_kwargs["terminal_group_api_keys"] = {
            scoped_terminal_group_id: terminal_group_default_api_key,
        }

    credential_resolver = ScopedCredentialResolver(**resolver_kwargs)

    multisafepay_sdk = Sdk(
        is_production=False,
        credential_resolver=credential_resolver,
    )

    # Get the managers from the SDK
    order_manager = multisafepay_sdk.get_order_manager()
    event_manager = multisafepay_sdk.get_event_manager()
    pos_manager = multisafepay_sdk.get_pos_manager()

    order_request = (
        OrderRequest()
        .add_type("redirect")
        .add_order_id(f"cloud-pos-receipt-{int(time.time())}")
        .add_description("Cloud POS order for receipt")
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

    print(f"Created Cloud POS order: {order.order_id}")
    print("Waiting for completed event...")

    with event_manager.subscribe_order_events(order, timeout=45.0) as stream:
        for event in stream:
            print(event)

            if not _is_completed_event(event):
                continue

            print("Completed event detected. Fetching receipt...")
            receipt_response = pos_manager.get_receipt(
                order_id=order.order_id,
                terminal_group_id=scoped_terminal_group_id,
            )
            print(receipt_response.get_data())
            break
