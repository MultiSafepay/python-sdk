# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.capture.request.capture_request import (
    CaptureRequest,
)


def test_initialization_with_no_data():
    """
    Test the initialization of CaptureRequest with no data.

    This test ensures that when a CaptureRequest object is initialized
    without any parameters, its status and reason attributes are None.

    """
    capture_request = CaptureRequest()
    assert capture_request.status is None
    assert capture_request.reason is None


def test_initialization_with_valid_data():
    """
    Test the initialization of CaptureRequest with valid data.

    This test ensures that when a CaptureRequest object is initialized
    with status and reason parameters, these attributes are set correctly.


    """
    capture_request = CaptureRequest(status="completed", reason="valid_reason")
    assert capture_request.status == "completed"
    assert capture_request.reason == "valid_reason"


def test_add_status_with_valid_data():
    """
    Test adding a valid status to CaptureRequest.

    This test ensures that the add_status method correctly sets the status
    attribute when provided with a valid status.


    """
    capture_request = CaptureRequest()
    capture_request_updated = capture_request.add_status("completed")
    assert capture_request.status == "completed"
    assert isinstance(capture_request_updated, CaptureRequest)


def test_add_reason_with_valid_data():
    """
    Test adding a valid reason to CaptureRequest.

    This test ensures that the add_reason method correctly sets the reason
    attribute when provided with a valid reason.


    """
    capture_request = CaptureRequest()
    capture_request_updated = capture_request.add_reason("valid_reason")
    assert capture_request.reason == "valid_reason"
    assert isinstance(capture_request_updated, CaptureRequest)
