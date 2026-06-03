"""Configuration for end-to-end tests."""

import os
from collections.abc import Callable
from typing import Optional
from urllib.parse import urlparse

import pytest
from dotenv import load_dotenv

from multisafepay.client import Client
from multisafepay.sdk import Sdk
from multisafepay.transport import HTTPTransport

E2E_API_KEY_ENV = "E2E_API_KEY"
E2E_BASE_URL_ENV = "E2E_BASE_URL"

# Node ids for terminal-endpoint example tests that have their own
# selective skip logic in tests/multisafepay/e2e/examples/conftest.py.
# The parent hook must not unconditionally skip these when E2E_API_KEY is
# missing, otherwise the child hook's terminal-specific env detection has no
# effect.
TERMINAL_EXAMPLE_NODE_PREFIXES = (
    "tests/multisafepay/e2e/examples/terminal_manager/",
    "tests/multisafepay/e2e/examples/terminal_group_manager/",
)

# Load .env file from the project root
load_dotenv()


def _get_e2e_api_key() -> str:
    return os.getenv(E2E_API_KEY_ENV, "").strip()


def _get_e2e_base_url() -> str:
    base_url = os.getenv(E2E_BASE_URL_ENV, "").strip()
    return base_url or Client.TEST_URL


def _validate_e2e_base_url(base_url: str, env_name: str) -> str:
    parsed = urlparse(base_url)
    if parsed.scheme != "https" or not parsed.netloc:
        msg = f"{env_name} must be a valid https URL"
        raise pytest.UsageError(msg)

    parsed = urlparse(base_url)
    path = parsed.path.rstrip("/")
    normalized_path = "/" if not path else f"{path}/"
    return f"{parsed.scheme}://{parsed.netloc}{normalized_path}"


@pytest.fixture(scope="session")
def e2e_api_key() -> str:
    """Return the dedicated API key used by E2E tests."""
    api_key = _get_e2e_api_key()
    if not api_key:
        pytest.skip(f"E2E tests require {E2E_API_KEY_ENV} (not set)")

    return api_key


@pytest.fixture(scope="session")
def e2e_base_url() -> str:
    """Return the dedicated base URL used by E2E tests."""
    return _validate_e2e_base_url(_get_e2e_base_url(), E2E_BASE_URL_ENV)


@pytest.fixture(scope="session")
def e2e_sdk_factory(
    e2e_api_key: str,
    e2e_base_url: str,
) -> Callable[..., Sdk]:
    """Create SDK instances for E2E tests with a shared configuration."""

    def create_sdk(*, transport: Optional[HTTPTransport] = None) -> Sdk:
        sdk = Sdk(
            api_key=e2e_api_key,
            is_production=False,
            transport=transport,
        )
        sdk.get_client().url = e2e_base_url

        return sdk

    return create_sdk


@pytest.fixture(scope="session")
def e2e_sdk(e2e_sdk_factory: Callable[..., Sdk]) -> Sdk:
    """Return the default SDK instance used by E2E tests."""
    return e2e_sdk_factory()


def pytest_collection_modifyitems(
    config: pytest.Config,  # noqa: ARG001
    items: list[pytest.Item],
) -> None:
    """
    Skip all e2e tests when E2E_API_KEY is missing.

    These tests perform real API calls. In most local/CI environments the secret
    isn't present, so we prefer a clean skip over hard errors during fixture setup.
    """
    if _get_e2e_api_key():
        return

    skip = pytest.mark.skip(
        reason=f"E2E tests require {E2E_API_KEY_ENV} (not set)",
    )
    for item in items:
        # This hook runs for the whole session (all collected tests), even when
        # this conftest is only loaded due to e2e tests being present/deselected.
        # Ensure we only affect e2e tests.
        if not item.nodeid.startswith("tests/multisafepay/e2e/"):
            continue

        # Terminal-endpoint example tests can run with their own dedicated
        # credentials (API_KEY + MSP_SDK_CUSTOM_BASE_URL +
        # E2E_CLOUD_POS_TERMINAL_ID) without E2E_API_KEY. Defer the skip
        # decision for those tests to the child conftest under
        # tests/multisafepay/e2e/examples/, which inspects the
        # terminal-specific env.
        if item.nodeid.startswith(TERMINAL_EXAMPLE_NODE_PREFIXES):
            continue

        item.add_marker(skip)
