import os

from dotenv import load_dotenv

from multisafepay.api.paths.orders.order_id.update.request.update_request import UpdateOrderRequest
from multisafepay.sdk import Sdk

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk = Sdk(API_KEY, False)

    # Get the order manager from the SDK
    order_manager = multisafepay_sdk.get_order_manager()

    # Create an UpdateOrderRequest object and set the status to '<new_status>'
    update_order_request = UpdateOrderRequest().add_status('<new_status>')

    # Update the order with the specified order ID using the order manager
    update_response = order_manager.update('<order_id>', update_order_request)

    # Print the API response containing the updated order information
    # print(update_response)

    # Return the API response containing the updated order information
    update_data = update_response.get_data()

    # Print the updated order data
    print(update_data)
