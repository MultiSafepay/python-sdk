import os

from dotenv import load_dotenv

from multisafepay import Sdk

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk = Sdk(API_KEY, False)

    # Get the recurring payments manager from the SDK and retrieve the list of recurring payments for a specific shopper
    get_list_response = multisafepay_sdk.get_recurring_manager().get_list(
        reference='<reference>'
    )

    # Print the API response containing the recurring payments information
    # print(get_list_response)

    # Retrieve the recurring payments data from the API response
    recurring_payments_data = get_list_response.get_data()

    # Print the recurring payments data
    print(recurring_payments_data)
