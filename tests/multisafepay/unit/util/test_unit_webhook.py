# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Utility functions for test unit webhook."""

import pytest
import json

from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.util.webhook import Webhook

API_KEY = "your-MultiSafepay-API-key"
AUTH = "MTYxNjYwMTg1MTo5MTYxYzdmMmUyNWQ5NGQ2NDFiYmMwNmFiNTA0OTg4ZTRmYWI0ZjhhMTc4NTBhM2QyYTI1ODRiMjBkYjVkMTNiNTYzMzI0OGRjZmFjMzkzN2E2YWZkNDE0ZjJjZDYxNDc3MGZlMGQ3MjcyOWUxNmZiZGUzMGU4OTg5OGE0MzNlYw=="
JSON_STRING = json.dumps(
    {
        "amount": 24293,
        "amount_refunded": 0,
        "checkout_options": {
            "alternate": [
                {
                    "name": "0",
                    "rules": [{"country": "", "rate": "0.00"}],
                    "standalone": "",
                },
            ],
            "default": {"rate": 0.21, "shipping_taxed": True},
        },
        "costs": [
            {
                "amount": 7.04,
                "description": "2.9 % For Visa CreditCards Transactions (min 0.6)",
                "transaction_id": "2583849",
                "type": "SYSTEM",
            },
        ],
        "created": "2021-03-24T16:26:31",
        "currency": "GBP",
        "custom_info": {"custom_1": None, "custom_2": None, "custom_3": None},
        "customer": {
            "address1": "Kraanspoor",
            "address2": None,
            "city": "Amsterdam",
            "country": "NL",
            "country_name": None,
            "email": "john.doe@example.com",
            "first_name": "John",
            "house_number": "39C",
            "last_name": "Doe",
            "locale": "nl_NL",
            "phone1": "0612345678",
            "phone2": "",
            "state": None,
            "zip_code": "1033SC",
        },
        "description": "Payment for order: 182",
        "fastcheckout": "NO",
        "financial_status": "completed",
        "items": '<table border="0" cellpadding="5" width="100%">\n<tr>\n<th width="10%"><font size="2" face="Verdana">Quantity </font></th>\n<th align="left"></th>\n<th align="left"><font size="2" face="Verdana">Details </font></th>\n<th width="19%" align="right"><font size="2" face="Verdana">Price </font></th>\n</tr>\n<tr>\n<td align="center"><font size="2" face="Verdana">1</font></td>\n<td width="6%"></td>\n<td width="65%"><font size="2" face="Verdana">Ergonomic Paper Table</font></td>\n<td align="right">&pound;<font size="2" face="Verdana">242.93</font>\n</td>\n</tr>\n</table>',
        "modified": "2021-03-24T16:26:38",
        "order_id": "182",
        "payment_details": {
            "account_holder_name": "MultiSafepay",
            "account_id": None,
            "card_expiry_date": "2404",
            "external_transaction_id": "234453696",
            "last4": "1111",
            "recurring_flow": None,
            "recurring_id": "99814704667013722040",
            "recurring_model": None,
            "type": "VISA",
        },
        "payment_methods": [
            {
                "account_holder_name": "MultiSafepay",
                "amount": 24293,
                "card_expiry_date": 2404,
                "currency": "GBP",
                "description": "Payment for order: 182",
                "external_transaction_id": "234453696",
                "last4": 1111,
                "payment_description": "Visa CreditCards",
                "status": "completed",
                "type": "VISA",
            },
        ],
        "reason": "",
        "reason_code": "",
        "related_transactions": None,
        "shopping_cart": {
            "items": [
                {
                    "cashback": "",
                    "currency": "GBP",
                    "description": "",
                    "image": "",
                    "merchant_item_id": "68",
                    "name": "Ergonomic Paper Table",
                    "options": [],
                    "product_url": "",
                    "quantity": "1",
                    "tax_table_selector": "0",
                    "unit_price": "242.9300000000",
                    "weight": {"unit": None, "value": None},
                },
            ],
        },
        "status": "completed",
        "transaction_id": 4680345,
        "var1": None,
        "var2": "182",
        "var3": None,
    },
)


def test_check_auth_with_no_timestamp_check():
    """Test that the Webhook.validate method returns True when the timestamp check is disabled."""
    assert Webhook.validate(JSON_STRING, AUTH, API_KEY, 0)


def test_check_auth_with_failing_timestamp_check():
    """Test that the Webhook.validate method returns False when the timestamp check fails."""
    assert not Webhook.validate(JSON_STRING, AUTH, API_KEY, 1)


def test_verify_with_invalid_api_key():
    """Test that the Webhook.validate method returns False when an invalid API key is provided."""
    assert not Webhook.validate(JSON_STRING, AUTH, "a-fake-API-key", 0)


def test_verify_with_invalid_json_argument():
    """Test that the Webhook.validate method raises an InvalidArgumentException when an invalid JSON argument is provided."""
    with pytest.raises(
        InvalidArgumentException,
    ):  # changed to TypeError because in python you cant pass int to json.loads
        Webhook.validate(1, AUTH, API_KEY, 0)


def test_verify_with_invalid_validation_time_argument():
    """Test that the Webhook.validate method raises an InvalidArgumentException when an invalid validation time argument is provided."""
    with pytest.raises(
        InvalidArgumentException,
    ):  # changed to ValueError to match python's error handling.
        Webhook.validate(JSON_STRING, AUTH, API_KEY, -1)


def test_verify_with_empty_spaces_in_api_key():
    """Test that the Webhook.validate method returns True when the API key contains leading or trailing spaces."""
    assert Webhook.validate(
        JSON_STRING,
        AUTH,
        " your-MultiSafepay-API-key ",
        0,
    )
