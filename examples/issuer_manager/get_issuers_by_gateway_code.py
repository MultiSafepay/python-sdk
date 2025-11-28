import os

from dotenv import load_dotenv

from multisafepay import Sdk
from multisafepay.api.base.response import CustomApiResponse

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk = Sdk(API_KEY, False)

    # Get the issuer manager from the SDK
    issuer_manager = multisafepay_sdk.get_issuer_manager()

    # Request the list of issuers by the gateway code "MYBANK"
    get_issuers_by_gateway_code_response: CustomApiResponse = (
        issuer_manager.get_issuers_by_gateway_code("MYBANK")
    )

    # Print the API response containing the list of issuers
    # print(get_issuers_by_gateway_code_response)

    # Print the API response containing the list of issuers
    issuers_by_gateway_code = (
        get_issuers_by_gateway_code_response.get_data()
    )

    print(issuers_by_gateway_code)
