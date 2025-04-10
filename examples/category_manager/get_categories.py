import os

from dotenv import load_dotenv

from multisafepay.api.base.listings.listing import Listing
from multisafepay.api.base.response.custom_api_response import CustomApiResponse
from multisafepay.api.paths.categories.response.category import Category
from multisafepay.sdk import Sdk

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk = Sdk(API_KEY, False)

    # Get the category manager from the SDK
    category_manager = multisafepay_sdk.get_category_manager()

    # Request categories through the category manager
    get_categories_response: CustomApiResponse = category_manager.get_categories()

    # Print the API response containing the categories
    # print(get_categories_response)

    # Print the API response containing the categories
    categories: list[Category] = get_categories_response.get_data()

    print(categories)
