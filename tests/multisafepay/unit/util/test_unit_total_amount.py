# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Utility functions for test unit total amount."""

from decimal import Decimal

from multisafepay.util.total_amount import (
    validate_total_amount,
    calculate_total_amount,
    calculate_total_amount_cents,
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

    assert __get_tax_rate_by_item(item, data) == Decimal("0.1")


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

    assert __get_tax_rate_by_item(item, data) == Decimal("0.21")


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

    assert __calculate_totals(data) == Decimal("2.42")


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


def test_calculate_total_amount_helpers_match_validator_math() -> None:
    """Ensure calculate_total_amount and calculate_total_amount_cents produce consistent results."""
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

    assert calculate_total_amount(data) == Decimal("10.00")
    assert calculate_total_amount_cents(data) == 1000


def test_rounding_strategy_end_vs_line_can_differ() -> None:
    """Per-line rounding can diverge from end rounding on micro-priced lines."""
    data = {
        "shopping_cart": {
            "items": [
                {
                    "unit_price": "0.335",
                    "quantity": 1,
                    "tax_table_selector": None,
                },
                {
                    "unit_price": "0.335",
                    "quantity": 1,
                    "tax_table_selector": None,
                },
                {
                    "unit_price": "0.335",
                    "quantity": 1,
                    "tax_table_selector": None,
                },
            ],
        },
        "amount": 0,
    }

    # 0.335 * 3 = 1.005 -> 1.01 (101 cents) if rounding at end.
    assert calculate_total_amount_cents(data, rounding_strategy="end") == 101

    # 0.335 -> 0.34 per line, 0.34 * 3 = 1.02 (102 cents).
    assert calculate_total_amount_cents(data, rounding_strategy="line") == 102


def test_rounding_mode_half_even_vs_half_up_boundary() -> None:
    """HALF_EVEN and HALF_UP can differ on x.xx5 boundaries."""
    data = {
        "shopping_cart": {
            "items": [
                {
                    "unit_price": "0.335",
                    "quantity": 3,
                    "tax_table_selector": None,
                },
            ],
        },
        "amount": 0,
    }

    # 0.335 * 3 = 1.005
    assert calculate_total_amount_cents(data, rounding_mode="half_up") == 101
    assert calculate_total_amount_cents(data, rounding_mode="half_even") == 100


def test_validate_total_amount_honors_rounding_mode() -> None:
    """Ensure validate_total_amount respects the rounding_mode parameter."""
    data = {
        "shopping_cart": {
            "items": [
                {
                    "unit_price": "0.335",
                    "quantity": 3,
                    "tax_table_selector": None,
                },
            ],
        },
        "amount": 100,
    }

    assert validate_total_amount(data, rounding_mode="half_even") is True


def test_tax_rounding_can_differ_between_line_and_end() -> None:
    """After-tax values can diverge when rounded per line vs at end."""
    tax_tables = {
        "default": {"shipping_taxed": True, "rate": 0.21},
        "alternate": [
            {"name": "BTW21", "standalone": True, "rules": [{"rate": 0.21}]},
        ],
    }
    data = {
        "shopping_cart": {
            "items": [
                {
                    "unit_price": "0.03",
                    "quantity": 1,
                    "tax_table_selector": "BTW21",
                },
                {
                    "unit_price": "0.03",
                    "quantity": 1,
                    "tax_table_selector": "BTW21",
                },
            ],
        },
        "checkout_options": {"tax_tables": tax_tables},
        "amount": 0,
    }

    # Each line: 0.03 * 1.21 = 0.0363 -> 0.04 (line), so total 0.08.
    assert calculate_total_amount_cents(data, rounding_strategy="line") == 8

    # End rounding: 0.0363 + 0.0363 = 0.0726 -> 0.07.
    assert calculate_total_amount_cents(data, rounding_strategy="end") == 7


def test_float_unit_price_binary_representation_does_not_break_simple_totals() -> (
    None
):
    """Float inputs are risky, but the validator should still handle simple cases."""
    data = {
        "shopping_cart": {
            "items": [
                {"unit_price": 0.1, "quantity": 3, "tax_table_selector": None},
            ],
        },
        "amount": 30,
    }

    assert calculate_total_amount_cents(data) == 30
    assert validate_total_amount(data) is True


def test_quantity_as_string_and_fractional_quantity_are_supported() -> None:
    """Ensure string and fractional quantities are handled correctly."""
    data_int_string = {
        "shopping_cart": {
            "items": [
                {
                    "unit_price": "1.00",
                    "quantity": "3",
                    "tax_table_selector": None,
                },
            ],
        },
        "amount": 300,
    }
    assert validate_total_amount(data_int_string) is True

    data_fractional = {
        "shopping_cart": {
            "items": [
                {
                    "unit_price": "1.00",
                    "quantity": "0.5",
                    "tax_table_selector": None,
                },
            ],
        },
        "amount": 50,
    }
    assert validate_total_amount(data_fractional) is True
