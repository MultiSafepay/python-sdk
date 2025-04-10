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

    # Delete a recurring payment using the reference and token
    delete_response = multisafepay_sdk.get_recurring_manager().delete(reference='<reference>', token='<token>')

    # Print the API response containing the deletion result
    # print(delete_response)

    # Retrieve the deletion result from the API response
    deletion_result = delete_response.get_data()

    # Print the deletion result
    print(deletion_result)
