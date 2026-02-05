"""Multi-line rounding policy mismatches (offline)."""

from __future__ import annotations

import pytest

from multisafepay.exception.invalid_total_amount import (
    InvalidTotalAmountException,
)
from multisafepay.util.total_amount import (
    calculate_total_amount_cents,
    validate_total_amount,
)

from ._helpers import data, no_tax_tables


def test_round_per_line_vs_round_at_end_can_disagree() -> None:
    """Verify that per-line rounding can produce different totals than end rounding."""
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
        calculate_total_amount_cents(payload, rounding_strategy="line") == 102
    )
    assert validate_total_amount(payload, rounding_strategy="line") is True

    with pytest.raises(InvalidTotalAmountException):
        validate_total_amount(payload, rounding_strategy="end")


def test_many_small_lines_rounding_noise() -> None:
    """Verify that many small lines can accumulate rounding noise."""
    payload = data(
        amount=20,
        items=[
            {
                "unit_price": "0.015",
                "quantity": 1,
                "tax_table_selector": "none",
            }
            for _ in range(10)
        ],
        tax_tables=no_tax_tables(),
    )
    assert (
        calculate_total_amount_cents(payload, rounding_strategy="line") == 20
    )
    assert validate_total_amount(payload, rounding_strategy="line") is True

    with pytest.raises(InvalidTotalAmountException):
        validate_total_amount(payload, rounding_strategy="end")
