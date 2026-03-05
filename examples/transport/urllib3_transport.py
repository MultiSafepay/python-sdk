"""Example: Injecting an urllib3-based transport (with response adaptation).

Unlike requests/httpx, urllib3 is lower-level and its response object does NOT
expose the typical high-level interface (`status_code`, `.json()`,
`.raise_for_status()`).

This is why the example shows the full pattern:
- A `Transport` that executes the request via `urllib3.PoolManager`
- A `ResponseAdapter` that translates urllib3 responses into what the SDK expects

Requirements
------------
- `pip install urllib3`
- `API_KEY` in the environment (optionally via a `.env` + python-dotenv)
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from multisafepay import Sdk


@dataclass
class Urllib3ResponseAdapter:
    """Adapter: urllib3.HTTPResponse -> interface expected by the SDK."""

    response: Any

    @property
    def status_code(self) -> int:
        return int(getattr(self.response, "status"))

    @property
    def headers(self) -> Dict[str, str]:
        raw = getattr(self.response, "headers", {})
        return {str(k): str(v) for k, v in dict(raw).items()}

    def json(self) -> Any:
        data = getattr(self.response, "data", b"")
        if data is None:
            return None
        text = data if isinstance(data, str) else data.decode("utf-8")
        return json.loads(text) if text else {}

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise Exception(f"HTTP Error {self.status_code}")


class Urllib3Transport:
    """Minimal `HTTPTransport` implementation backed by urllib3."""

    def __init__(self, pool_manager: Optional[Any] = None) -> None:
        urllib3 = __import__("urllib3")
        self._pool = pool_manager or urllib3.PoolManager()

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,  # noqa: ARG002
        data: Optional[Any] = None,
        **kwargs: Any,
    ) -> Urllib3ResponseAdapter:
        # The SDK already bakes query parameters into `url`; avoid re-applying `params`.
        body: Optional[bytes]
        if data is None:
            body = None
        elif isinstance(data, (bytes, bytearray)):
            body = bytes(data)
        elif isinstance(data, str):
            body = data.encode("utf-8")
        else:
            body = json.dumps(data).encode("utf-8")

        resp = self._pool.request(
            method=method,
            url=url,
            body=body,
            headers=headers,
            **kwargs,
        )
        return Urllib3ResponseAdapter(resp)


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise SystemExit("Missing API_KEY env var")

    transport = Urllib3Transport()
    sdk = Sdk(api_key=api_key, is_production=False, transport=transport)
    gateways = sdk.get_gateway_manager().get_gateways().get_data()
    print(gateways)
