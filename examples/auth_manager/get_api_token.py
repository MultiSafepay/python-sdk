import os

from dotenv import load_dotenv

from multisafepay import Sdk
from multisafepay.api.base.response import CustomApiResponse
from multisafepay.api.paths import AuthManager
from multisafepay.api.paths.auth import ApiToken

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk: Sdk = Sdk(API_KEY, False)

    # Get the authentication manager from the SDK
    auth_manager: AuthManager = multisafepay_sdk.get_auth_manager()

    # Request an API token using the authentication manager
    api_token_response: CustomApiResponse = auth_manager.get_api_token()

    # print(api_token_response)

    # Extract the data from the API response
    api_token: ApiToken = api_token_response.get_data()

    # Print the API token
    print(api_token)
