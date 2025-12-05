# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Total amount calculation and validation utilities for order processing."""

import json
from decimal import Decimal
from typing import Union

from multisafepay.exception.invalid_total_amount import (
    InvalidTotalAmountException,
)


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


def validate_total_amount(data: dict) -> bool:
    """
    Validate the total amount in the provided data dictionary.

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
    total_unit_price = __calculate_totals(data)

    # Convert total_unit_price to cents (integer) for comparison
    total_unit_price_cents = int(total_unit_price * 100)

    if total_unit_price_cents != amount:
        msg = f"Total of unit_price ({total_unit_price}) does not match amount ({amount})"
        # Create a JSON-serializable copy of data by converting Decimal to float
        serializable_data = _convert_decimals_to_float(data)
        msg += "\n" + json.dumps(serializable_data, indent=4)
        raise InvalidTotalAmountException(msg)

    return True


def __calculate_totals(data: dict) -> Decimal:
    """
    Calculate the total unit price of items in the shopping cart using precise Decimal arithmetic.

    Parameters
    ----------
    data (dict): The data dictionary containing the shopping cart details.

    Returns
    -------
    Decimal: The total unit price of all items in the shopping cart with precise decimal calculation.

    """
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
        total_unit_price += item_price

    # Round to 2 decimal places for currency
    return total_unit_price.quantize(Decimal("0.01"))


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
