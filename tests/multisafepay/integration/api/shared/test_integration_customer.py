# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.shared.customer import Customer
from multisafepay.value_object.ip_address import IpAddress


def test_adds_ip_address():
    """
    Test that an IP address is added to the Customer instance.

    This test verifies that the IP address is correctly set.

    """
    ip_address = IpAddress(ip_address="192.168.0.1")
    customer = Customer().add_ip_address(ip_address)
    assert customer.ip_address == "192.168.0.1"


def test_adds_ip_address_as_string():
    """
    Test that an IP address is added to the Customer instance as a string.

    This test verifies that the IP address is correctly set.

    """
    customer = Customer().add_ip_address("192.168.0.1")
    assert customer.ip_address == "192.168.0.1"


def test_adds_forwarded_ip():
    """
    Test that a forwarded IP address is added to the Customer instance.

    This test verifies that the forwarded IP address is correctly set.


    """
    forwarded_ip = IpAddress(ip_address="10.0.0.1")
    customer = Customer().add_forwarded_ip(forwarded_ip)
    assert customer.forwarded_ip == "10.0.0.1"


def test_adds_forwarded_ip_as_string():
    """
    Test that a forwarded IP address is added to the Customer instance as a string.

    This test verifies that the forwarded IP address is correctly set.

    """
    customer = Customer().add_forwarded_ip("10.0.0.1")
    assert customer.forwarded_ip == "10.0.0.1"
