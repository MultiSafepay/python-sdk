# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.paths.payment_methods.response.components.qr import Qr


def test_initializes_correctly():
    """
    Test that the Qr object initializes correctly with given values.

    This test verifies that the Qr object is initialized with the provided
    supported attribute.
    """
    qr = Qr(supported=True)
    assert qr.supported is True


def test_from_dict_creates_qr_instance_correctly():
    """
    Test that from_dict method creates a Qr instance correctly.

    This test verifies that the from_dict method of the Qr class
    creates a Qr instance with the correct attributes from a dictionary.
    """
    data = {"supported": True}
    qr = Qr.from_dict(data)
    assert qr.supported is True


def test_from_dict_returns_none_for_none_input():
    """
    Test that from_dict method returns None for None input.

    This test verifies that the from_dict method of the Qr class
    returns None when the input dictionary is None.
    """
    assert Qr.from_dict(None) is None


def test_from_dict_handles_missing_fields():
    """
    Test that from_dict method handles missing fields correctly.

    This test verifies that the from_dict method of the Qr class
    handles missing fields in the input dictionary correctly.
    """
    data = {}
    qr = Qr.from_dict(data)
    assert qr.supported is None
