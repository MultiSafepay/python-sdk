"""Integration tests for amount policy validation."""

from __future__ import annotations

import pytest

from multisafepay.exception.invalid_total_amount import (
    InvalidTotalAmountException,
)
from multisafepay.util.total_amount import (
    calculate_total_amount_cents,
    validate_total_amount,
)

from ._helpers import data, no_tax_tables, vat_tables


def test_end_rounding_half_up_matches_expected_cents() -> None:
    """Verify that end rounding with HALF_UP strategy produces expected results."""
    payload = data(
        amount=101,
        items=[
            {
                "unit_price": "0.335",
                "quantity": 3,
                "tax_table_selector": "none",
            },
        ],
        tax_tables=no_tax_tables(),
    )

    assert (
        calculate_total_amount_cents(
            payload,
            rounding_strategy="end",
            rounding_mode="half_up",
        )
        == 101
    )
    assert (
        validate_total_amount(
            payload,
            rounding_strategy="end",
            rounding_mode="half_up",
        )
        is True
    )


def test_end_rounding_half_even_can_disagree_on_half_cent_boundary() -> None:
    """Verify that HALF_EVEN rounding can differ from HALF_UP on boundaries."""
    payload = data(
        amount=100,
        items=[
            {
                "unit_price": "0.335",
                "quantity": 3,
                "tax_table_selector": "none",
            },
        ],
        tax_tables=no_tax_tables(),
    )

    # 0.335 * 3 = 1.005 -> half-even rounds to 1.00 (100 cents)
    assert (
        calculate_total_amount_cents(
            payload,
            rounding_strategy="end",
            rounding_mode="half_even",
        )
        == 100
    )
    assert (
        validate_total_amount(
            payload,
            rounding_strategy="end",
            rounding_mode="half_even",
        )
        is True
    )

    # Same payload fails under HALF_UP.
    with pytest.raises(InvalidTotalAmountException):
        validate_total_amount(
            payload,
            rounding_strategy="end",
            rounding_mode="half_up",
        )


def test_line_rounding_changes_expected_amount() -> None:
    """Verify that per-line rounding produces different totals than end rounding."""
    payload = data(
        amount=102,
        items=[
            {
                "unit_price": "0.335",
                "quantity": 1,
                "tax_table_selector": "none",
            },
            {
                "unit_price": "0.335",
                "quantity": 1,
                "tax_table_selector": "none",
            },
            {
                "unit_price": "0.335",
                "quantity": 1,
                "tax_table_selector": "none",
            },
        ],
        tax_tables=no_tax_tables(),
    )

    assert (
        calculate_total_amount_cents(
            payload,
            rounding_strategy="line",
            rounding_mode="half_up",
        )
        == 102
    )
    assert (
        validate_total_amount(
            payload,
            rounding_strategy="line",
            rounding_mode="half_up",
        )
        is True
    )

    with pytest.raises(InvalidTotalAmountException):
        validate_total_amount(
            payload,
            rounding_strategy="end",
            rounding_mode="half_up",
        )


def test_tax_tables_respected_and_helper_matches_validator() -> None:
    """Verify that tax tables are applied correctly and helper matches validator."""
    payload = data(
        amount=0,
        items=[
            {
                "unit_price": "0.10",
                "quantity": 3,
                "tax_table_selector": "BTW21",
            },
            {
                "unit_price": "0.20",
                "quantity": 3,
                "tax_table_selector": "BTW9",
            },
        ],
        tax_tables=vat_tables(),
    )

    expected = calculate_total_amount_cents(
        payload,
        rounding_strategy="end",
        rounding_mode="half_up",
    )
    payload["amount"] = expected
    assert (
        validate_total_amount(
            payload,
            rounding_strategy="end",
            rounding_mode="half_up",
        )
        is True
    )
