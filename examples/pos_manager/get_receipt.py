# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Fetch the receipt for an existing Cloud POS order."""

import os

from dotenv import load_dotenv

from multisafepay import Sdk
from multisafepay.client import ScopedCredentialResolver

load_dotenv()

DEFAULT_ACCOUNT_API_KEY = os.getenv("API_KEY", "")
TERMINAL_GROUP_DEFAULT_API_KEY = os.getenv("TERMINAL_GROUP_API_KEY_GROUP_DEFAULT", "")
CLOUD_POS_TERMINAL_GROUP_ID = os.getenv("CLOUD_POS_TERMINAL_GROUP_ID", "Default")
ORDER_ID = os.getenv("CLOUD_POS_ORDER_ID", "")

if __name__ == "__main__":
    if not ORDER_ID:
        raise SystemExit(
            "Set CLOUD_POS_ORDER_ID to a completed Cloud POS order id "
            "(receipts are only available for completed orders).",
        )

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
    print(receipt_response.get_data())
