# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""HTTP client module for making API requests to MultiSafepay services."""

from typing import Any, Optional

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.transport import HTTPTransport, RequestsTransport

from ..exception.api import ApiException
from .api_key import ApiKey


class Client:
    """
    Client for interacting with the MultiSafepay API.

    Attributes
    ----------
    LIVE_URL (str): The live API URL.
    TEST_URL (str): The test API URL.
    METHOD_POST (str): HTTP POST method.
    METHOD_GET (str): HTTP GET method.
    METHOD_PATCH (str): HTTP PATCH method.
    METHOD_DELETE (str): HTTP DELETE method.

    """

    LIVE_URL = "https://api.multisafepay.com/v1/"
    TEST_URL = "https://testapi.multisafepay.com/v1/"

    METHOD_POST = "POST"
    METHOD_GET = "GET"
    METHOD_PATCH = "PATCH"
    METHOD_DELETE = "DELETE"

    def __init__(
        self: "Client",
        api_key: str,
        is_production: bool,
        transport: Optional[HTTPTransport] = None,
        locale: str = "en_US",
    ) -> None:
        """
        Initialize the Client.

        Parameters
        ----------
        api_key (str): The API key for authentication.
        is_production (bool): Flag indicating if the client is in production mode.
        transport (Optional[HTTPTransport], optional): Custom HTTP transport implementation.
            Defaults to RequestsTransport if not provided.
        locale (str, optional): Locale for the requests. Defaults to "en_US".

        """
        self.api_key = ApiKey(api_key=api_key)
        self.url = self.LIVE_URL if is_production else self.TEST_URL
        self.transport = transport or RequestsTransport()
        self.locale = locale

    def create_get_request(
        self: "Client",
        endpoint: str,
        params: dict[str, Any] = None,
        context: dict[str, Any] = None,
    ) -> ApiResponse:
        """
        Create a GET request.

        Parameters
        ----------
        endpoint (str): The API endpoint.
        params (Dict[str, Any], optional): Query parameters. Defaults to None.
        context (Dict[str, Any], optional): Additional context for the request. Defaults to None.

        Returns
        -------
        ApiResponse: The API response.

        """
        url = self._build_url(endpoint, params)
        return self._create_request(
            self.METHOD_GET,
            url,
            context=context,
        )

    def create_post_request(
        self: "Client",
        endpoint: str,
        params: dict[str, Any] = None,
        request_body: str = None,
        context: dict[str, Any] = None,
    ) -> ApiResponse:
        """
        Create a POST request.

        Parameters
        ----------
        endpoint (str): The API endpoint.
        params (Dict[str, Any], optional): Query parameters. Defaults to None.
        request_body (str, optional): The request body. Defaults to None.
        context (Dict[str, Any], optional): Additional context for the request. Defaults to None.

        Returns
        -------
        ApiResponse: The API response.

        """
        url = self._build_url(endpoint, params)
        return self._create_request(
            self.METHOD_POST,
            url,
            request_body=request_body,
            context=context,
        )

    def create_patch_request(
        self: "Client",
        endpoint: str,
        params: dict[str, Any] = None,
        request_body: str = None,
        context: dict[str, Any] = None,
    ) -> ApiResponse:
        """
        Create a PATCH request.

        Parameters
        ----------
        endpoint (str): The API endpoint.
        params (Dict[str, Any], optional): Query parameters. Defaults to None.
        request_body (Optional[RequestBodyInterface], optional): The request body. Defaults to None.
        context (Dict[str, Any], optional): Additional context for the request. Defaults to None.

        Returns
        -------
        ApiResponse: The API response.

        """
        url = self._build_url(endpoint, params)
        return self._create_request(
            self.METHOD_PATCH,
            url,
            request_body=request_body,
            context=context,
        )

    def create_delete_request(
        self: "Client",
        endpoint: str,
        params: dict[str, Any] = None,
        context: dict[str, Any] = None,
    ) -> ApiResponse:
        """
        Create a DELETE request.

        Parameters
        ----------
        endpoint (str): The API endpoint.
        params (Dict[str, Any], optional): Query parameters. Defaults to None.
        context (Dict[str, Any], optional): Additional context for the request. Defaults to None.

        Returns
        -------
        ApiResponse: The API response.

        """
        url = self._build_url(endpoint, params)
        return self._create_request(self.METHOD_DELETE, url, context=context)

    def _build_url(
        self: "Client",
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
    ) -> str:
        """
        Build the full URL for the request.

        Parameters
        ----------
        endpoint (str): The API endpoint.
        params (Optional[Dict[str, Any]], optional): Query parameters. Defaults to None.

        Returns
        -------
        str: The full URL.

        """
        if params is None:
            params = {}
        if "locale" not in params:
            params["locale"] = self.locale
        query_string = "&".join(
            f"{key}={value}" for key, value in params.items()
        )
        return f"{self.url}{endpoint}?{query_string}"

    def _create_request(
        self: "Client",
        method: str,
        url: str,
        request_body: Optional[dict[str, Any]] = None,
        context: dict[str, Any] = None,
    ) -> ApiResponse:
        """
        Create and send an HTTP request.

        Parameters
        ----------
        method (str): The HTTP method.
        url (str): The full URL.
        request_body (Optional[Dict[str, Any]], optional): The request body. Defaults to None.
        context (Dict[str, Any], optional): Additional context for the request. Defaults to None.

        Returns
        -------
        ApiResponse: The API response.

        """
        headers = {
            "Authorization": "Bearer " + self.api_key.get(),
            "accept-encoding": "application/json",
            "Content-Type": "application/json",
        }

        try:
            response = self.transport.request(
                method=method,
                url=url,
                headers=headers,
                data=request_body,
            )
            response.raise_for_status()
        except Exception as e:
            if (
                hasattr(response, "status_code")
                and 500 <= response.status_code < 600
            ):
                raise ApiException(f"Request failed: {e}") from e
            raise

        context = context or {}
        context.update(
            {
                "headers": headers,
                "request_body": request_body,
            },
        )
        return ApiResponse.with_json(
            status_code=response.status_code,
            json_data=response.json(),
            headers=response.headers,
            context=context,
        )
