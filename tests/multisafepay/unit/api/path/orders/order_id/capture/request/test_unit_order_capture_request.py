# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from multisafepay.api.paths.orders.order_id.capture.request.capture_request import (
    CaptureOrderRequest,
)


def test_initializes_capture_order_request_with_default_values():
    """
    Test that a CaptureOrderRequest object is correctly initialized with default values.
    """
    request = CaptureOrderRequest(
        amount=1000,
        new_order_id="ORD123",
        new_order_status="completed",
        invoice_id="INV123",
        carrier="DHL",
        reason="Customer request",
        tracktrace_code="TRACK123",
        description="This is a test description.",
    )

    assert request.amount == 1000
    assert request.new_order_id == "ORD123"
    assert request.new_order_status == "completed"
    assert request.invoice_id == "INV123"
    assert request.carrier == "DHL"
    assert request.reason == "Customer request"
    assert request.tracktrace_code == "TRACK123"
    assert request.description == "This is a test description."


def test_initializes_capture_order_request_with_empty_values():
    """
    Test that a CaptureOrderRequest object is correctly initialized with empty values.
    """
    request = CaptureOrderRequest()

    assert request.amount is None
    assert request.new_order_id is None
    assert request.new_order_status is None
    assert request.invoice_id is None
    assert request.carrier is None
    assert request.reason is None
    assert request.tracktrace_code is None
    assert request.description is None


def test_add_amount_updates_value():
    """
    Test that the add_amount method updates the amount attribute to the given value.
    """
    request = CaptureOrderRequest()
    request_updated = request.add_amount(500)

    assert request.amount == 500
    assert isinstance(request_updated, CaptureOrderRequest)


def test_add_new_order_id_updates_value():
    """
    Test that the add_new_order_id method updates the new_order_id attribute to the given value.
    """
    request = CaptureOrderRequest()
    request_updated = request.add_new_order_id("order123")

    assert request.new_order_id == "order123"
    assert isinstance(request_updated, CaptureOrderRequest)


def test_add_new_order_status_updates_value():
    """
    Test that the add_new_order_status method updates the new_order_status attribute
    to the given value.
    """
    request = CaptureOrderRequest()
    request_updated = request.add_new_order_status("shipped")

    assert request.new_order_status == "shipped"
    assert isinstance(request_updated, CaptureOrderRequest)


def test_add_invoice_id_updates_value():
    """
    Test that the add_invoice_id method updates the invoice_id attribute to the given value.
    """
    request = CaptureOrderRequest()
    request_updated = request.add_invoice_id("invoice123")

    assert request.invoice_id == "invoice123"
    assert isinstance(request_updated, CaptureOrderRequest)


def test_add_carrier_updates_value():
    """
    Test that the add_carrier method updates the carrier attribute to the given value.
    """
    request = CaptureOrderRequest()
    request_updated = request.add_carrier("DHL")

    assert request.carrier == "DHL"
    assert isinstance(request_updated, CaptureOrderRequest)


def test_add_reason_updates_value():
    """
    Test that the add_reason method updates the reason attribute to the given value.
    """
    request = CaptureOrderRequest()
    request_updated = request.add_reason("Customer request")

    assert request.reason == "Customer request"
    assert isinstance(request_updated, CaptureOrderRequest)


def test_add_tracktrace_code_updates_value():
    """
    Test that the add_tracktrace_code method updates the tracktrace_code attribute to the given value.
    """
    request = CaptureOrderRequest()
    request_updated = request.add_tracktrace_code("TRACK123")

    assert request.tracktrace_code == "TRACK123"
    assert isinstance(request_updated, CaptureOrderRequest)


def test_description_updates_value():
    """
    Test that the add_description method updates the description attribute to the given value.
    """
    request = CaptureOrderRequest()
    request_updated = request.add_description("This is a test description.")

    assert request.description == "This is a test description."
    assert isinstance(request_updated, CaptureOrderRequest)
