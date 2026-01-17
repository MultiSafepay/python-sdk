"""Tax-related scenarios that can drift due to rounding policy (offline)."""

from __future__ import annotations

from decimal import Decimal

from multisafepay.util.total_amount import (
    calculate_total_amount_cents,
    validate_total_amount,
)

from ._helpers import data, vat_tables


def test_tax_rate_applied_simple_21_percent() -> None:
    """Basic tax application: unit_price*qty*(1+rate) should match."""
    payload = data(
        amount=121,
        items=[
            {
                "unit_price": "1.00",
                "quantity": 1,
                "tax_table_selector": "BTW21",
            },
        ],
        tax_tables=vat_tables(),
    )
    assert validate_total_amount(payload) is True


def test_tax_rate_string_decimal_rate() -> None:
    """Tax rate as strings should behave the same in calculations."""
    tax_tables = {
        "default": {"shipping_taxed": True, "rate": "0.21"},
        "alternate": [
            {"name": "BTW21", "standalone": True, "rules": [{"rate": "0.21"}]},
        ],
    }
    payload = data(
        amount=121,
        items=[
            {
                "unit_price": Decimal("1.00"),
                "quantity": 1,
                "tax_table_selector": "BTW21",
            },
        ],
        tax_tables=tax_tables,
    )
    assert validate_total_amount(payload) is True


def test_multiple_items_mixed_taxes_total_can_differ_by_rounding() -> None:
    """
    Mixed tax selectors across items should be internally consistent.

    We compute `amount` using the SDK helper so the validator matches.
    """
    # Este test construye un payload “tipo order” (pero offline) para validar que
    # `validate_total_amount()` considera coherentes:
    # - `amount`: total declarado en **minor units** (céntimos).
    # - `items[*].unit_price`: precio unitario en **major units** (p.ej. EUR).
    # - `items[*].quantity`: cantidad.
    # - `tax_table_selector`: qué regla/tabla de IVA aplicar por línea.
    # - `tax_tables`: tablas de IVA disponibles.
    #
    # La idea del caso: mezclar diferentes tipos de IVA (21% y 9%) en distintas
    # líneas puede destapar diferencias de política de redondeo (por línea vs al
    # final) y de cómo se aplican los impuestos (y cuándo se cuantiza a 2 decimales).
    payload = data(
        amount=0,
        items=[
            # Línea 1: 0.10 EUR * 3 unidades, con IVA 21% (BTW21).
            {
                "unit_price": "0.10",
                "quantity": 3,
                "tax_table_selector": "BTW21",
            },
            # Línea 2: 0.20 EUR * 3 unidades, con IVA 9% (BTW9).
            {
                "unit_price": "0.20",
                "quantity": 3,
                "tax_table_selector": "BTW9",
            },
        ],
        # Tablas de IVA usadas por el selector: normalmente incluyen una “default”
        # y reglas “standalone” por nombre (p.ej. BTW21 / BTW9).
        tax_tables=vat_tables(),
    )

    # `validate_total_amount()` calcula el total localmente (con Decimal y reglas
    # de IVA) y lo compara contra `amount`.
    #
    # Ojo: si tu cálculo “externo” (o el backend) redondea distinto (p.ej. redondeo
    # por línea vs redondeo al final, o diferente handling de impuestos), este tipo
    # de caso puede producir discrepancias de 1-2 céntimos.
    payload["amount"] = calculate_total_amount_cents(payload)
    assert validate_total_amount(payload) is True
