# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the tax rule shared model."""

from multisafepay.api.shared.checkout.tax_rule import TaxRule


def test_initializes_with_default_values():
    """
    Test that a TaxRule instance initializes with default values.
    """
    tax_rule = TaxRule()
    assert tax_rule.name is None
    assert tax_rule.rules is None
    assert tax_rule.standalone is None


def test_creates_from_dict_with_only_name():
    """
    Test that a TaxRule instance is created from a dictionary with only a name.
    """
    data = {"name": "Standard Tax"}
    tax_rule = TaxRule.from_dict(data)
    assert tax_rule.name == "Standard Tax"
    assert tax_rule.rules is None


def test_creates_from_empty_dict():
    """
    Test that a TaxRule instance is created from an empty dictionary.
    """
    data = {}
    tax_rule = TaxRule.from_dict(data)
    assert tax_rule.name is None
    assert tax_rule.rules is None


def test_creates_from_none():
    """
    Test that a TaxRule instance is created from None.
    """
    tax_rule = TaxRule.from_dict(None)
    assert tax_rule is None


def test_adds_standalone():
    """
    Test that standalone information is added to a TaxRule instance.
    """
    tax_rule = TaxRule()
    tax_rule.add_standalone(True)
    assert tax_rule.standalone is True
