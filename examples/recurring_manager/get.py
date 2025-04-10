import os

from dotenv import load_dotenv

from multisafepay.sdk import Sdk

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    mulsafepay_sdk = Sdk(API_KEY, False)

    # Get the recurring payment details using the reference and token
    get_response = mulsafepay_sdk.get_recurring_manager().get(reference='<reference>', token='<token>')

    # Print the API response containing the recurring payment details
    # print(get_response)

    # Retrieve the recurring payment details from the API response
    recurring_payment = get_response.get_data()

    # Print the recurring payment details
    print(recurring_payment)
