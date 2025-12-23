"""Configuration for end-to-end tests."""

import os

import pytest


def pytest_collection_modifyitems(
    config: pytest.Config,  # noqa: ARG001
    items: list[pytest.Item],
) -> None:
    """
    Skip all e2e tests when API_KEY is missing.

    These tests perform real API calls. In most local/CI environments the secret
    isn't present, so we prefer a clean skip over hard errors during fixture setup.
    """
    api_key = os.getenv("API_KEY")
    if api_key and api_key.strip():
        return

    skip = pytest.mark.skip(reason="E2E tests require API_KEY (not set)")
    for item in items:
        # This hook runs for the whole session (all collected tests), even when
        # this conftest is only loaded due to e2e tests being present/deselected.
        # Ensure we only affect e2e tests.
        if item.nodeid.startswith("tests/multisafepay/e2e/"):
            item.add_marker(skip)
