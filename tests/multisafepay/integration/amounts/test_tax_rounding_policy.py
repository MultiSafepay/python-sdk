"""Tax rounding mismatches (offline)."""

from __future__ import annotations

import pytest

from multisafepay.exception.invalid_total_amount import (
    InvalidTotalAmountException,
)
from multisafepay.util.total_amount import calculate_total_amount_cents
from multisafepay.util.total_amount import validate_total_amount

from ._helpers import data, vat_tables


def test_tax_round_per_line_vs_total_can_disagree() -> None:
    """Verify that tax rounding per line can differ from total tax rounding."""
    payload = data(
        # Crafted to show a per-line rounding difference vs end rounding.
        amount=8,
        items=[
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
        tax_tables=vat_tables(),
    )

    assert calculate_total_amount_cents(payload, rounding_strategy="line") == 8
    assert validate_total_amount(payload, rounding_strategy="line") is True

    with pytest.raises(InvalidTotalAmountException):
        validate_total_amount(payload, rounding_strategy="end")


def test_tax_mixed_rates_with_boundary_prices() -> None:
    """Verify tax calculations with mixed rates and boundary prices."""
    payload = data(
        amount=0,
        items=[
            {
                "unit_price": "0.105",
                "quantity": 1,
                "tax_table_selector": "BTW21",
            },
            {
                "unit_price": "0.105",
                "quantity": 1,
                "tax_table_selector": "BTW9",
            },
        ],
        tax_tables=vat_tables(),
    )

    payload["amount"] = calculate_total_amount_cents(
        payload,
        rounding_strategy="end",
    )
    assert validate_total_amount(payload, rounding_strategy="end") is True
