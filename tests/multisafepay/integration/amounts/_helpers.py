"""Shared helpers for offline amount/total validation scenario tests."""

from __future__ import annotations

from decimal import Decimal


def data(
    *,
    amount: int,
    items: list[dict],
    tax_tables: dict | None = None,
) -> dict:
    """Build a minimal `validate_total_amount` input dict."""
    result: dict = {
        "amount": amount,
        "shopping_cart": {"items": items},
    }
    if tax_tables is not None:
        result["checkout_options"] = {"tax_tables": tax_tables}
    return result


def no_tax_tables() -> dict:
    """Tax tables configuration that yields 0% tax under selector 'none'."""
    return {
        "default": {"shipping_taxed": True, "rate": 0.0},
        "alternate": [
            {"name": "none", "standalone": False, "rules": [{"rate": 0.0}]},
        ],
    }


def vat_tables() -> dict:
    """Common VAT tables used for scenarios (21% and 9%)."""
    return {
        "default": {"shipping_taxed": True, "rate": 0.21},
        "alternate": [
            {"name": "BTW21", "standalone": True, "rules": [{"rate": 0.21}]},
            {"name": "BTW9", "standalone": True, "rules": [{"rate": 0.09}]},
        ],
    }


def d(value: str) -> Decimal:
    """Convenience Decimal constructor for test readability."""
    return Decimal(value)
