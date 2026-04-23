# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

import os

from dotenv import load_dotenv

from multisafepay import Sdk
from multisafepay.api.paths.terminals.request.create_terminal_request import (
    CreateTerminalRequest,
)
from multisafepay.client import ScopedCredentialResolver

# Load environment variables from a .env file
load_dotenv()

default_account_api_key = (os.getenv("API_KEY") or "").strip()
partner_affiliate_api_key = (os.getenv("PARTNER_API_KEY") or "").strip()

terminal_group_id_raw = os.getenv(
    "CLOUD_POS_TERMINAL_GROUP_ID",
    "<terminal_group_id>",
).strip()

if __name__ == "__main__":
    # create_terminal → default scope → resolver returns default_api_key
    terminal_group_id = int(terminal_group_id_raw)

    resolver_kwargs = {
        "default_api_key": default_account_api_key,
        "partner_affiliate_api_key": partner_affiliate_api_key,
    }

    credential_resolver = ScopedCredentialResolver(**resolver_kwargs)

    multisafepay_sdk = Sdk(
        is_production=False,
        credential_resolver=credential_resolver,
    )

    # Get the 'Terminal' manager from the SDK
    terminal_manager = multisafepay_sdk.get_terminal_manager()

    # Build the create terminal request
    create_request = (
        CreateTerminalRequest()
        .add_provider("CTAP")
        .add_group_id(terminal_group_id)
        .add_name("Demo POS Terminal")
    )

    # Create a new POS terminal
    terminal_response = terminal_manager.create_terminal(create_request)

    # Print the created terminal data
    terminal_data = terminal_response.get_data()
    print(terminal_data)
