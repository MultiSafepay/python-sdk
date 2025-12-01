import os

from dotenv import load_dotenv

from multisafepay import Sdk
from multisafepay.api.paths.orders.order_manager import OrderManager
from multisafepay.api.paths.orders.response import Order

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key
    multisafepay_sdk = Sdk(API_KEY, False)

    # Get the order manager instance from the SDK
    order_manager: OrderManager = multisafepay_sdk.get_order_manager()

    # Retrieve order details using the order manager
    order: Order = order_manager.get('<order_id>').get_data()

    # Create a refund request for a specific item in the order
    refund_by_item_response = order_manager.refund_by_item(
        order, '<merchant_item_id>', 1
    )

    # Print the response of the refund request
    # print(refund_by_item_response)

    # Retrieve and print the data from the refund response
    refund_data = refund_by_item_response.get_data()

    # Print the refund data
    print(refund_data)
