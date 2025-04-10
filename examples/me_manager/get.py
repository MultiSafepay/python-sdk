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

    # Get the 'Me' manager from the SDK
    me_manager = multisafepay_sdk.get_me_manager()

    # Request the 'Me' information
    me = me_manager.get().get_data()

    # Print the API response containing the 'Me' information
    print(me)
