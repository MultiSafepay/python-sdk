# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""
Total amount calculation and validation utilities for order processing.

Important:
---------
Different integrators (ERP/POS/e-commerce) can legitimately compute `amount`
under different rounding policies (per-line vs end rounding, half-up vs
bankers rounding, etc.).

This module supports a **best-effort** local validator that can be configured
to match a known policy, but the API remains the source of truth.

"""

import json
from decimal import ROUND_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from typing import Literal, Union

from multisafepay.exception.invalid_total_amount import (
    InvalidTotalAmountException,
)

RoundingStrategy = Literal["end", "line"]
RoundingMode = Literal["half_up", "half_even", "down"]


def _decimal_rounding(mode: RoundingMode) -> str:
    if mode == "half_even":
        return ROUND_HALF_EVEN
    if mode == "down":
        return ROUND_DOWN
    return ROUND_HALF_UP


def _convert_decimals_to_float(
    obj: Union[Decimal, dict, list, object],
) -> Union[float, dict, list, object]:
    """
    Recursively convert Decimal objects to float for JSON serialization.

    Parameters
    ----------
    obj : Union[Decimal, dict, list, object]
        The object to convert (can be dict, list, Decimal, or any other type)

    Returns
    -------
    Union[float, dict, list, object]
        The converted object with all Decimals replaced by floats

    """
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, dict):
        return {
            key: _convert_decimals_to_float(value)
            for key, value in obj.items()
        }
    if isinstance(obj, list):
        return [_convert_decimals_to_float(item) for item in obj]
    return obj


def validate_total_amount(
    data: dict,
    *,
    rounding_strategy: RoundingStrategy = "end",
    rounding_mode: RoundingMode = "half_up",
) -> bool:
    """
    Validate the total amount in the provided data dictionary.

    Important
    ---------
    This validator uses a specific calculation/rounding model:
    - Applies tax per item (if any) and sums the precise Decimal totals.
    - Quantizes the final total to 2 decimals.
    - Converts to cents using HALF_UP.

    If the input `amount` was produced under a different policy (per-line rounding,
    different tax rounding, unit prices with more than 2 decimals, etc.), the SDK
    may disagree with external systems. In those cases, prefer letting the API
    validate and/or use `calculate_total_amount_cents()` to compute a consistent
    amount under this validator's rules.

    Parameters
    ----------
    data (dict): The data dictionary containing the amount and shopping cart details.

    Returns
    -------
    bool: True if the total amount is valid, False otherwise.

    Raises
    ------
    InvalidTotalAmountException: If the total unit price does not match the amount in the data.

    """
    if "amount" not in data:
        raise InvalidTotalAmountException("Amount is required")

    if not data.get("shopping_cart") or not data["shopping_cart"].get("items"):
        return False

    amount = data["amount"]
    total_unit_price = calculate_total_amount(
        data,
        rounding_strategy=rounding_strategy,
        rounding_mode=rounding_mode,
    )

    # Convert to cents (integer) for comparison.
    # Note: total_unit_price is already quantized to 2 decimals in calculate_total_amount().
    total_unit_price_cents = calculate_total_amount_cents(
        data,
        rounding_strategy=rounding_strategy,
        rounding_mode=rounding_mode,
    )

    if total_unit_price_cents != amount:
        delta = amount - total_unit_price_cents
        msg = (
            f"Total of unit_price ({total_unit_price}) does not match amount ({amount}). "
            f"Expected amount: {total_unit_price_cents} (delta: {delta})."
        )
        # Create a JSON-serializable copy of data by converting Decimal to float
        serializable_data = _convert_decimals_to_float(data)
        msg += "\n" + json.dumps(serializable_data, indent=4)
        raise InvalidTotalAmountException(msg)

    return True


def calculate_total_amount(
    data: dict,
    *,
    rounding_strategy: RoundingStrategy = "end",
    rounding_mode: RoundingMode = "half_up",
) -> Decimal:
    """
    Calculate the order total (major units) using the same logic as the validator.

    This is useful to generate a consistent `amount` before submitting an Order.
    """
    return __calculate_totals(
        data,
        rounding_strategy=rounding_strategy,
        rounding_mode=rounding_mode,
    )


def calculate_total_amount_cents(
    data: dict,
    *,
    rounding_strategy: RoundingStrategy = "end",
    rounding_mode: RoundingMode = "half_up",
) -> int:
    """Calculate the expected `amount` (minor units) using the validator's logic."""
    total = calculate_total_amount(
        data,
        rounding_strategy=rounding_strategy,
        rounding_mode=rounding_mode,
    )
    cents = (total * 100).to_integral_value(
        rounding=_decimal_rounding(rounding_mode),
    )
    return int(cents)


def __calculate_totals(
    data: dict,
    *,
    rounding_strategy: RoundingStrategy = "end",
    rounding_mode: RoundingMode = "half_up",
) -> Decimal:
    """
    Calculate the total unit price of items in the shopping cart using precise Decimal arithmetic.

    Parameters
    ----------
    data (dict): The data dictionary containing the shopping cart details.

    Returns
    -------
    Decimal: The total unit price of all items in the shopping cart with precise decimal calculation.

    """
    rounding = _decimal_rounding(rounding_mode)
    total_unit_price = Decimal("0")
    for item in data["shopping_cart"]["items"]:
        tax_rate = __get_tax_rate_by_item(item, data)

        # Convert to Decimal for precise calculations
        unit_price = Decimal(str(item["unit_price"]))
        quantity = Decimal(str(item["quantity"]))
        tax_rate_decimal = Decimal(str(tax_rate))

        # Calculate item price with tax
        item_price = unit_price * quantity
        item_price += tax_rate_decimal * item_price

        # Some systems (e.g., ERPs/POS) round per line item; others round at the end.
        if rounding_strategy == "line":
            item_price = item_price.quantize(
                Decimal("0.01"),
                rounding=rounding,
            )

        total_unit_price += item_price

    # Round to 2 decimal places for currency
    return total_unit_price.quantize(Decimal("0.01"), rounding=rounding)


def __get_tax_rate_by_item(
    item: dict,
    data: dict,
) -> Union[Decimal, int]:
    """
    Get the tax rate for a specific item in the shopping cart.

    Parameters
    ----------
    item (dict): The item dictionary containing the tax table selector.
    data (dict): The data dictionary containing the checkout options and tax tables.

    Returns
    -------
    Union[Decimal, int]: The tax rate for the item as Decimal, or 0 if no tax rate is found.

    """
    if "tax_table_selector" not in item or not item["tax_table_selector"]:
        return 0

    if (
        "checkout_options" not in data
        or "tax_tables" not in data["checkout_options"]
        or "default" not in data["checkout_options"]["tax_tables"]
    ):
        return 0

    for tax_table in data["checkout_options"]["tax_tables"]["alternate"]:
        if tax_table["name"] != item["tax_table_selector"]:
            continue

        tax_rule = tax_table["rules"][0]
        return Decimal(str(tax_rule["rate"]))

    default_rate = (
        data["checkout_options"]["tax_tables"]["default"]["rate"]
        if "default" in data["checkout_options"]["tax_tables"]
        and "rate" in data["checkout_options"]["tax_tables"]["default"]
        else 0
    )
    return Decimal(str(default_rate)) if default_rate != 0 else 0
