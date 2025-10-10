# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the base API response wrapper."""


from multisafepay.api.base.response.api_response import ApiResponse


def test_with_json_creates_response():
    """
    Test that ApiResponse.with_json creates a response with the correct attributes.

    Raises
    ------
    AssertionError
        If any of the response attributes do not match the expected values.

    """
    status_code = 200
    json_data = {"key": "value"}
    headers = {"Content-Type": "application/json"}
    context = {"user": "test"}

    response = ApiResponse.with_json(status_code, json_data, headers, context)

    assert response.status_code == status_code
    assert response.body == json_data
    assert response.headers == headers
    assert response.context == context
    assert response.raw == str(json_data)


def test_get_body_data_returns_data():
    """
    Test that get_body_data returns the correct data from the response body.

    Raises
    ------
    AssertionError
        If the returned data does not match the expected value.

    """
    response = ApiResponse(
        status_code=200,
        body={"data": {"key": "value"}},
        context={},
        headers={},
        raw="",
    )
    assert response.get_body_data() == {"key": "value"}


def test_get_body_success_returns_none():
    """
    Test that get_body_success returns None when the success key is not present in the response body.

    Raises
    ------
    AssertionError
        If the returned success status is not None.

    """
    response = ApiResponse(
        status_code=200,
        body={},
        context={},
        headers={},
        raw="",
    )
    assert response.get_body_success() is None


def test_get_body_error_code_returns_code():
    """
    Test that get_body_error_code returns the correct error code from the response body.

    Raises
    ------
    AssertionError
        If the returned error code does not match the expected value.

    """
    response = ApiResponse(
        status_code=200,
        body={"error_code": 404},
        context={},
        headers={},
        raw="",
    )
    assert response.get_body_error_code() == 404


def test_get_body_error_info_returns_info():
    """
    Test that get_body_error_info returns the correct error information from the response body.

    Raises
    ------
    AssertionError
        If the returned error information does not match the expected value.

    """
    response = ApiResponse(
        status_code=200,
        body={"error_info": "Not Found"},
        context={},
        headers={},
        raw="",
    )
    assert response.get_body_error_info() == "Not Found"


def test_get_context_returns_context():
    """
    Test that get_context returns the correct context from the response.

    Raises
    ------
    AssertionError
        If the returned context does not match the expected value.

    """
    context = {"user": "test"}
    response = ApiResponse(
        status_code=200,
        body={},
        context=context,
        headers={},
        raw="",
    )
    assert response.get_context() == context


def test_get_headers_returns_headers():
    """
    Test that get_headers returns the correct headers from the response.

    Raises
    ------
    AssertionError
        If the returned headers do not match the expected value.

    """
    headers = {"Content-Type": "application/json"}
    response = ApiResponse(
        status_code=200,
        body={},
        context={},
        headers=headers,
        raw="",
    )
    assert response.get_headers() == headers


def test_get_status_code_returns_status_code():
    """
    Test that get_status_code returns the correct status code from the response.

    Raises
    ------
    AssertionError
        If the returned status code does not match the expected value.

    """
    response = ApiResponse(
        status_code=200,
        body={},
        context={},
        headers={},
        raw="",
    )
    assert response.get_status_code() == 200


def test_get_raw_returns_raw():
    """
    Test that get_raw returns the correct raw response data as a string.

    Raises
    ------
    AssertionError
        If the returned raw data does not match the expected value.

    """
    raw = '{"key": "value"}'
    response = ApiResponse(
        status_code=200,
        body={},
        context={},
        headers={},
        raw=raw,
    )
    assert response.get_raw() == raw
