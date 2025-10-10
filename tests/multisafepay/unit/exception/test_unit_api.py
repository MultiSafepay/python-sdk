# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for API exception handling."""


from multisafepay.exception.api import ApiException


def test_api_exception_initialization():
    """
    Test the initialization of ApiException.

    """
    exception = ApiException("An error occurred")
    assert str(exception) == "An error occurred"
    assert exception.context == {}


def test_api_exception_initialization__string__():
    """
    Test the initialization of ApiException with a string representation.

    """
    context = {"key": "value"}
    exception = ApiException("An error occurred", context)
    assert str(exception) == "('An error occurred', {'key': 'value'})"


def test_api_exception_initialization_with_context():
    """
    Test the initialization of ApiException with context.

    """
    context = {"key": "value"}
    exception = ApiException("An error occurred", context)
    assert exception.get_message() == "An error occurred"
    assert exception.context == context


def test_add_context():
    """
    Test adding context to ApiException.

    """
    exception = ApiException("An error occurred")
    exception.add_context({"key": "value"})
    assert exception.context == {"key": "value"}


def test_get_details():
    """
    Test getting details from ApiException.

    """
    context = {"key": "value"}
    exception = ApiException("An error occurred", context)
    details = exception.get_details()
    expected_details = "ApiException: An error occurred\nkey: value"
    assert details == expected_details


def test_get_context_as_array():
    """
    Test getting context as an array from ApiException.

    """
    context = {"key": "value"}
    exception = ApiException("An error occurred", context)
    context_array = exception.get_context_as_array()
    expected_context_array = ["key: value"]
    assert context_array == expected_context_array


def test_get_context_value():
    """
    Test getting a specific context value from ApiException.

    """
    context = {"key": "value"}
    exception = ApiException("An error occurred", context)
    assert exception.get_context_value("key") == "value"
    assert exception.get_context_value("nonexistent_key") is None
