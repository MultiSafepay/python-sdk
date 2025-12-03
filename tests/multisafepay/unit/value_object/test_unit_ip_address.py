# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Value object for Test Unit Ip Address data."""

from pydantic.error_wrappers import ValidationError
import pytest

from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.value_object.ip_address import IpAddress


def test_ip_address_initialization():
    """Test the initialization of an IpAddress object with a valid IPv4 address."""
    ip = IpAddress(ip_address="192.168.1.1")
    assert ip.ip_address == "192.168.1.1"


def test_empty_ip_address_initialization():
    """Test the initialization of an IpAddress object with no IP address."""
    with pytest.raises(ValidationError):
        IpAddress()


def test_invalid_ip_address_initialization():
    """Test the initialization of an IpAddress object with an invalid IP address (None)."""
    with pytest.raises(ValidationError):
        IpAddress(ip_address=None)


def test_ip_address_initialization_ipv6():
    """Test the initialization of an IpAddress object with a valid IPv6 address."""
    ip = IpAddress(ip_address="2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    assert ip.get() == "2001:0db8:85a3:0000:0000:8a2e:0370:7334"


def test_ip_address_initialization_invalid_ip():
    """Test the initialization of an IpAddress object with an invalid IP address."""
    with pytest.raises(
        InvalidArgumentException,
        match='Value "invalid_ip" is not a valid IP address',
    ):
        IpAddress(ip_address="invalid_ip")


def test_ip_address_initialization_comma_separated_ips():
    """Test the initialization of an IpAddress object with a comma-separated list of IP addresses."""
    ip = IpAddress(ip_address="192.168.1.1, 10.0.0.1")
    assert ip.get() == "192.168.1.1"


def test_ip_address_get():
    """Test the get method of the IpAddress object."""
    ip = IpAddress(ip_address="192.168.1.1")
    assert ip.get() == "192.168.1.1"
