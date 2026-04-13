"""Configuration for end-to-end tests."""

import os
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Optional

import pytest
from dotenv import load_dotenv

from multisafepay.client.client import Client
from multisafepay.sdk import Sdk
from multisafepay.transport import HTTPTransport

E2E_API_KEY_ENV = "E2E_API_KEY"
BUILD_PROFILE_ENV = "MSP_SDK_BUILD_PROFILE"
ALLOW_CUSTOM_BASE_URL_ENV = "MSP_SDK_ALLOW_CUSTOM_BASE_URL"
CUSTOM_BASE_URL_ENV = "MSP_SDK_CUSTOM_BASE_URL"

# Load .env file from the project root
load_dotenv()


def _get_e2e_api_key() -> str:
    return os.getenv(E2E_API_KEY_ENV, "").strip()


@contextmanager
def _without_custom_base_url_env() -> Iterator[None]:
    """Temporarily disable custom base URL overrides for E2E SDK creation."""
    env_names = (
        BUILD_PROFILE_ENV,
        ALLOW_CUSTOM_BASE_URL_ENV,
        CUSTOM_BASE_URL_ENV,
    )
    previous_values = {name: os.getenv(name) for name in env_names}

    for name in env_names:
        os.environ.pop(name, None)

    try:
        yield
    finally:
        for name, value in previous_values.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


@pytest.fixture(scope="session")
def e2e_api_key() -> str:
    """Return the dedicated API key used by E2E tests."""
    api_key = _get_e2e_api_key()
    if not api_key:
        pytest.skip(f"E2E tests require {E2E_API_KEY_ENV} (not set)")

    return api_key


@pytest.fixture(scope="session")
def e2e_sdk_factory(e2e_api_key: str) -> Callable[..., Sdk]:
    """Create SDK instances for E2E tests with a shared configuration."""

    def create_sdk(*, transport: Optional[HTTPTransport] = None) -> Sdk:
        with _without_custom_base_url_env():
            sdk = Sdk(
                api_key=e2e_api_key,
                is_production=False,
                transport=transport,
            )

        if sdk.get_client().url != Client.TEST_URL:
            raise RuntimeError(
                "E2E SDK must use the test API base URL.",
            )

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
        if item.nodeid.startswith("tests/multisafepay/e2e/"):
            item.add_marker(skip)
