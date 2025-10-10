# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.gateway_info.qr_code import (
    QrCode,
)


def test_initializes_qr_code_correctly():
    """
    Test that the QrCode object is initialized correctly with given values.
    """
    qr_code = QrCode(
        qr_size=200,
        allow_multiple=True,
        allow_change_amount=False,
        min_amount=100,
        max_amount=500,
    )

    assert qr_code.qr_size == 200
    assert qr_code.allow_multiple is True
    assert qr_code.allow_change_amount is False
    assert qr_code.min_amount == 100
    assert qr_code.max_amount == 500


def test_initializes_qr_code_with_empty_values():
    """
    Test that the QrCode object is initialized correctly with empty values.
    """
    qr_code = QrCode()

    assert qr_code.qr_size is None
    assert qr_code.allow_multiple is None
    assert qr_code.allow_change_amount is None
    assert qr_code.min_amount is None
    assert qr_code.max_amount is None


def test_add_qr_size_updates_value():
    """
    Test that the add_qr_size method updates the qr_size attribute.
    """
    request = QrCode()
    request_updated = request.add_qr_size(200)

    assert request.qr_size == 200
    assert isinstance(request_updated, QrCode)


def test_add_allow_multiple_updates_value():
    """
    Test that the add_allow_multiple method updates the allow_multiple attribute.
    """
    request = QrCode()
    request_updated = request.add_allow_multiple(True)

    assert request.allow_multiple is True
    assert isinstance(request_updated, QrCode)


def test_add_allow_change_amount_updates_value():
    """
    Test that the add_allow_change_amount method updates the allow_change_amount attribute.
    """
    request = QrCode()
    request_updated = request.add_allow_change_amount(False)

    assert request.allow_change_amount is False
    assert isinstance(request_updated, QrCode)


def test_add_min_amount_updates_value():
    """
    Test that the add_min_amount method updates the min_amount attribute.
    """
    request = QrCode()
    request_updated = request.add_min_amount(100)

    assert request.min_amount == 100
    assert isinstance(request_updated, QrCode)


def test_add_max_amount_updates_value():
    """
    Test that the add_max_amount method updates the max_amount attribute.
    """
    request = QrCode()
    request_updated = request.add_max_amount(500)

    assert request.max_amount == 500
    assert isinstance(request_updated, QrCode)
