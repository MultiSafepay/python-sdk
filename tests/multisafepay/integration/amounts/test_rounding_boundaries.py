"""
Rounding boundary scenarios (offline).

These scenarios validate that policy knobs (strategy/mode) produce the expected
minor-unit totals around half-cent boundaries.
"""

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


def test_rounding_boundary_truncation_mismatch_expected() -> None:
    """
    Boundary: 0.335 * 3 = 1.005.

    With HALF_UP end-rounding, this becomes 1.01 (101 cents).
    """
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


def test_rounding_boundary_expected_pass_with_truncated_amount() -> None:
    """Same case, but HALF_EVEN rounds 1.005 down to 1.00 (100 cents)."""
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

    with pytest.raises(InvalidTotalAmountException):
        validate_total_amount(
            payload,
            rounding_strategy="end",
            rounding_mode="half_up",
        )
