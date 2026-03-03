"""Example: Injecting an httpx-based transport.

This example demonstrates the recommended pattern for using a different HTTP
client than requests, without the SDK having to maintain “official” adapters.

Requirements
------------
- `pip install httpx`
- `API_KEY` in the environment (optionally via a `.env` + python-dotenv)

Notes
-----
- `httpx.Response` already exposes `status_code`, `headers`, `.json()` and
    `.raise_for_status()`, so we don't need to adapt the response object.
- We only adapt the *transport* (how requests are executed) to match the SDK's
    `HTTPTransport.request(...)` contract.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from multisafepay import Sdk


class HttpxTransport:
    """Minimal `HTTPTransport` implementation backed by httpx."""

    def __init__(self, client: Optional[Any] = None) -> None:
        import httpx

        self._httpx = httpx
        self.client = client or httpx.Client()

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        **kwargs: Any,
    ) -> Any:
        # The SDK may pass `data` as a dict; in httpx this should be sent as `json=`.
        request_kwargs: Dict[str, Any] = {
            "method": method,
            "url": url,
            "headers": headers,
            "params": params,
            **kwargs,
        }

        if data is not None:
            if isinstance(data, (dict, list)):
                request_kwargs["json"] = data
            else:
                request_kwargs["content"] = data

        return self.client.request(**request_kwargs)

    def close(self) -> None:
        self.client.close()


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise SystemExit("Missing API_KEY env var")

    transport = HttpxTransport()
    try:
        sdk = Sdk(api_key=api_key, is_production=False, transport=transport)
        gateways = sdk.get_gateway_manager().get_gateways().get_data()
        print(gateways)
    finally:
        transport.close()
