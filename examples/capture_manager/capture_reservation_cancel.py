import os

from dotenv import load_dotenv

from multisafepay.api.base.response.custom_api_response import CustomApiResponse
from multisafepay.api.paths.capture.request.capture_request import CaptureRequest
from multisafepay.api.paths.capture.response.capture import CancelReservation
from multisafepay.sdk import Sdk

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk = Sdk(API_KEY, False)

    # Get the capture manager from the SDK
    capture_manager = multisafepay_sdk.get_capture_manager()

    # Create a capture request with status 'cancelled' and a reason
    capture_request = (CaptureRequest().add_status('cancelled').add_reason('<reason>'))

    # Cancel the capture reservation for the given order ID
    capture_reservation_cancel_response: CustomApiResponse = capture_manager.capture_reservation_cancel(
        '<order_id>',
        capture_request)
    # Print the API response containing the capture reservation cancel information
    # print(capture_reservation_cancel_response)

    # Extract the data from the capture reservation cancel response
    capture_data = capture_reservation_cancel_response.get_data()

    # Print the capture data
    print(capture_data)
