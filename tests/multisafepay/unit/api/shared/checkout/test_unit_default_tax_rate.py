# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the default tax rate shared model."""


from multisafepay.api.shared.checkout.default_tax_rate import DefaultTaxRate


def test_initializes_with_valid_values():
    """
    Test that a DefaultTaxRate instance initializes with valid values.
    """
    default_tax_rate = DefaultTaxRate(rate=21, shipping_taxed=True)
    assert default_tax_rate.rate == 21
    assert default_tax_rate.shipping_taxed is True


def test_initializes_with_default_values():
    """
    Test that a DefaultTaxRate instance initializes with default values.
    """
    default_tax_rate = DefaultTaxRate()
    assert default_tax_rate.rate is None
    assert default_tax_rate.shipping_taxed is None


def test_creates_from_dict_with_rate_and_shipping_taxed():
    """
    Test that a DefaultTaxRate instance is created from a dictionary with rate and shipping taxed.
    """
    data = {"rate": 21, "shipping_taxed": True}
    default_tax_rate = DefaultTaxRate.from_dict(data)
    assert default_tax_rate.rate == 21
    assert default_tax_rate.shipping_taxed is True


def test_creates_from_dict_with_only_rate():
    """
    Test that a DefaultTaxRate instance is created from a dictionary with only rate.
    """
    data = {"rate": 21}
    default_tax_rate = DefaultTaxRate.from_dict(data)
    assert default_tax_rate.rate == 21
    assert default_tax_rate.shipping_taxed is None


def test_creates_from_dict_with_only_shipping_taxed():
    """
    Test that a DefaultTaxRate instance is created from a dictionary with only shipping taxed.
    """
    data = {"shipping_taxed": True}
    default_tax_rate = DefaultTaxRate.from_dict(data)
    assert default_tax_rate.rate is None
    assert default_tax_rate.shipping_taxed is True


def test_creates_from_empty_dict():
    """
    Test that a DefaultTaxRate instance is created from an empty dictionary.
    """
    data = {}
    default_tax_rate = DefaultTaxRate.from_dict(data)
    assert default_tax_rate.rate is None
    assert default_tax_rate.shipping_taxed is None


def test_creates_from_none():
    """
    Test that a DefaultTaxRate instance is created from None.
    """
    default_tax_rate = DefaultTaxRate.from_dict(None)
    assert default_tax_rate is None


def test_adds_rate():
    """
    Test that a rate is added to a DefaultTaxRate instance.
    """
    default_tax_rate = DefaultTaxRate()
    default_tax_rate.add_rate(21)
    assert default_tax_rate.rate == 21


def test_adds_shipping_taxed():
    """
    Test that shipping taxed information is added to a DefaultTaxRate instance.
    """
    default_tax_rate = DefaultTaxRate()
    default_tax_rate.add_shipping_taxed(True)
    assert default_tax_rate.shipping_taxed is True
