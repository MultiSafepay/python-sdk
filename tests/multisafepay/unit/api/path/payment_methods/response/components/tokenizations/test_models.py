# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.paths.payment_methods.response.components.tokenizations.models import (
    Models,
)


def test_initializes_correctly():
    """
    Test that the Models object initializes correctly with given values.

    This test verifies that the Models object is initialized with the provided
    cardonfile, subscription, and unscheduled attributes.

    Assertions:
    - The cardonfile value should be True.
    - The subscription value should be False.
    - The unscheduled value should be True.
    """
    models = Models(cardonfile=True, subscription=False, unscheduled=True)
    assert models.cardonfile is True
    assert models.subscription is False
    assert models.unscheduled is True


def test_initializes_with_none_values():
    """
    Test that Models initializes with None values.

    This test verifies that all attributes are optional.

    Assertions:
    - The cardonfile value should be None.
    - The subscription value should be None.
    - The unscheduled value should be None.
    """
    models = Models()
    assert models.cardonfile is None
    assert models.subscription is None
    assert models.unscheduled is None


def test_from_dict_creates_models_instance_correctly():
    """
    Test that from_dict method creates a Models instance correctly.

    This test verifies that the from_dict method of the Models class
    creates a Models instance with the correct attributes from a dictionary.

    Assertions:
    - The created Models instance should have True for cardonfile.
    - The created Models instance should have False for subscription.
    - The created Models instance should have True for unscheduled.
    """
    data = {"cardonfile": True, "subscription": False, "unscheduled": True}
    models = Models.from_dict(data)
    assert models.cardonfile is True
    assert models.subscription is False
    assert models.unscheduled is True


def test_from_dict_returns_none_for_none_input():
    """
    Test that from_dict method returns None for None input.

    This test verifies that the from_dict method of the Models class
    returns None when the input dictionary is None.

    Assertions:
    - The returned value should be None.
    """
    assert Models.from_dict(None) is None


def test_from_dict_handles_missing_fields():
    """
    Test that from_dict method handles missing fields correctly.

    This test verifies that the from_dict method of the Models class
    handles missing fields in the input dictionary correctly.

    Assertions:
    - The created Models instance should have None for cardonfile.
    - The created Models instance should have None for subscription.
    - The created Models instance should have None for unscheduled.
    """
    data = {}
    models = Models.from_dict(data)
    assert models.cardonfile is None
    assert models.subscription is None
    assert models.unscheduled is None
