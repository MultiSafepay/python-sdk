# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the base API decorator utilities."""

from multisafepay.api.base.decorator import Decorator


def test_initialization_with_empty_dependencies():
    """Test the initialization of a Decorator object with empty dependencies."""
    decorator = Decorator()
    assert decorator.get_dependencies() == {}


def test_adapt_costs_with_valid_data() -> None:
    """Adapt costs from a list of cost dictionaries."""
    decorator = Decorator(dependencies={"key": "value"})
    costs = [{"amount": 100, "description": "Shipping"}]
    result = decorator.adapt_costs(costs)
    assert result is decorator
    assert "costs" in decorator.get_dependencies()


def test_adapt_costs_with_none() -> None:
    """Skip costs adaptation when input is None."""
    decorator = Decorator(dependencies={})
    decorator.adapt_costs(None)
    assert "costs" not in decorator.get_dependencies()


def test_adapt_custom_info_with_valid_data() -> None:
    """Adapt custom info from dictionary."""
    decorator = Decorator(dependencies={})
    decorator.adapt_custom_info({"custom_1": "val1"})
    assert "custom_info" in decorator.get_dependencies()


def test_adapt_customer_with_valid_data() -> None:
    """Adapt customer from dictionary."""
    decorator = Decorator(dependencies={})
    decorator.adapt_customer({"first_name": "John", "last_name": "Doe"})
    assert "customer" in decorator.get_dependencies()


def test_adapt_payment_details_with_valid_data() -> None:
    """Adapt payment details from dictionary."""
    decorator = Decorator(dependencies={})
    decorator.adapt_payment_details({"type": "VISA"})
    assert "payment_details" in decorator.get_dependencies()


def test_adapt_payment_methods_with_valid_data() -> None:
    """Adapt payment methods from list of dictionaries."""
    decorator = Decorator(dependencies={})
    decorator.adapt_payment_methods([{"type": "VISA"}])
    assert "payment_methods" in decorator.get_dependencies()


def test_adapt_shopping_cart_with_valid_data() -> None:
    """Adapt shopping cart from dictionary."""
    decorator = Decorator(dependencies={})
    decorator.adapt_shopping_cart({"items": []})
    assert "shopping_cart" in decorator.get_dependencies()


def test_adapt_related_transactions_with_valid_data() -> None:
    """Adapt related transactions from list of dictionaries."""
    decorator = Decorator(dependencies={})
    decorator.adapt_related_transactions(
        [{"transaction_id": 123, "order_id": "order-1"}],
    )
    assert "related_transactions" in decorator.get_dependencies()


def test_adapt_checkout_options_with_valid_data() -> None:
    """Adapt checkout options from dictionary."""
    decorator = Decorator(dependencies={})
    decorator.adapt_checkout_options({})
    assert "checkout_options" in decorator.get_dependencies()


def test_adapt_order_adjustment_with_valid_data() -> None:
    """Adapt order adjustment from dictionary."""
    decorator = Decorator(dependencies={})
    decorator.adapt_order_adjustment({"total_adjustment": 0})
    assert "order_adjustment" in decorator.get_dependencies()


def test_chaining_multiple_adapters() -> None:
    """Chain multiple adapt calls and get all dependencies."""
    deps = (
        Decorator(dependencies={"status": "completed"})
        .adapt_costs([{"amount": 10}])
        .adapt_custom_info({"custom_1": "a"})
        .adapt_payment_details({"type": "VISA"})
        .adapt_payment_methods([{"type": "VISA"}])
        .get_dependencies()
    )
    assert "costs" in deps
    assert "custom_info" in deps
    assert "payment_details" in deps
    assert "payment_methods" in deps
    assert deps["status"] == "completed"
