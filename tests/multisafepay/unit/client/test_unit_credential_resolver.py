# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Unit tests for scoped credential resolver behavior."""

import pytest

from multisafepay.client.credential_resolver import ScopedCredentialResolver

DEFAULT_API_KEY = "default_api_key"
PARTNER_API_KEY = "partner_api_key"
TERMINAL_GROUP_ID = "Default"
TERMINAL_GROUP_API_KEY = "terminal_group_api_key"
MISSING_GROUP_ID_ERROR = "Missing terminal_group_id"
NO_DEFAULT_SCOPE_ERROR = "No API key configured for default scope"


def _resolver_with_terminal_group() -> ScopedCredentialResolver:
    """Create resolver fixture data for terminal-group scope tests."""
    return ScopedCredentialResolver(
        default_api_key=DEFAULT_API_KEY,
        terminal_group_api_keys={
            TERMINAL_GROUP_ID: TERMINAL_GROUP_API_KEY,
        },
    )


def test_rejects_resolver_without_any_api_key() -> None:
    """Require at least one API key across all resolver sources."""
    with pytest.raises(
        ValueError,
        match="requires at least one API key",
    ):
        ScopedCredentialResolver(default_api_key="")


def test_resolves_default_scope_with_default_api_key() -> None:
    """Resolve default scope using the configured default API key."""
    resolver = ScopedCredentialResolver(default_api_key=DEFAULT_API_KEY)

    assert (
        resolver.resolve(ScopedCredentialResolver.AUTH_SCOPE_DEFAULT)
        == DEFAULT_API_KEY
    )


def test_resolves_partner_scope_with_partner_api_key() -> None:
    """Prefer partner key for partner_affiliate scope."""
    resolver = ScopedCredentialResolver(
        default_api_key=DEFAULT_API_KEY,
        partner_affiliate_api_key=PARTNER_API_KEY,
    )

    assert (
        resolver.resolve(ScopedCredentialResolver.AUTH_SCOPE_PARTNER_AFFILIATE)
        == PARTNER_API_KEY
    )


def test_resolves_terminal_group_scope_with_group_key() -> None:
    """Resolve terminal_group scope using group-specific API key mapping."""
    resolver = _resolver_with_terminal_group()

    assert (
        resolver.resolve(
            ScopedCredentialResolver.AUTH_SCOPE_TERMINAL_GROUP,
            group_id=TERMINAL_GROUP_ID,
        )
        == TERMINAL_GROUP_API_KEY
    )


def test_raises_for_terminal_group_scope_without_group_id() -> None:
    """Reject terminal_group scope when group_id is missing."""
    resolver = _resolver_with_terminal_group()

    with pytest.raises(ValueError, match=MISSING_GROUP_ID_ERROR):
        resolver.resolve(ScopedCredentialResolver.AUTH_SCOPE_TERMINAL_GROUP)


def test_raises_for_default_scope_without_default_key() -> None:
    """Reject default scope when no default key is configured."""
    resolver = ScopedCredentialResolver(
        default_api_key="",
        partner_affiliate_api_key=PARTNER_API_KEY,
    )

    with pytest.raises(
        ValueError,
        match=NO_DEFAULT_SCOPE_ERROR,
    ):
        resolver.resolve(ScopedCredentialResolver.AUTH_SCOPE_DEFAULT)


def test_resolves_partner_scope_falls_back_to_default_key() -> None:
    """Fall back to default_api_key for partner scope when no partner key."""
    resolver = ScopedCredentialResolver(default_api_key=DEFAULT_API_KEY)

    assert (
        resolver.resolve(ScopedCredentialResolver.AUTH_SCOPE_PARTNER_AFFILIATE)
        == DEFAULT_API_KEY
    )


def test_raises_for_unknown_terminal_group_id() -> None:
    """Reject terminal_group scope when the group_id is not configured."""
    resolver = _resolver_with_terminal_group()

    with pytest.raises(ValueError, match="No API key configured"):
        resolver.resolve(
            ScopedCredentialResolver.AUTH_SCOPE_TERMINAL_GROUP,
            group_id="unknown_group",
        )


def test_strips_whitespace_from_api_keys() -> None:
    """Strip leading/trailing whitespace from provided API keys."""
    resolver = ScopedCredentialResolver(
        default_api_key="  key_with_spaces  ",
        partner_affiliate_api_key="  partner_spaces  ",
    )

    assert (
        resolver.resolve(ScopedCredentialResolver.AUTH_SCOPE_DEFAULT)
        == "key_with_spaces"
    )
    assert (
        resolver.resolve(ScopedCredentialResolver.AUTH_SCOPE_PARTNER_AFFILIATE)
        == "partner_spaces"
    )
