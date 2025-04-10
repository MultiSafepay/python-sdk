import os

from dotenv import load_dotenv

from multisafepay.util.webhook import Webhook

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    Webhook.validate(request="<request>", auth="<header_auth>", api_key=API_KEY, validation_time_in_seconds=600)
