"""
Unit tests for transport selection behavior.

We validate the three main behaviors and their combinations:

- Injected transport always wins (even if `requests` is missing).
- Without an injected transport, the SDK defaults to RequestsTransport.
- Without an injected transport and without `requests`, the SDK fails fast with a clear error.
"""

from __future__ import annotations

from typing import NoReturn
from unittest.mock import Mock

import pytest

from multisafepay.sdk import Sdk
from tests.support.mock_transport import MockTransport


def test_injected_transport_wins_when_requests_installed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Injected transport must be used; RequestsTransport must not be instantiated."""
    import multisafepay.client.client as client_module

    def _boom() -> NoReturn:
        raise AssertionError("RequestsTransport() should not be called")

    monkeypatch.setattr(client_module, "RequestsTransport", _boom)

    injected_transport = MockTransport()
    sdk = Sdk(
        api_key="test_api_key",
        is_production=False,
        transport=injected_transport,
    )
    assert sdk.client.transport is injected_transport


def test_injected_transport_wins_when_requests_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Injected transport must be used even if `requests` is missing."""
    import multisafepay.client.client as client_module
    from multisafepay.transport import requests_transport

    monkeypatch.setattr(requests_transport, "_HAS_REQUESTS", False)
    monkeypatch.setattr(
        requests_transport,
        "_REQUESTS_IMPORT_ERROR",
        ModuleNotFoundError("No module named 'requests'"),
    )

    def _boom() -> NoReturn:
        raise AssertionError("RequestsTransport() should not be called")

    monkeypatch.setattr(client_module, "RequestsTransport", _boom)

    injected_transport = MockTransport()
    sdk = Sdk(
        api_key="test_api_key",
        is_production=False,
        transport=injected_transport,
    )
    assert sdk.client.transport is injected_transport


def test_defaults_to_requests_transport_when_not_injected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When no transport is injected, the SDK should default to RequestsTransport."""
    import multisafepay.client.client as client_module

    sentinel_transport = object()
    requests_transport_factory = Mock(return_value=sentinel_transport)
    monkeypatch.setattr(
        client_module,
        "RequestsTransport",
        requests_transport_factory,
    )

    sdk = Sdk(api_key="test_api_key", is_production=False)
    assert sdk.client.transport is sentinel_transport
    requests_transport_factory.assert_called_once_with()


def test_raises_clear_error_when_requests_missing_and_not_injected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When no transport is injected and `requests` is missing, the SDK should fail fast."""
    from multisafepay.transport import requests_transport

    monkeypatch.setattr(requests_transport, "_HAS_REQUESTS", False)
    monkeypatch.setattr(
        requests_transport,
        "_REQUESTS_IMPORT_ERROR",
        ModuleNotFoundError("No module named 'requests'"),
    )

    with pytest.raises(
        ModuleNotFoundError,
        match="multisafepay\\[requests\\]",
    ):
        Sdk(api_key="test_api_key", is_production=False)
