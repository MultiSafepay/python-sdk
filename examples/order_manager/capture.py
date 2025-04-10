import os

from dotenv import load_dotenv

from multisafepay.api.paths.orders.order_id.capture.request.capture_request import CaptureOrderRequest
from multisafepay.sdk import Sdk
from multisafepay.value_object.amount import Amount
from multisafepay.value_object.currency import Currency

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk = Sdk(API_KEY, False)

    # Get the order manager from the SDK
    order_manager = multisafepay_sdk.get_order_manager()

    # Create an Amount object with the capture amount
    amount = Amount(amount=10)

    # Create a CaptureOrderRequest object and add the capture details
    capture_request = (CaptureOrderRequest()
                       .add_amount(amount)
                       .add_reason('Order captured')
                       .add_new_order_id('<capture_order_id>')
                       .add_new_order_status('completed'))

    # Capture the order with the specified order ID using the order manager
    capture_response = order_manager.capture('<order_id>', capture_request)

    # Print the API response containing the capture information
    # print(capture_response)

    # Return the API response containing the capture information
    capture_data = capture_response.get_data()

    # Print the capture data
    print(capture_data)
