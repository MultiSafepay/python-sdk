# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""HTTP client module for making API requests to MultiSafepay services."""

import os
from typing import Any, Optional
from urllib.parse import urlparse

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
    BUILD_PROFILE_ENV = "MSP_SDK_BUILD_PROFILE"
    CUSTOM_BASE_URL_ENV = "MSP_SDK_CUSTOM_BASE_URL"
    ALLOW_CUSTOM_BASE_URL_ENV = "MSP_SDK_ALLOW_CUSTOM_BASE_URL"

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
        base_url: Optional[str] = None,
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
        base_url (Optional[str], optional): Custom API base URL.
            Only allowed when running with `MSP_SDK_BUILD_PROFILE=dev`
            and `MSP_SDK_ALLOW_CUSTOM_BASE_URL=1`.

        """
        self.api_key = ApiKey(api_key=api_key)
        self.url = self._resolve_base_url(
            is_production=is_production,
            explicit_base_url=base_url,
        )
        self.transport = transport or RequestsTransport()
        self.locale = locale

    def _resolve_base_url(
        self: "Client",
        is_production: bool,
        explicit_base_url: Optional[str],
    ) -> str:
        profile = os.getenv(self.BUILD_PROFILE_ENV, "release").strip().lower()
        if profile != "dev":
            profile = "release"

        env_base_url = os.getenv(self.CUSTOM_BASE_URL_ENV, "").strip()
        requested_base_url = (explicit_base_url or env_base_url or "").strip()

        if not requested_base_url:
            return self.LIVE_URL if is_production else self.TEST_URL

        allow_custom = os.getenv(
            self.ALLOW_CUSTOM_BASE_URL_ENV,
            "0",
        ).strip().lower() in {"1", "true", "yes"}

        if profile != "dev" or not allow_custom:
            msg = (
                "Custom base URL is only allowed in dev profile with "
                "MSP_SDK_ALLOW_CUSTOM_BASE_URL enabled."
            )
            raise ValueError(msg)

        return self._normalize_base_url(requested_base_url)

    @staticmethod
    def _normalize_base_url(base_url: str) -> str:
        parsed = urlparse(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Invalid custom base URL.")

        if parsed.query or parsed.fragment:
            raise ValueError("Invalid custom base URL.")

        path = parsed.path.rstrip("/")
        path = "/" if not path else path + "/"

        return f"{parsed.scheme}://{parsed.netloc}{path}"

    def create_get_request(
        self: "Client",
        endpoint: str,
        params: dict[str, Any] = None,
        context: Optional[dict[str, Any]] = None,
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
        context: Optional[dict[str, Any]] = None,
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
        context: Optional[dict[str, Any]] = None,
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
        context: Optional[dict[str, Any]] = None,
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
        context: Optional[dict[str, Any]] = None,
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
