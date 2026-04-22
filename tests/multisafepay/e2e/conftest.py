"""Configuration for end-to-end tests."""

import os
from collections.abc import Callable
from typing import Optional
from urllib.parse import urlparse

import pytest
from dotenv import load_dotenv

from multisafepay.client import Client, ScopedCredentialResolver
from multisafepay.sdk import Sdk
from multisafepay.transport import HTTPTransport

E2E_API_KEY_ENV = "E2E_API_KEY"
E2E_BASE_URL_ENV = "E2E_BASE_URL"
DEV_API_KEY_ENV = "API_KEY"
DEV_PARTNER_API_KEY_ENV = "PARTNER_API_KEY"
DEV_CLOUD_POS_TERMINAL_GROUP_ID_ENV = "CLOUD_POS_TERMINAL_GROUP_ID"
DEV_CUSTOM_BASE_URL_ENV = "MSP_SDK_CUSTOM_BASE_URL"
# Temporary override for strict feature examples while testapi lacks
# support for specific Cloud POS / terminal flows.
E2E_NO_SANDBOX_BASE_URL_ENV = "E2E_NO_SANDBOX_BASE_URL"
E2E_PARTNER_API_KEY_ENV = "E2E_PARTNER_API_KEY"
E2E_TERMINAL_GROUP_DEFAULT_API_KEY_ENV = (
    "E2E_TERMINAL_GROUP_API_KEY_GROUP_DEFAULT"
)
E2E_CLOUD_POS_TERMINAL_ID_ENV = "E2E_CLOUD_POS_TERMINAL_ID"

# Load .env file from the project root
load_dotenv()


def _get_e2e_api_key() -> str:
    return os.getenv(E2E_API_KEY_ENV, "").strip()


def _get_first_env(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value

    return ""


def _get_e2e_base_url() -> str:
    base_url = os.getenv(E2E_BASE_URL_ENV, "").strip()
    return base_url or Client.TEST_URL


def _get_e2e_no_sandbox_base_url() -> str:
    base_url = os.getenv(E2E_NO_SANDBOX_BASE_URL_ENV, "").strip()
    if base_url:
        return base_url

    return _get_e2e_base_url()


def _require_strict_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        msg = f"Feature-specific E2E tests require {name} (not set)"
        raise pytest.UsageError(msg)
    return value


def _resolve_terminal_group_id(
    partner_sdk: Sdk,
    terminal_id: str,
    label: str,
) -> str:
    terminal_manager = partner_sdk.get_terminal_manager()
    limit = 100
    max_pages = 10

    for page in range(1, max_pages + 1):
        response = terminal_manager.get_terminals(
            options={
                "limit": limit,
                "page": page,
            },
        )
        if (
            response.get_status_code() != 200
            or not response.get_body_success()
        ):
            raise pytest.UsageError(
                "Unable to resolve Cloud POS terminal group id: "
                "GET /json/terminals did not return a successful response",
            )

        listing = response.get_data()
        if listing is None:
            break

        terminals = listing.get_data()
        for terminal in terminals:
            listed_terminal_id = getattr(terminal, "id", None)
            terminal_code = getattr(terminal, "code", None)
            if terminal_id not in {listed_terminal_id, terminal_code}:
                continue

            group_id = getattr(terminal, "group_id", None)
            if group_id is None:
                raise pytest.UsageError(
                    f"Unable to resolve {label}: "
                    f"terminal {terminal_id} has no group_id",
                )
            return str(group_id)

        if len(terminals) < limit:
            break

    raise pytest.UsageError(
        f"Unable to resolve {label} from /json/terminals "
        f"for terminal {terminal_id}",
    )


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
def e2e_no_sandbox_base_url() -> str:
    """Return non-sandbox base URL used by strict example E2E tests."""
    return _validate_e2e_base_url(
        _get_e2e_no_sandbox_base_url(),
        E2E_NO_SANDBOX_BASE_URL_ENV,
    )


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


@pytest.fixture(scope="session")
def merchant_e2e_api_key() -> str:
    """Return merchant key for strict feature tests."""
    return _require_strict_env(E2E_API_KEY_ENV)


@pytest.fixture(scope="session")
def partner_affiliate_api_key() -> str:
    """Return partner affiliate API key used by strict feature E2E tests."""
    return _require_strict_env(E2E_PARTNER_API_KEY_ENV)


@pytest.fixture(scope="session")
def cloud_pos_terminal_group_id(
    partner_sdk: Sdk,
    cloud_pos_terminal_id: str,
) -> str:
    """Return terminal group id resolved from terminal listing data."""
    return _resolve_terminal_group_id(
        partner_sdk=partner_sdk,
        terminal_id=cloud_pos_terminal_id,
        label="Cloud POS terminal group id",
    )


@pytest.fixture(scope="session")
def cloud_pos_terminal_id() -> str:
    """Return terminal id used by Cloud POS E2E tests."""
    return _require_strict_env(E2E_CLOUD_POS_TERMINAL_ID_ENV)


@pytest.fixture(scope="session")
def cloud_pos_numeric_terminal_group_id(
    cloud_pos_terminal_group_id: str,
) -> str:
    """Return terminal group id and ensure it matches numeric example constraints."""
    if not cloud_pos_terminal_group_id.isdigit():
        raise pytest.UsageError(
            "Resolved Cloud POS terminal group id must be numeric for this "
            "example",
        )
    return cloud_pos_terminal_group_id


@pytest.fixture(scope="session")
def e2e_terminal_group_default_api_key() -> str:
    """Return terminal-group API key used by strict Cloud POS E2E tests."""
    return _require_strict_env(E2E_TERMINAL_GROUP_DEFAULT_API_KEY_ENV)


@pytest.fixture(scope="session")
def terminals_e2e_api_key() -> str:
    """Return default API key used by terminal endpoint E2E tests."""
    return _require_strict_env(DEV_API_KEY_ENV)


@pytest.fixture(scope="session")
def terminals_partner_affiliate_api_key() -> Optional[str]:
    """Return partner key for terminal endpoint E2E tests when available."""
    api_key = _get_first_env(DEV_PARTNER_API_KEY_ENV)
    return api_key or None


@pytest.fixture(scope="session")
def terminals_e2e_base_url() -> str:
    """Return dev base URL used by terminal endpoint E2E tests."""
    return _validate_e2e_base_url(
        _require_strict_env(DEV_CUSTOM_BASE_URL_ENV),
        DEV_CUSTOM_BASE_URL_ENV,
    )


@pytest.fixture(scope="session")
def terminals_sdk(
    terminals_e2e_api_key: str,
    terminals_e2e_base_url: str,
    terminals_partner_affiliate_api_key: Optional[str],
) -> Sdk:
    """Return SDK isolated for terminal endpoint E2E tests."""
    resolver_kwargs: dict = {
        "default_api_key": terminals_e2e_api_key,
    }
    if terminals_partner_affiliate_api_key:
        resolver_kwargs["partner_affiliate_api_key"] = (
            terminals_partner_affiliate_api_key
        )

    credential_resolver = ScopedCredentialResolver(**resolver_kwargs)
    sdk = Sdk(
        is_production=False,
        credential_resolver=credential_resolver,
    )
    sdk.get_client().url = terminals_e2e_base_url
    return sdk


@pytest.fixture(scope="session")
def terminals_group_id(
    terminals_sdk: Sdk,
    cloud_pos_terminal_id: str,
) -> str:
    """Return terminal group id used by terminal endpoint E2E tests."""
    group_id = _get_first_env(DEV_CLOUD_POS_TERMINAL_GROUP_ID_ENV)
    if group_id:
        return group_id

    return _resolve_terminal_group_id(
        partner_sdk=terminals_sdk,
        terminal_id=cloud_pos_terminal_id,
        label="terminal endpoint E2E group id",
    )


@pytest.fixture(scope="session")
def merchant_sdk(
    merchant_e2e_api_key: str,
    e2e_base_url: str,
) -> Sdk:
    """Return SDK configured with merchant credentials only."""
    sdk = Sdk(
        api_key=merchant_e2e_api_key,
        is_production=False,
    )
    sdk.get_client().url = e2e_base_url
    return sdk


@pytest.fixture(scope="session")
def partner_sdk(
    merchant_e2e_api_key: str,
    e2e_no_sandbox_base_url: str,
    partner_affiliate_api_key: str,
) -> Sdk:
    """Return partner-scoped SDK isolated for strict feature examples."""
    credential_resolver = ScopedCredentialResolver(
        default_api_key=merchant_e2e_api_key,
        partner_affiliate_api_key=partner_affiliate_api_key,
    )
    sdk = Sdk(
        is_production=False,
        credential_resolver=credential_resolver,
    )
    sdk.get_client().url = e2e_no_sandbox_base_url
    return sdk


@pytest.fixture(scope="session")
def cloud_pos_sdk(
    merchant_e2e_api_key: str,
    e2e_no_sandbox_base_url: str,
    cloud_pos_terminal_group_id: str,
    e2e_terminal_group_default_api_key: str,
) -> Sdk:
    """Return Cloud POS SDK isolated for strict feature examples."""
    partner_affiliate_api_key = os.getenv(E2E_PARTNER_API_KEY_ENV, "").strip()

    resolver_kwargs: dict = {
        "default_api_key": merchant_e2e_api_key,
        "terminal_group_api_keys": {
            cloud_pos_terminal_group_id: e2e_terminal_group_default_api_key,
        },
    }
    if partner_affiliate_api_key:
        resolver_kwargs["partner_affiliate_api_key"] = (
            partner_affiliate_api_key
        )

    credential_resolver = ScopedCredentialResolver(**resolver_kwargs)
    sdk = Sdk(
        is_production=False,
        credential_resolver=credential_resolver,
    )
    sdk.get_client().url = e2e_no_sandbox_base_url
    return sdk


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
