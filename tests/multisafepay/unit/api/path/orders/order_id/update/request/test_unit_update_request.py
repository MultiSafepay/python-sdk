# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.order_id.update.request.update_request import (
    UpdateOrderRequest,
)


def test_initializes_update_order_request_correctly():
    """Test that an UpdateOrderRequest object is correctly initialized with given values."""
    request = UpdateOrderRequest(
        tracktrace_code="123ABC",
        tracktrace_url="http://example.com/track",
        carrier="CarrierName",
        ship_date="2023-10-01",
        reason="Update reason",
        invoice_id="INV123",
        invoice_url="http://example.com/invoice",
        po_number="PO123",
        status="Shipped",
        exclude_order=True,
        extend_expiration=True,
    )

    assert request.tracktrace_code == "123ABC"
    assert request.tracktrace_url == "http://example.com/track"
    assert request.carrier == "CarrierName"
    assert request.ship_date == "2023-10-01"
    assert request.reason == "Update reason"
    assert request.invoice_id == "INV123"
    assert request.invoice_url == "http://example.com/invoice"
    assert request.po_number == "PO123"
    assert request.status == "Shipped"
    assert request.exclude_order is True
    assert request.extend_expiration is True


def test_initializes_update_order_request_with_empty_values():
    """Test that an UpdateOrderRequest object is correctly initialized with empty values."""
    request = UpdateOrderRequest()

    assert request.tracktrace_code is None
    assert request.tracktrace_url is None
    assert request.carrier is None
    assert request.ship_date is None
    assert request.reason is None
    assert request.invoice_id is None
    assert request.invoice_url is None
    assert request.po_number is None
    assert request.status is None
    assert request.exclude_order is None
    assert request.extend_expiration is None


def test_add_tracktrace_code_updates_value():
    """Test that the add_tracktrace_code method updates the tracktrace_code attribute."""
    request = UpdateOrderRequest()
    request_updated = request.add_tracktrace_code("123ABC")

    assert request.tracktrace_code == "123ABC"
    assert isinstance(request_updated, UpdateOrderRequest)


def test_add_tracktrace_url_updates_value():
    """Test that the add_tracktrace_url method updates the tracktrace_url attribute."""
    request = UpdateOrderRequest()
    request_updated = request.add_tracktrace_url("http://example.com/track")

    assert request.tracktrace_url == "http://example.com/track"
    assert isinstance(request_updated, UpdateOrderRequest)


def test_add_carrier_updates_value():
    """Test that the add_carrier method updates the carrier attribute."""
    request = UpdateOrderRequest()
    request_updated = request.add_carrier("CarrierName")

    assert request.carrier == "CarrierName"
    assert isinstance(request_updated, UpdateOrderRequest)


def test_add_ship_date_updates_value():
    """Test that the add_ship_date method updates the ship_date attribute."""
    request = UpdateOrderRequest()
    request_updated = request.add_ship_date("2023-10-01")

    assert request.ship_date == "2023-10-01"
    assert isinstance(request_updated, UpdateOrderRequest)


def test_add_reason_updates_value():
    """Test that the add_reason method updates the reason attribute."""
    request = UpdateOrderRequest()
    request_updated = request.add_reason("Update reason")

    assert request.reason == "Update reason"
    assert isinstance(request_updated, UpdateOrderRequest)


def test_add_invoice_id_updates_value():
    """Test that the add_invoice_id method updates the invoice_id attribute."""
    request = UpdateOrderRequest()
    request_updated = request.add_invoice_id("INV123")

    assert request.invoice_id == "INV123"
    assert isinstance(request_updated, UpdateOrderRequest)


def test_add_invoice_url_updates_value():
    """Test that the add_invoice_url method updates the invoice_url attribute."""
    request = UpdateOrderRequest()
    request_updated = request.add_invoice_url("http://example.com/invoice")

    assert request.invoice_url == "http://example.com/invoice"
    assert isinstance(request_updated, UpdateOrderRequest)


def test_add_po_number_updates_value():
    """Test that the add_po_number method updates the po_number attribute."""
    request = UpdateOrderRequest()
    request_updated = request.add_po_number("PO123")

    assert request.po_number == "PO123"
    assert isinstance(request_updated, UpdateOrderRequest)


def test_add_status_updates_value():
    """Test that the add_status method updates the status attribute."""
    request = UpdateOrderRequest()
    request_updated = request.add_status("Shipped")

    assert request.status == "Shipped"
    assert isinstance(request_updated, UpdateOrderRequest)


def test_add_exclude_order_updates_value():
    """Test that the add_exclude_order method updates the exclude_order attribute."""
    request = UpdateOrderRequest()
    request_updated = request.add_exclude_order(True)

    assert request.exclude_order is True
    assert isinstance(request_updated, UpdateOrderRequest)


def test_add_extend_expiration_updates_value():
    """Test that the add_extend_expiration method updates the extend_expiration attribute."""
    request = UpdateOrderRequest()
    request_updated = request.add_extend_expiration(True)

    assert request.extend_expiration is True
    assert isinstance(request_updated, UpdateOrderRequest)
