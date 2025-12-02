# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.plugin import (
    Plugin,
)


def test_initializes_plugin_correctly():
    """Tests that the Plugin object is initialized correctly with the given values."""
    plugin = Plugin(
        plugin_version="1.0.0",
        shop_version="1.0.0",
        partner="TestPartner",
        shop="TestShop",
        shop_root_url="https://example.com",
    )

    assert plugin.plugin_version == "1.0.0"
    assert plugin.shop == "TestShop"
    assert plugin.shop_version == "1.0.0"
    assert plugin.partner == "TestPartner"
    assert plugin.shop_root_url == "https://example.com"


def test_initializes_plugin_with_empty_values():
    """Tests that the Plugin object is initialized with None values when no arguments are provided."""
    plugin = Plugin()
    assert plugin.plugin_version is None
    assert plugin.shop is None
    assert plugin.shop_version is None
    assert plugin.plugin_version is None
    assert plugin.partner is None
    assert plugin.shop_root_url is None


def test_add_plugin_version_updates_value():
    """Tests that the add_plugin_version method updates the plugin_version field correctly."""
    plugin = Plugin()
    plugin_updated = plugin.add_plugin_version("1.0.0")

    assert plugin.plugin_version == "1.0.0"
    assert isinstance(plugin_updated, Plugin)


def test_add_shop_updates_value():
    """Tests that the add_shop method updates the shop field correctly."""
    plugin = Plugin()
    plugin_updated = plugin.add_shop("TestShop")

    assert plugin.shop == "TestShop"
    assert isinstance(plugin_updated, Plugin)


def test_add_shop_version_updates_value():
    """Tests that the add_shop_version method updates the shop_version field correctly."""
    plugin = Plugin()
    plugin_updated = plugin.add_shop_version("1.0.0")

    assert plugin.shop_version == "1.0.0"
    assert isinstance(plugin_updated, Plugin)


def test_add_partner_updates_value():
    """Tests that the add_partner method updates the partner field correctly."""
    plugin = Plugin()
    plugin_updated = plugin.add_partner("TestPartner")

    assert plugin.partner == "TestPartner"
    assert isinstance(plugin_updated, Plugin)


def test_add_shop_root_url_updates_value():
    """Tests that the add_shop_root_url method updates the shop_root_url field correctly."""
    plugin = Plugin()
    plugin_updated = plugin.add_shop_root_url(
        "https://example.com",
    )

    assert plugin.shop_root_url == "https://example.com"
    assert isinstance(plugin_updated, Plugin)
