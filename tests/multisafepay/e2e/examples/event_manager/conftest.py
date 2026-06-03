"""Event-manager-specific E2E fixtures and selective skip behavior."""

import os
from urllib.parse import urlparse

import pytest

from multisafepay.client import ScopedCredentialResolver
from multisafepay.client.client import Client
from multisafepay.client.credential_resolver import AuthScope
from multisafepay.sdk import Sdk

EVENT_MANAGER_E2E_NODE_PREFIXES = (
    "tests/multisafepay/e2e/examples/event_manager/",
)
DEFAULT_API_KEY_ENVS = ("E2E_API_KEY", "API_KEY")
PARTNER_API_KEY_ENVS = ("E2E_PARTNER_API_KEY", "PARTNER_API_KEY")
TERMINAL_GROUP_API_KEY_ENVS = (
    "E2E_TERMINAL_GROUP_API_KEY_GROUP_DEFAULT",
    "TERMINAL_GROUP_API_KEY_GROUP_DEFAULT",
)
TERMINAL_GROUP_ID_ENVS = ("CLOUD_POS_TERMINAL_GROUP_ID",)
TERMINAL_ID_ENVS = ("E2E_CLOUD_POS_TERMINAL_ID", "CLOUD_POS_TERMINAL_ID")
BASE_URL_ENVS = ("E2E_NO_SANDBOX_BASE_URL", "MSP_SDK_CUSTOM_BASE_URL")


def _get_first_env(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value

    return ""


def _require_first_env(*names: str) -> str:
    value = _get_first_env(*names)
    if value:
        return value

    msg = f"SSE E2E tests require one of: {', '.join(names)}"
    raise pytest.UsageError(msg)


def _validate_base_url(base_url: str, *env_names: str) -> str:
    parsed = urlparse(base_url)
    if parsed.scheme != "https" or not parsed.netloc:
        msg = f"{', '.join(env_names)} must be a valid https URL"
        raise pytest.UsageError(msg)

    path = parsed.path.rstrip("/")
    normalized_path = "/" if not path else f"{path}/"
    return f"{parsed.scheme}://{parsed.netloc}{normalized_path}"


def _has_event_manager_e2e_env() -> bool:
    has_base = bool(
        _get_first_env(*DEFAULT_API_KEY_ENVS)
        and _get_first_env(*TERMINAL_GROUP_API_KEY_ENVS)
        and _get_first_env(*TERMINAL_ID_ENVS)
        and _get_first_env(*BASE_URL_ENVS),
    )
    if not has_base:
        return False

    return bool(
        _get_first_env(*TERMINAL_GROUP_ID_ENVS)
        or _get_first_env(*PARTNER_API_KEY_ENVS),
    )


def _resolve_terminal_group_id(
    base_url: str,
    default_api_key: str,
    partner_api_key: str,
    terminal_id: str,
) -> str:
    credential_resolver = ScopedCredentialResolver(
        default_api_key=default_api_key,
        partner_affiliate_api_key=partner_api_key,
    )
    sdk = Sdk(
        is_production=False,
        credential_resolver=credential_resolver,
    )
    sdk.get_client().url = base_url

    limit = 100
    max_pages = 10
    for page in range(1, max_pages + 1):
        response = sdk.get_client().create_get_request(
            "json/terminals",
            params={
                "limit": limit,
                "page": page,
            },
            auth_scope=AuthScope(
                scope=Client.AUTH_SCOPE_PARTNER_AFFILIATE,
            ),
        )
        if (
            response.get_status_code() != 200
            or not response.get_body_success()
        ):
            raise pytest.UsageError(
                "Unable to resolve Cloud POS terminal group id: "
                "GET /json/terminals did not return a successful response",
            )

        listing = response.get_body_data()
        if not isinstance(listing, list) or not listing:
            break

        for terminal in listing:
            listed_terminal_id = terminal.get("id")
            terminal_code = terminal.get("code")
            if terminal_id not in {listed_terminal_id, terminal_code}:
                continue

            group_id = terminal.get("group_id")
            if group_id is None:
                raise pytest.UsageError(
                    f"Unable to resolve Cloud POS terminal group id: "
                    f"terminal {terminal_id} has no group_id",
                )
            return str(group_id)

        if len(listing) < limit:
            break

    raise pytest.UsageError(
        f"Unable to resolve Cloud POS terminal group id for terminal {terminal_id}",
    )


@pytest.fixture(scope="session")
def cloud_pos_terminal_id() -> str:
    """Return terminal id used by SSE E2E tests."""
    return _require_first_env(*TERMINAL_ID_ENVS)


@pytest.fixture(scope="session")
def cloud_pos_base_url() -> str:
    """Return dev-backed base URL used by SSE E2E tests."""
    return _validate_base_url(
        _require_first_env(*BASE_URL_ENVS),
        *BASE_URL_ENVS,
    )


@pytest.fixture(scope="session")
def cloud_pos_terminal_group_id(
    cloud_pos_base_url: str,
    cloud_pos_terminal_id: str,
) -> str:
    """Return terminal group id from env or resolve it via /json/terminals."""
    explicit_group_id = _get_first_env(*TERMINAL_GROUP_ID_ENVS)
    if explicit_group_id:
        return explicit_group_id

    return _resolve_terminal_group_id(
        base_url=cloud_pos_base_url,
        default_api_key=_require_first_env(*DEFAULT_API_KEY_ENVS),
        partner_api_key=_require_first_env(*PARTNER_API_KEY_ENVS),
        terminal_id=cloud_pos_terminal_id,
    )


@pytest.fixture(scope="session")
def cloud_pos_events_sdk(
    cloud_pos_base_url: str,
    cloud_pos_terminal_group_id: str,
) -> Sdk:
    """Return SDK configured for Cloud POS creation plus SSE subscription."""
    credential_resolver = ScopedCredentialResolver(
        default_api_key=_require_first_env(*DEFAULT_API_KEY_ENVS),
        terminal_group_api_keys={
            cloud_pos_terminal_group_id: _require_first_env(
                *TERMINAL_GROUP_API_KEY_ENVS,
            ),
        },
    )
    sdk = Sdk(
        is_production=False,
        credential_resolver=credential_resolver,
    )
    sdk.get_client().url = cloud_pos_base_url
    return sdk


def pytest_collection_modifyitems(
    config: pytest.Config,  # noqa: ARG001
    items: list[pytest.Item],
) -> None:
    """Skip SSE E2E tests when the required credentials are missing."""
    if _has_event_manager_e2e_env():
        return

    skip = pytest.mark.skip(
        reason=(
            "SSE E2E tests require E2E_API_KEY or API_KEY, "
            "E2E_TERMINAL_GROUP_API_KEY_GROUP_DEFAULT or "
            "TERMINAL_GROUP_API_KEY_GROUP_DEFAULT, "
            "E2E_CLOUD_POS_TERMINAL_ID or CLOUD_POS_TERMINAL_ID, "
            "E2E_NO_SANDBOX_BASE_URL or MSP_SDK_CUSTOM_BASE_URL, "
            "and either CLOUD_POS_TERMINAL_GROUP_ID or PARTNER_API_KEY"
        ),
    )
    for item in items:
        if item.nodeid.startswith(EVENT_MANAGER_E2E_NODE_PREFIXES):
            item.add_marker(skip)
