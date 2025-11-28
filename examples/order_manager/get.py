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

    # Get the 'Order' manager from the SDK
    order_manager = multisafepay_sdk.get_order_manager()

    # Request the 'Order' information using the order ID
    order_response = order_manager.get("<order_id>")

    # Print the API response containing the order information
    # print(order_response)

    # Return the API response containing the capture information
    order_data = order_response.get_data()

    # Print the order data
    print(order_data)
