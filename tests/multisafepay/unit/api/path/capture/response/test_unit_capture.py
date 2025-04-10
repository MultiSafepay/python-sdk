# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.paths.capture.response.capture import CancelReservation


def test_initialization_with_no_data():
    """
    Test that the CancelReservation object initializes correctly with no data.

    This test verifies that the CancelReservation object initializes with None
    for all attributes when no data is provided.


    """
    cancel_reservation = CancelReservation()
    assert cancel_reservation.order_id is None
    assert cancel_reservation.success is None
    assert cancel_reservation.transaction_id is None


def test_initialization_with_valid_data():
    """
    Test that the CancelReservation object initializes correctly with valid data.

    This test verifies that the CancelReservation object initializes with the correct
    values for all attributes when valid data is provided.


    """
    cancel_reservation = CancelReservation(
        order_id="12345",
        success=True,
        transaction_id="67890",
    )
    assert cancel_reservation.order_id == "12345"
    assert cancel_reservation.success is True
    assert cancel_reservation.transaction_id == "67890"


def test_from_dict_with_valid_data():
    """
    Test that the from_dict method initializes a CancelReservation object with valid data.

    This test verifies that the from_dict method correctly creates a CancelReservation
    object from a dictionary containing valid data.


    """
    data = {"order_id": "12345", "success": True, "transaction_id": "67890"}
    cancel_reservation = CancelReservation.from_dict(data)
    assert cancel_reservation.order_id == "12345"
    assert cancel_reservation.success is True
    assert cancel_reservation.transaction_id == "67890"


def test_from_dict_with_none():
    """
    Test that the from_dict method returns None when the input dictionary is None.

    This test verifies that the from_dict method returns None when None is provided
    as the input dictionary.

    """
    cancel_reservation = CancelReservation.from_dict(None)
    assert cancel_reservation is None


def test_from_dict_handles_missing_fields():
    """
    Test that the from_dict method handles missing fields by setting them to None.

    This test verifies that the from_dict method correctly creates a CancelReservation
    object from a dictionary with missing fields, resulting in None values for
    all attributes.


    """
    data = {}
    cancel_reservation = CancelReservation.from_dict(data)
    assert cancel_reservation.order_id is None
    assert cancel_reservation.success is None
    assert cancel_reservation.transaction_id is None
