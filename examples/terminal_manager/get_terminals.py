# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

import os

from dotenv import load_dotenv

from multisafepay import Sdk
from multisafepay.client import ScopedCredentialResolver

# Load environment variables from a .env file
load_dotenv()

default_account_api_key = (os.getenv("API_KEY") or "").strip()
partner_affiliate_api_key = (os.getenv("PARTNER_API_KEY") or "").strip()

if __name__ == "__main__":
    # get_terminals → partner_affiliate scope → resolver returns
    # partner_affiliate_api_key, falls back to default_api_key
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

    # Define optional pagination parameters
    options = {
        "limit": 10,
        "page": 1,
    }

    # Fetch terminals for the account
    terminals_response = terminal_manager.get_terminals(options=options)

    # Print the terminal listing data
    print(terminals_response.get_data())
