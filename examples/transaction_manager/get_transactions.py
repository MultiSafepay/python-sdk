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

    # Get the transaction manager from the SDK
    transaction_manager = multisafepay_sdk.get_transaction_manager()

    # Retrieve all transactions using the transaction manager
    transaction_response = transaction_manager.get_transactions()

    # Print the API response containing the transactions
    # print(transaction_response)

    # Retrieve the transactions from the API response
    transactions = transaction_response.get_data()

    # Print the transactions
    print(transactions)
