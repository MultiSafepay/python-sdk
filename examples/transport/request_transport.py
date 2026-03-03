"""Example: Custom requests.Session transport.

This example shows how to configure a real `requests.Session` (Retry + connection
pooling) and inject it into the SDK via `RequestsTransport`.

Requires the optional extra: `multisafepay[requests]`.
"""

import os

from dotenv import load_dotenv
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from multisafepay import Sdk
from multisafepay.transport import RequestsTransport


def create_custom_session() -> Session:
    """Create a custom requests Session with retry logic and connection pooling."""
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST", "PATCH", "DELETE"],
    )

    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,
        pool_maxsize=20,
    )

    session = Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Note: requests doesn't support a global default timeout on Session.
    # Timeouts must be passed per request (or implemented in a custom transport).
    session.headers.update(
        {
            "User-Agent": "multisafepay-python-sdk-examples",
            "Accept": "application/json",
        }
    )

    return session


# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")


if __name__ == "__main__":
    # Create a custom requests Session and inject it into the SDK
    custom_session = create_custom_session()
    transport = RequestsTransport(session=custom_session)

    multisafepay_sdk: Sdk = Sdk(API_KEY, False, transport)
    gateway_manager = multisafepay_sdk.get_gateway_manager()

    get_gateways_response = gateway_manager.get_gateways()
    gateway_listing = get_gateways_response.get_data()

    print(gateway_listing)

    custom_session.close()
