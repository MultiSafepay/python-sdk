# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.transactions.response.transaction import (
    Transaction,
)


def test_initializes_transaction_correctly():
    """
    Test that a Transaction object is correctly initialized with given data.
    """
    transaction = Transaction(
        amount=1000,
        completed="2023-10-01",
        costs=None,
        created="2023-09-01",
        modified="2023-09-15",
        currency="USD",
        customer=None,
        custom_info=None,
        debit_credit="debit",
        description="Test Transaction",
        financial_status="completed",
        invoice_id="INV123",
        net=900,
        order_id="ORD123",
        payment_method="credit_card",
        payment_methods=None,
        reason="Purchase",
        reason_code="00",
        site_id="SITE123",
        status="completed",
        transaction_id="TX123",
        type="sale",
        var1="var1",
        var2="var2",
        var3="var3",
        fastcheckout="yes",
        items="item1, item2",
    )
    assert transaction.amount == 1000
    assert transaction.completed == "2023-10-01"
    assert transaction.costs is None
    assert transaction.created == "2023-09-01"
    assert transaction.modified == "2023-09-15"
    assert transaction.currency == "USD"
    assert transaction.customer is None
    assert transaction.custom_info is None
    assert transaction.debit_credit == "debit"
    assert transaction.description == "Test Transaction"
    assert transaction.financial_status == "completed"
    assert transaction.invoice_id == "INV123"
    assert transaction.net == 900
    assert transaction.order_id == "ORD123"
    assert transaction.payment_method == "credit_card"
    assert transaction.payment_methods is None
    assert transaction.reason == "Purchase"
    assert transaction.reason_code == "00"
    assert transaction.site_id == "SITE123"
    assert transaction.status == "completed"
    assert transaction.transaction_id == "TX123"
    assert transaction.type == "sale"
    assert transaction.var1 == "var1"
    assert transaction.var2 == "var2"
    assert transaction.var3 == "var3"
    assert transaction.fastcheckout == "yes"
    assert transaction.items == "item1, item2"


def test_initializes_transaction_empty():
    """
    Test that a Transaction object is correctly initialized with default values.
    """
    transaction = Transaction()
    assert transaction.amount is None
    assert transaction.completed is None
    assert transaction.costs is None
    assert transaction.created is None
    assert transaction.modified is None
    assert transaction.currency is None
    assert transaction.customer is None
    assert transaction.custom_info is None
    assert transaction.debit_credit is None
    assert transaction.description is None
    assert transaction.financial_status is None
    assert transaction.invoice_id is None
    assert transaction.net is None
    assert transaction.order_id is None
    assert transaction.payment_method is None
    assert transaction.payment_methods is None
    assert transaction.reason is None
    assert transaction.reason_code is None
    assert transaction.site_id is None
    assert transaction.status is None
    assert transaction.transaction_id is None
    assert transaction.type is None
    assert transaction.var1 is None
    assert transaction.var2 is None
    assert transaction.var3 is None
    assert transaction.fastcheckout is None
    assert transaction.items is None


def test_initializes_transaction_from_dict():
    """
    Test that a Transaction object is correctly initialized from a dictionary.
    """
    data = {
        "amount": 1000,
        "completed": "2023-10-01",
        "costs": None,
        "created": "2023-09-01",
        "modified": "2023-09-15",
        "currency": "USD",
        "customer": None,
        "custom_info": None,
        "debit_credit": "debit",
        "description": "Test Transaction",
        "financial_status": "completed",
        "invoice_id": "INV123",
        "net": 900,
        "order_id": "ORD123",
        "payment_method": "credit_card",
        "payment_methods": None,
        "reason": "Purchase",
        "reason_code": "00",
        "site_id": "SITE123",
        "status": "completed",
        "transaction_id": "TX123",
        "type": "sale",
        "var1": "var1",
        "var2": "var2",
        "var3": "var3",
        "fastcheckout": "yes",
        "items": "item1, item2",
    }
    transaction = Transaction.from_dict(data)
    assert transaction.amount == 1000
    assert transaction.completed == "2023-10-01"
    assert transaction.costs is None
    assert transaction.created == "2023-09-01"
    assert transaction.modified == "2023-09-15"
    assert transaction.currency == "USD"
    assert transaction.customer is None
    assert transaction.custom_info is None
    assert transaction.debit_credit == "debit"
    assert transaction.description == "Test Transaction"
    assert transaction.financial_status == "completed"
    assert transaction.invoice_id == "INV123"
    assert transaction.net == 900
    assert transaction.order_id == "ORD123"
    assert transaction.payment_method == "credit_card"
    assert transaction.payment_methods is None
    assert transaction.reason == "Purchase"
    assert transaction.reason_code == "00"
    assert transaction.site_id == "SITE123"
    assert transaction.status == "completed"
    assert transaction.transaction_id == "TX123"
    assert transaction.type == "sale"
    assert transaction.var1 == "var1"
    assert transaction.var2 == "var2"
    assert transaction.var3 == "var3"
    assert transaction.fastcheckout == "yes"
    assert transaction.items == "item1, item2"


def test_initializes_transaction_with_none_values_from_dict():
    """
    Test that a Transaction object is correctly initialized from an empty dictionary.
    """
    data = {}
    transaction = Transaction.from_dict(data)
    assert transaction.amount is None
    assert transaction.completed is None
    assert transaction.costs is None
    assert transaction.created is None
    assert transaction.modified is None
    assert transaction.currency is None
    assert transaction.customer is None
    assert transaction.custom_info is None
    assert transaction.debit_credit is None
    assert transaction.description is None
    assert transaction.financial_status is None
    assert transaction.invoice_id is None
    assert transaction.net is None
    assert transaction.order_id is None
    assert transaction.payment_method is None
    assert transaction.payment_methods is None
    assert transaction.reason is None
    assert transaction.reason_code is None
    assert transaction.site_id is None
    assert transaction.status is None
    assert transaction.transaction_id is None
    assert transaction.type is None
    assert transaction.var1 is None
    assert transaction.var2 is None
    assert transaction.var3 is None
    assert transaction.fastcheckout is None
    assert transaction.items is None


def test_from_dict_returns_none_for_none_input_from_dict():
    """
    Test that the from_dict method returns None when given None as input.
    """
    transaction = Transaction.from_dict(None)
    assert transaction is None
