# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.paths.payment_methods.response.components.app import App


def test_initializes_correctly():
    """
    Test that the App object initializes correctly with given parameters.

    This test verifies that the App object is initialized with the correct
    is_enabled, has_fields, and qr values.
    """
    app = App(is_enabled=True, has_fields=False, qr=None)
    assert app.is_enabled is True
    assert app.has_fields is False
    assert app.qr is None


def test_from_dict_creates_app_instance_correctly():
    """
    Test that from_dict method creates an App instance correctly.

    This test verifies that the from_dict method of the App class
    creates an App instance with the correct attributes from a dictionary.
    """
    data = {"is_enabled": True, "has_fields": False, "qr": None}
    app = App.from_dict(data)
    assert app.is_enabled is True
    assert app.has_fields is False
    assert app.qr is None


def test_from_dict_returns_none_for_none_input():
    """
    Test that from_dict method returns None for None input.

    This test verifies that the from_dict method of the App class
    returns None when the input dictionary is None.
    """
    assert App.from_dict(None) is None


def test_from_dict_handles_missing_fields():
    """
    Test that from_dict method handles missing fields correctly.

    This test verifies that the from_dict method of the App class
    creates an App instance with None for missing fields in the input dictionary.
    """
    data = {"is_enabled": True}
    app = App.from_dict(data)
    assert app.is_enabled is True
    assert app.has_fields is None
    assert app.qr is None
