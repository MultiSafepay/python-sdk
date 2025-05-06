import os
from typing import List

from dotenv import load_dotenv

from multisafepay.api.base.listings.listing import Listing
from multisafepay.api.base.response.custom_api_response import CustomApiResponse
from multisafepay.api.paths.gateways.gateway_manager import GatewayManager
from multisafepay.api.paths.gateways.response.gateway import Gateway
from multisafepay.sdk import Sdk

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk: Sdk = Sdk(API_KEY, False)

    # Get the gateway manager from the SDK
    gateway_manager: GatewayManager = multisafepay_sdk.get_gateway_manager()

    # Request the list of gateways
    get_gateways_response: CustomApiResponse = gateway_manager.get_gateways()

    # Print the API response containing the list of gateways
    # print(get_gateways_response)

    # Extract the listing of gateways from the response
    gatewayListing: List[Gateway] = get_gateways_response.get_data()

    print(gatewayListing)
