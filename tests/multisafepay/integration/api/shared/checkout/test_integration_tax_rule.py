# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.shared.checkout.tax_rate import TaxRate
from multisafepay.api.shared.checkout.tax_rule import TaxRule


def test_initializes_with_valid_values():
    """
    Test that a TaxRule instance initializes with valid values.

    This test verifies that the name, rules, and standalone attributes are correctly set.

    """
    tax_rule = TaxRule(
        name="Standard Tax",
        rules=[TaxRate(rate=21, country="NL")],
        standalone=True,
    )
    assert tax_rule.name == "Standard Tax"
    assert len(tax_rule.rules) == 1
    assert tax_rule.rules[0].rate == 21
    assert tax_rule.rules[0].country == "NL"
    assert tax_rule.standalone is True


def test_creates_from_dict_with_name_and_rules():
    """
    Test that a TaxRule instance is created from a dictionary with name and rules.

    """
    data = {"name": "Standard Tax", "rules": [{"rate": 21, "country": "NL"}]}
    tax_rule = TaxRule.from_dict(data)
    assert tax_rule.name == "Standard Tax"
    assert len(tax_rule.rules) == 1
    assert tax_rule.rules[0].rate == 21
    assert tax_rule.rules[0].country == "NL"


def test_creates_from_dict_with_only_rules():
    """
    Test that a TaxRule instance is created from a dictionary with only rules.

    """
    data = {"rules": [{"rate": 21, "country": "NL"}]}
    tax_rule = TaxRule.from_dict(data)
    assert tax_rule.name is None
    assert len(tax_rule.rules) == 1
    assert tax_rule.rules[0].rate == 21
    assert tax_rule.rules[0].country == "NL"


def test_adds_rules():
    """
    Test that rules are added to a TaxRule instance.

    """
    tax_rule = TaxRule()
    tax_rates = [TaxRate(rate=21, country="NL")]
    tax_rule.add_rules(tax_rates)
    assert len(tax_rule.rules) == 1
    assert tax_rule.rules[0].rate == 21
    assert tax_rule.rules[0].country == "NL"


def test_adds_single_rule():
    """
    Test that a single rule is added to a TaxRule instance.

    """
    tax_rule = TaxRule()
    tax_rate = TaxRate(rate=21, country="NL")
    tax_rule.add_rule(tax_rate)
    assert len(tax_rule.rules) == 1
    assert tax_rule.rules[0].rate == 21
    assert tax_rule.rules[0].country == "NL"
