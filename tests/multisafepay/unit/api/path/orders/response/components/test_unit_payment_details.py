# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.response.components.payment_details import (
    PaymentDetails,
)


def test_initialize_correctly():
    """Test that the PaymentDetails object is initialized correctly with all attributes."""
    payment_details = PaymentDetails(
        account_holder_name="John Doe",
        account_id="acc123",
        collecting_flow="flow1",
        external_transaction_id="ext123",
        recurring_flow="rec_flow1",
        recurring_id="rec123",
        recurring_model="model1",
        type="type1",
        acquirer_reference_number="acq123",
        authorization_code="auth123",
        card_acceptor_id="card_acc_id",
        card_acceptor_location="location1",
        card_acceptor_name="acceptor_name",
        card_entry_mode="entry_mode1",
        card_expiry_date="12/23",
        card_funding="funding1",
        issuer_bin="bin123",
        last4="1234",
        mcc="mcc123",
        response_code="resp123",
        scheme_reference_id="scheme123",
    )

    assert payment_details.account_holder_name == "John Doe"
    assert payment_details.account_id == "acc123"
    assert payment_details.collecting_flow == "flow1"
    assert payment_details.external_transaction_id == "ext123"
    assert payment_details.recurring_flow == "rec_flow1"
    assert payment_details.recurring_id == "rec123"
    assert payment_details.recurring_model == "model1"
    assert payment_details.type == "type1"
    assert payment_details.acquirer_reference_number == "acq123"
    assert payment_details.authorization_code == "auth123"
    assert payment_details.card_acceptor_id == "card_acc_id"
    assert payment_details.card_acceptor_location == "location1"
    assert payment_details.card_acceptor_name == "acceptor_name"
    assert payment_details.card_entry_mode == "entry_mode1"
    assert payment_details.card_expiry_date == "12/23"
    assert payment_details.card_funding == "funding1"
    assert payment_details.issuer_bin == "bin123"
    assert payment_details.last4 == "1234"
    assert payment_details.mcc == "mcc123"
    assert payment_details.response_code == "resp123"
    assert payment_details.scheme_reference_id == "scheme123"


def test_initialize_with_none_values():
    """Test that the PaymentDetails object is initialized correctly with None values for all attributes."""
    payment_details = PaymentDetails()

    assert payment_details.account_holder_name is None
    assert payment_details.account_id is None
    assert payment_details.collecting_flow is None
    assert payment_details.external_transaction_id is None
    assert payment_details.recurring_flow is None
    assert payment_details.recurring_id is None
    assert payment_details.recurring_model is None
    assert payment_details.type is None
    assert payment_details.acquirer_reference_number is None
    assert payment_details.authorization_code is None
    assert payment_details.card_acceptor_id is None
    assert payment_details.card_acceptor_location is None
    assert payment_details.card_acceptor_name is None
    assert payment_details.card_entry_mode is None
    assert payment_details.card_expiry_date is None
    assert payment_details.card_funding is None
    assert payment_details.issuer_bin is None
    assert payment_details.last4 is None
    assert payment_details.mcc is None
    assert payment_details.response_code is None
    assert payment_details.scheme_reference_id is None


def test_from_dict_creates_payment_details_instance_with_correct_values():
    """Test that the PaymentDetails object is created correctly from a dictionary with all attributes."""
    data = {
        "account_holder_name": "John Doe",
        "account_id": "acc123",
        "collecting_flow": "flow1",
        "external_transaction_id": "ext123",
        "recurring_flow": "rec_flow1",
        "recurring_id": "rec123",
        "recurring_model": "model1",
        "type": "type1",
        "acquirer_reference_number": "acq123",
        "authorization_code": "auth123",
        "card_acceptor_id": "card_acc_id",
        "card_acceptor_location": "location1",
        "card_acceptor_name": "acceptor_name",
        "card_entry_mode": "entry_mode1",
        "card_expiry_date": "12/23",
        "card_funding": "funding1",
        "issuer_bin": "bin123",
        "last4": "1234",
        "mcc": "mcc123",
        "response_code": "resp123",
        "scheme_reference_id": "scheme123",
    }
    payment_details = PaymentDetails.from_dict(data)

    assert payment_details.account_holder_name == "John Doe"
    assert payment_details.account_id == "acc123"
    assert payment_details.collecting_flow == "flow1"
    assert payment_details.external_transaction_id == "ext123"
    assert payment_details.recurring_flow == "rec_flow1"
    assert payment_details.recurring_id == "rec123"
    assert payment_details.recurring_model == "model1"
    assert payment_details.type == "type1"
    assert payment_details.acquirer_reference_number == "acq123"
    assert payment_details.authorization_code == "auth123"
    assert payment_details.card_acceptor_id == "card_acc_id"
    assert payment_details.card_acceptor_location == "location1"
    assert payment_details.card_acceptor_name == "acceptor_name"
    assert payment_details.card_entry_mode == "entry_mode1"
    assert payment_details.card_expiry_date == "12/23"
    assert payment_details.card_funding == "funding1"
    assert payment_details.issuer_bin == "bin123"
    assert payment_details.last4 == "1234"
    assert payment_details.mcc == "mcc123"
    assert payment_details.response_code == "resp123"
    assert payment_details.scheme_reference_id == "scheme123"


def test_from_dict_creates_payment_details_instance_with_none_values():
    """Test that the PaymentDetails object is created correctly from an empty dictionary with None values for all attributes."""
    data = {}
    payment_details = PaymentDetails.from_dict(data)

    assert payment_details.account_holder_name is None
    assert payment_details.account_id is None
    assert payment_details.collecting_flow is None
    assert payment_details.external_transaction_id is None
    assert payment_details.recurring_flow is None
    assert payment_details.recurring_id is None
    assert payment_details.recurring_model is None
    assert payment_details.type is None
    assert payment_details.acquirer_reference_number is None
    assert payment_details.authorization_code is None
    assert payment_details.card_acceptor_id is None
    assert payment_details.card_acceptor_location is None
    assert payment_details.card_acceptor_name is None
    assert payment_details.card_entry_mode is None
    assert payment_details.card_expiry_date is None
    assert payment_details.card_funding is None
    assert payment_details.issuer_bin is None
    assert payment_details.last4 is None
    assert payment_details.mcc is None
    assert payment_details.response_code is None
    assert payment_details.scheme_reference_id is None


def from_dict_returns_none_for_none_input():
    """Test that the PaymentDetails.from_dict method returns None when the input is None."""
    payment_details = PaymentDetails.from_dict(None)

    assert payment_details is None
