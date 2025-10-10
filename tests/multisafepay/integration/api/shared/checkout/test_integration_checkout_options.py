# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Shared API models and utilities."""

from multisafepay.api.shared.checkout.default_tax_rate import DefaultTaxRate
from multisafepay.api.shared.checkout.tax_rate import TaxRate
from multisafepay.api.shared.checkout.tax_rule import TaxRule
from multisafepay.api.shared.checkout.checkout_options import CheckoutOptions


def test_initializes_with_valid_values():
    """
    Test that a CheckoutOptions instance initializes with valid values.

    This test verifies that the default tax rate and alternate tax rates are correctly set.

    """
    tax_rule = TaxRule(
        name="Standard Tax",
        rules=[TaxRate(rate=21, country="NL")],
    )
    default_tax_rate = DefaultTaxRate(rate=21, shipping_taxed=True)

    checkout_options = CheckoutOptions(
        default=default_tax_rate,
        alternate=[tax_rule],
    )
    assert checkout_options.default == default_tax_rate
    assert checkout_options.alternate == [tax_rule]


def test_adds_default_tax_rate():
    """
    Test that a default tax rate is added to a CheckoutOptions instance.

    This test verifies that the default tax rate is correctly set.

    """
    default_tax_rate = DefaultTaxRate(rate=21, shipping_taxed=True)
    checkout_options = CheckoutOptions().add_default(default_tax_rate)
    assert checkout_options.default == default_tax_rate


def test_adds_alternate_tax_rates():
    """
    Test that alternate tax rates are added to a CheckoutOptions instance.

    This test verifies that the alternate tax rates are correctly set.

    """
    tax_rates = [
        TaxRate(rate=21, country="NL"),
        TaxRate(rate=19, country="DE"),
    ]
    checkout_options = CheckoutOptions().add_alternate(tax_rates)
    assert checkout_options.alternate == tax_rates


def test_adds_tax_rule():
    """
    Test that a tax rule is added to a CheckoutOptions instance.

    This test verifies that the tax rule is correctly set.

    """
    tax_rule = TaxRule(
        name="Standard Tax",
        rules=[TaxRate(rate=21, country="NL")],
    )
    checkout_options = CheckoutOptions().add_tax_rule(tax_rule)
    assert len(checkout_options.alternate) == 1
    assert checkout_options.alternate[0] == tax_rule


def test_creates_from_dict_with_all_fields():
    """
    Test that a CheckoutOptions instance is created from a dictionary with all fields.

    This test verifies that the default tax rate and alternate tax rates are correctly set.

    """
    data = {
        "default": {"rate": 21, "shipping_taxed": True},
        "alternate": [
            {"rate": 21, "country": "NL"},
            {"rate": 19, "country": "DE"},
        ],
    }
    checkout_options = CheckoutOptions.from_dict(data)
    assert checkout_options.default.rate == 21
    assert checkout_options.default.shipping_taxed is True
    assert len(checkout_options.alternate) == 2
    assert checkout_options.alternate[0].rate == 21
    assert checkout_options.alternate[0].country == "NL"
    assert checkout_options.alternate[1].rate == 19
    assert checkout_options.alternate[1].country == "DE"
