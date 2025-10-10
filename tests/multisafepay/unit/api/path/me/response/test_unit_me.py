# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the me response model."""


from multisafepay.api.paths.me.response.me import Me


def test_initializes_correctly():
    """
    Test that the Me object initializes correctly with given parameters.

    This test verifies that the Me object is initialized with the correct
    account_id, role, and site_id.
    """
    me = Me(account_id=1, role="admin", site_id=100)
    assert me.account_id == 1
    assert me.role == "admin"
    assert me.site_id == 100


def test_initializes_with_none_values():
    """
    Test that Me initializes with None values.

    This test verifies that all attributes all optional.
    """
    me = Me()
    assert me.account_id is None
    assert me.role is None
    assert me.site_id is None


def test_from_dict_creates_me_instance_correctly():
    """
    Test that from_dict method creates a Me instance correctly.

    This test verifies that the from_dict method of the Me class
    creates a Me instance with the correct attributes from a dictionary.
    """
    data = {"account_id": 1, "role": "admin", "site_id": 100}
    me = Me.from_dict(data)
    assert me.account_id == 1
    assert me.role == "admin"
    assert me.site_id == 100


def test_from_dict_handles_missing_fields():
    """
    Test that from_dict method handles missing fields correctly.

    This test verifies that the from_dict method of the Me class
    """
    data = {}
    me = Me.from_dict(data)
    assert me.account_id is None
    assert me.role is None
    assert me.site_id is None


def test_from_dict_returns_none_for_none_input():
    """
    Test that from_dict method returns None for None input.

    This test verifies that the from_dict method of the Me class
    returns None when the input dictionary is None.
    """
    assert Me.from_dict(None) is None
