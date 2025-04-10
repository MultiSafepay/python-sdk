import os

from dotenv import load_dotenv

from multisafepay.api.paths.orders.order_id.refund.request.refund_request import RefundOrderRequest
from multisafepay.sdk import Sdk
from multisafepay.value_object.amount import Amount
from multisafepay.value_object.currency import Currency
from multisafepay.api.shared.description import Description

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk = Sdk(API_KEY, False)

    # Get the order manager from the SDK
    order_manager = multisafepay_sdk.get_order_manager()

    # Create a RefundOrderRequest object and add the refund details
    refund_request = (RefundOrderRequest()
    .add_amount(Amount(amount=100))
    .add_currency(Currency(currency='EUR'))
    .add_description(
        Description().add_description('Refund for order #<order_id>')))

    # Request a refund for the specified order ID using the order manager
    refund_response = order_manager.refund('<order_id>', refund_request)

    # Print the API response containing the capture information
    # print(refund_response)

    # Return the API response containing the capture information
    refund_data = refund_response.get_data()

    # Print the capture data
    print(refund_data)
