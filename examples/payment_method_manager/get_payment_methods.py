import os

from dotenv import load_dotenv

from multisafepay.sdk import Sdk

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk = Sdk(API_KEY, False)

    # Get the payment method manager from the MultiSafepay SDK
    payment_method_manager = multisafepay_sdk.get_payment_method_manager()

    # Make a request to get the available payment methods
    payment_methods_response = payment_method_manager.get_payment_methods()

    # Print the API response containing the available payment methods
    # print(payment_methods_response)

    # Retrieve the payment methods data from the API response
    payment_method_data = payment_methods_response.get_data()

    # Print the payment methods data
    print(payment_method_data)
