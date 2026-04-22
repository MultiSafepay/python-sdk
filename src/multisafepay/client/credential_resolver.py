# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Credential resolver contracts and default scoped resolver."""

from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass(frozen=True)
class AuthScope:
    """Auth scope selection payload for credential resolution."""

    scope: str
    group_id: Optional[str] = None


class CredentialResolver(Protocol):
    """Protocol for resolving API keys by auth scope and context."""

    def resolve(
        self: "CredentialResolver",
        auth_scope: str,
        group_id: Optional[str] = None,
    ) -> str:
        """Resolve the API key to use for a given scope and context."""


class ScopedCredentialResolver:
    """Default resolver implementation for account, partner and group scopes."""

    AUTH_SCOPE_DEFAULT = "default_account"
    AUTH_SCOPE_PARTNER_AFFILIATE = "partner_affiliate"
    AUTH_SCOPE_TERMINAL_GROUP = "terminal_group"

    def __init__(
        self: "ScopedCredentialResolver",
        default_api_key: str,
        partner_affiliate_api_key: Optional[str] = None,
        terminal_group_api_keys: Optional[dict[str, str]] = None,
    ) -> None:
        """
        Initialize a scoped credential resolver.

        Parameters
        ----------
        default_api_key (str): Fallback/default account API key.
        partner_affiliate_api_key (Optional[str]): Partner/affiliate API key.
        terminal_group_api_keys (Optional[dict[str, str]]): Mapping of
            terminal_group_id to API key.

        """
        self.default_api_key = (default_api_key or "").strip()
        self.partner_affiliate_api_key = (
            partner_affiliate_api_key or ""
        ).strip() or None
        self.terminal_group_api_keys = {
            group_id: api_key.strip()
            for group_id, api_key in (terminal_group_api_keys or {}).items()
            if api_key and api_key.strip()
        }

        if (
            not self.default_api_key
            and self.partner_affiliate_api_key is None
            and not self.terminal_group_api_keys
        ):
            raise ValueError(
                "ScopedCredentialResolver requires at least one API key.",
            )

    def resolve(
        self: "ScopedCredentialResolver",
        auth_scope: str,
        group_id: Optional[str] = None,
    ) -> str:
        """Resolve API key for the given scope and auth context."""
        if auth_scope == self.AUTH_SCOPE_TERMINAL_GROUP:
            if not group_id:
                raise ValueError(
                    "Missing terminal_group_id in auth scope.",
                )
            api_key = self.terminal_group_api_keys.get(group_id)
            if not api_key:
                raise ValueError(
                    "No API key configured for terminal_group_id "
                    f"'{group_id}'.",
                )
            return api_key

        if auth_scope == self.AUTH_SCOPE_PARTNER_AFFILIATE:
            api_key = self.partner_affiliate_api_key or self.default_api_key
            if not api_key:
                raise ValueError(
                    "No API key configured for partner_affiliate scope.",
                )
            return api_key

        if not self.default_api_key:
            raise ValueError("No API key configured for default scope.")

        return self.default_api_key
