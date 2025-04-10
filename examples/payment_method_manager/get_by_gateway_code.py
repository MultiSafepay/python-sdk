import os

from dotenv import load_dotenv

from multisafepay.sdk import Sdk

# API key to authenticate requests to the MultiSafepay SDK
load_dotenv()
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk = Sdk(API_KEY, False)

    # Get the payment method manager from the SDK
    payment_method_manager = multisafepay_sdk.get_payment_method_manager()

    # Retrieve the payment method using the gateway code
    get_by_gateway_code_response = payment_method_manager.get_by_gateway_code("IDEAL")

    # Print the API response containing the payment method information
    # print(get_by_gateway_code_response)

    # The payment method information can be accessed using the get_data method
    gateway_code_data = get_by_gateway_code_response.get_data()

    # Print the payment method information
    print(gateway_code_data)
