import os

from dotenv import load_dotenv

from multisafepay import Sdk
from multisafepay.api.paths.orders.order_manager import OrderManager

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key
    multisafepay_sdk = Sdk(API_KEY, False)

    # Get the order manager instance from the SDK
    order_manager = multisafepay_sdk.get_order_manager()

    # Retrieve order details using the order manager
    order_response = order_manager.get('<order_id>')

    # Create a refund request for the retrieved order
    create_refund_request_response = OrderManager.create_refund_request(
        order_response.get_data()
    )

    # Print the response of the refund request
    print(create_refund_request_response)
