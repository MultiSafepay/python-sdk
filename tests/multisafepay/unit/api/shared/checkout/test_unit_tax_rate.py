# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the tax rate shared model."""


from multisafepay.api.shared.checkout.tax_rate import TaxRate


def test_initializes_with_valid_values():
    """Test that a TaxRate instance initializes with valid values."""
    tax_rate = TaxRate(rate=21, country="NL")
    assert tax_rate.rate == 21
    assert tax_rate.country == "NL"


def test_initializes_with_default_values():
    """Test that a TaxRate instance initializes with default values."""
    tax_rate = TaxRate()
    assert tax_rate.rate is None
    assert tax_rate.country == ""


def test_creates_from_dict_with_rate_and_country():
    """Test that a TaxRate instance is created from a dictionary with rate and country."""
    data = {"rate": 21, "country": "NL"}
    tax_rate = TaxRate.from_dict(data)
    assert tax_rate.rate == 21
    assert tax_rate.country == "NL"


def test_creates_from_dict_with_only_rate():
    """Test that a TaxRate instance is created from a dictionary with only rate."""
    data = {"rate": 21}
    tax_rate = TaxRate.from_dict(data)
    assert tax_rate.rate == 21
    assert tax_rate.country == ""


def test_creates_from_dict_with_only_country():
    """Test that a TaxRate instance is created from a dictionary with only country."""
    data = {"country": "NL"}
    tax_rate = TaxRate.from_dict(data)
    assert tax_rate.rate is None
    assert tax_rate.country == "NL"


def test_creates_from_empty_dict():
    """Test that a TaxRate instance is created from an empty dictionary."""
    data = {}
    tax_rate = TaxRate.from_dict(data)
    assert tax_rate.rate is None
    assert tax_rate.country == ""


def test_creates_from_none():
    """Test that a TaxRate instance is created from None."""
    tax_rate = TaxRate.from_dict(None)
    assert tax_rate is None


def test_adds_rate():
    """Test that a rate is added to a TaxRate instance."""
    tax_rate = TaxRate()
    tax_rate.add_rate(21)
    assert tax_rate.rate == 21


def test_adds_country():
    """Test that a country is added to a TaxRate instance."""
    tax_rate = TaxRate()
    tax_rate.add_country("NL")
    assert tax_rate.country == "NL"
