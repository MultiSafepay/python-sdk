import os

from dotenv import load_dotenv

from multisafepay.api.base.response.custom_api_response import CustomApiResponse
from multisafepay.api.paths.gateways.gateway_manager import GatewayManager
from multisafepay.api.paths.gateways.response.gateway import Gateway
from multisafepay.sdk import Sdk

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk: Sdk = Sdk(API_KEY, False)

    # Get the gateway manager from the SDK
    gateway_manager: GatewayManager = multisafepay_sdk.get_gateway_manager()

    # Request the gateway information by its code
    get_by_code_response: CustomApiResponse = gateway_manager.get_by_code("IDEAL")

    # Print the API response containing the gateway information
    # print(get_by_code_response)

    # Extract the gateway information from the response
    gateway: Gateway = get_by_code_response.get_data()

    print(gateway)
