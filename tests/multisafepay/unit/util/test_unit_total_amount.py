# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Utility functions for test unit total amount."""

from multisafepay.util.total_amount import (
    validate_total_amount,
    __get_tax_rate_by_item,
    __calculate_totals,
)


def test_get_tax_rate_by_item():
    """Test the get_tax_rate_by_item method."""
    item = {"unit_price": 1000, "quantity": 1, "tax_table_selector": "BTW10"}

    data = {
        "checkout_options": {
            "tax_tables": {
                "default": {"shipping_taxed": True, "rate": 0.21},
                "alternate": [
                    {
                        "name": "BTW10",
                        "standalone": True,
                        "rules": [{"rate": 0.10}],
                    },
                ],
            },
        },
    }

    assert __get_tax_rate_by_item(item, data) == 0.1


def test_get_tax_rate_by_item_btw21():
    """Test the get_tax_rate_by_item method."""
    item = {"unit_price": 1000, "quantity": 1, "tax_table_selector": "BTW22"}

    data = {
        "checkout_options": {
            "tax_tables": {
                "default": {"shipping_taxed": True, "rate": 0.21},
                "alternate": [
                    {
                        "name": "BTW10",
                        "standalone": True,
                        "rules": [{"rate": 0.10}],
                    },
                ],
            },
        },
    }

    assert __get_tax_rate_by_item(item, data) == 0.21


def test_calculate_totals():
    """Test the calculate_totals method."""
    data = {
        "shopping_cart": {
            "items": [
                {
                    "unit_price": 1.21,
                    "quantity": 2,
                    "tax_table_selector": "default",
                },
            ],
        },
    }

    assert __calculate_totals(data) == 2.42


def test_validate_total_amount():
    """Test the validate_total_amount method."""
    data = {
        "amount": 1000,
        "shopping_cart": {
            "items": [
                {
                    "unit_price": 10.00,
                    "quantity": 1,
                    "tax_table_selector": "default",
                },
            ],
        },
    }

    assert validate_total_amount(data) is True
