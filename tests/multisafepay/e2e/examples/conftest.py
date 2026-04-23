"""Example-specific E2E fixtures and selective skip behavior."""

import os
from typing import Optional
from urllib.parse import urlparse

import pytest

from multisafepay.client import ScopedCredentialResolver
from multisafepay.sdk import Sdk

DEFAULT_E2E_API_KEY_ENV = "E2E_API_KEY"
TERMINAL_DEFAULT_API_KEY_ENV = "API_KEY"
TERMINAL_PARTNER_API_KEY_ENV = "PARTNER_API_KEY"
TERMINAL_CUSTOM_BASE_URL_ENV = "MSP_SDK_CUSTOM_BASE_URL"
TERMINAL_E2E_TERMINAL_ID_ENV = "E2E_CLOUD_POS_TERMINAL_ID"
TERMINAL_E2E_NODE_PREFIXES = (
    "tests/multisafepay/e2e/examples/terminal_manager/",
    "tests/multisafepay/e2e/examples/terminal_group_manager/",
)


def _get_first_env(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value

    return ""


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        msg = f"Feature-specific E2E tests require {name} (not set)"
        raise pytest.UsageError(msg)
    return value


def _has_terminal_e2e_env() -> bool:
    return bool(
        _get_first_env(TERMINAL_DEFAULT_API_KEY_ENV)
        and _get_first_env(TERMINAL_CUSTOM_BASE_URL_ENV)
        and _get_first_env(TERMINAL_E2E_TERMINAL_ID_ENV),
    )


def _validate_base_url(base_url: str, env_name: str) -> str:
    parsed = urlparse(base_url)
    if parsed.scheme != "https" or not parsed.netloc:
        msg = f"{env_name} must be a valid https URL"
        raise pytest.UsageError(msg)

    path = parsed.path.rstrip("/")
    normalized_path = "/" if not path else f"{path}/"
    return f"{parsed.scheme}://{parsed.netloc}{normalized_path}"


def _resolve_terminal_group_id(
    terminals_sdk: Sdk,
    terminal_id: str,
    label: str,
) -> str:
    terminal_manager = terminals_sdk.get_terminal_manager()
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
                "Unable to resolve terminal group id: "
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


@pytest.fixture(scope="session")
def terminals_terminal_id() -> str:
    """Return terminal id used to resolve a valid terminal group."""
    return _require_env(TERMINAL_E2E_TERMINAL_ID_ENV)


@pytest.fixture(scope="session")
def terminals_e2e_api_key() -> str:
    """Return default API key used by terminal endpoint E2E tests."""
    return _require_env(TERMINAL_DEFAULT_API_KEY_ENV)


@pytest.fixture(scope="session")
def terminals_partner_affiliate_api_key() -> Optional[str]:
    """Return partner key for terminal endpoint E2E tests when available."""
    api_key = _get_first_env(TERMINAL_PARTNER_API_KEY_ENV)
    return api_key or None


@pytest.fixture(scope="session")
def terminals_e2e_base_url() -> str:
    """Return custom base URL used by terminal endpoint E2E tests."""
    return _validate_base_url(
        _require_env(TERMINAL_CUSTOM_BASE_URL_ENV),
        TERMINAL_CUSTOM_BASE_URL_ENV,
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
    terminals_terminal_id: str,
) -> str:
    """Return terminal group id used by terminal endpoint E2E tests."""
    return _resolve_terminal_group_id(
        terminals_sdk=terminals_sdk,
        terminal_id=terminals_terminal_id,
        label="terminal endpoint E2E group id",
    )


def pytest_collection_modifyitems(
    config: pytest.Config,  # noqa: ARG001
    items: list[pytest.Item],
) -> None:
    """Skip example E2E tests when the required credentials are missing."""
    has_default_e2e = bool(os.getenv(DEFAULT_E2E_API_KEY_ENV, "").strip())
    has_terminal_e2e = _has_terminal_e2e_env()

    if has_default_e2e and has_terminal_e2e:
        return

    default_skip = pytest.mark.skip(
        reason=f"E2E tests require {DEFAULT_E2E_API_KEY_ENV} (not set)",
    )
    terminal_skip = pytest.mark.skip(
        reason=(
            "Terminal endpoint E2E tests require API_KEY, "
            "MSP_SDK_CUSTOM_BASE_URL, and E2E_CLOUD_POS_TERMINAL_ID "
            "(not set)"
        ),
    )
    for item in items:
        if item.nodeid.startswith(TERMINAL_E2E_NODE_PREFIXES):
            if has_terminal_e2e:
                continue
            item.add_marker(terminal_skip)
            continue

        if not has_default_e2e:
            item.add_marker(default_skip)
