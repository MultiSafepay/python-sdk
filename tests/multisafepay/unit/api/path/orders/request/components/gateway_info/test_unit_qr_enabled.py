# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.gateway_info.qr_enabled import (
    QrEnabled,
)


def test_initializes_qr_enabled_correctly():
    """Test that the QrEnabled object is initialized correctly with a given value."""
    qr_enabled = QrEnabled(qr_enabled=True)

    assert qr_enabled.qr_enabled is True


def test_initializes_qr_enabled_with_empty_value():
    """Test that the QrEnabled object is initialized correctly with an empty value."""
    qr_enabled = QrEnabled()

    assert qr_enabled.qr_enabled is None


def test_add_qr_enabled_updates_value():
    """Test that the add_qr_enabled method updates the qr_enabled attribute to True."""
    request = QrEnabled()
    request_updated = request.add_qr_enabled(True)

    assert request.qr_enabled is True
    assert isinstance(request_updated, QrEnabled)


def test_add_qr_enabled_with_false_value():
    """Test that the add_qr_enabled method updates the qr_enabled attribute to False."""
    request = QrEnabled()
    request_updated = request.add_qr_enabled(False)

    assert request.qr_enabled is False
    assert isinstance(request_updated, QrEnabled)
