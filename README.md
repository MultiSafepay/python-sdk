<p align="center">
    <img src="https://raw.githubusercontent.com/MultiSafepay/MultiSafepay-logos/master/MultiSafepay-logo-color.svg" width="400px" position="center">
</p>

# MultiSafepay Python SDK
[![Code Quality](https://img.shields.io/github/actions/workflow/status/multisafepay/python-sdk/code-quality.yaml?style=for-the-badge)](https://github.com/MultiSafepay/python-sdk/actions/workflows/code-quality.yaml)
[![Codecov](https://img.shields.io/codecov/c/github/multisafepay/python-sdk?style=for-the-badge)](https://app.codecov.io/gh/MultiSafepay/python-sdk)
[![License](https://img.shields.io/github/license/multisafepay/python-sdk?style=for-the-badge)](https://github.com/MultiSafepay/python-sdk/blob/master/LICENSE)
[![Latest stable version](https://img.shields.io/github/v/release/multisafepay/python-sdk?style=for-the-badge)](https://pypi.org/project/multisafepay/)
[![Python versions](https://img.shields.io/pypi/pyversions/multisafepay?style=for-the-badge)](https://pypi.org/project/multisafepay/)

Easily integrate MultiSafepay's payment solutions into your Python applications with this official API client.
This SDK provides convenient access to the MultiSafepay REST API, supports all core payment features, and is designed for seamless integration into any Python-based backend.

## About MultiSafepay

MultiSafepay is a Dutch payment services provider, which takes care of contracts, processing transactions, and
collecting payment for a range of local and international payment methods. Start selling online today and manage all
your transactions in one place!

## Installation

If you want to use the built-in default transport, install with the `requests` extra.

```bash
pip install "multisafepay[requests]"
```

If you want to provide your own transport implementation, install the base package.

```bash
pip install multisafepay
```

## HTTP client / transport (optional dependency)

**WARNING:** This SDK does not have a hard dependency on a specific HTTP client.

The SDK uses a small transport abstraction so you can choose (and swap) the underlying HTTP implementation without affecting the rest of your integration.

### How it works

- The SDK expects an object implementing the `HTTPTransport` / `HTTPResponse` protocols defined in `src/multisafepay/transport/http_transport.py`.
- Event stream subscriptions also require the transport to implement `open_stream(...)` and return an `HTTPStreamResponse` with `readline()`, `close()`, and `raise_for_status()`.
- If you do not provide a transport, the SDK defaults to `RequestsTransport`.
- `requests` is an optional extra:
    - To use the default transport, install `multisafepay[requests]`.
    - To avoid `requests`, inject your own transport (for example, `httpx` or `urllib3`).

The built-in `RequestsTransport` supports both regular requests and SSE streams through the same configured `requests.Session`. Custom transports that only implement `request(...)` can still be used for regular API calls, but SSE subscriptions fail explicitly until `open_stream(...)` is added. The SDK does not fall back to another HTTP library for event streams.

### Custom transport example

```bash
pip install multisafepay
```

```python
from multisafepay import Sdk


sdk = Sdk(
    api_key="<api_key>",
    is_production=False,
    transport=my_custom_transport,  # must implement HTTPTransport
)
```

See transport examples in `examples/transport/` (`httpx_transport.py`, `urllib3_transport.py`, `request_transport.py`).

## Getting started

### Initialize the client

```python
from multisafepay import Sdk

multisafepay_sdk: Sdk = Sdk(api_key='<api_key>', is_production=True)
```

### Initialize with scoped credentials

Use `ScopedCredentialResolver` when different API keys must be selected per auth scope.
When `credential_resolver` is provided, `api_key` becomes optional.

```python
from multisafepay import Sdk
from multisafepay.client import ScopedCredentialResolver


credential_resolver = ScopedCredentialResolver(
    default_api_key="<default_api_key>",
    partner_affiliate_api_key="<partner_api_key>",
    terminal_group_api_keys={
        "<terminal_group_id>": "<terminal_group_api_key>",
    },
)

sdk = Sdk(
    is_production=False,
    credential_resolver=credential_resolver,
)
```

### Event stream subscriptions

Use `EventManager` to subscribe to MultiSafepay SSE streams directly, or to subscribe from an order response that already contains event credentials.

```python
from multisafepay import Sdk
from multisafepay.client import ScopedCredentialResolver


credential_resolver = ScopedCredentialResolver(
    default_api_key="<default_api_key>",
    terminal_group_api_keys={
        "<terminal_group_id>": "<terminal_group_api_key>",
    },
)

sdk = Sdk(
    is_production=False,
    credential_resolver=credential_resolver,
)

order_manager = sdk.get_order_manager()
event_manager = sdk.get_event_manager()

create_response = order_manager.create(
    request_order=order_request,
    terminal_group_id="<terminal_group_id>",
)
order = create_response.get_data()

with event_manager.subscribe_order_events(order, timeout=45.0) as stream:
    for event in stream:
        print(event)
```

Use `subscribe_events(events_token=..., events_stream_url=...)` when the token and stream URL are already available separately.

SSE subscriptions use the same configured SDK transport as regular API calls. With the default transport this reuses the same `requests.Session`; with a custom transport, implement `open_stream(...)` on that transport instead of opening a separate HTTP connection path.

### Development-only custom base URL override

By default, the SDK only targets:

- `test`: `https://testapi.multisafepay.com/v1/`
- `live`: `https://api.multisafepay.com/v1/`

For local development, a custom base URL can be enabled with strict guardrails:

```bash
export MSP_SDK_BUILD_PROFILE=dev
export MSP_SDK_ALLOW_CUSTOM_BASE_URL=1
```

You can provide the custom base URL either via environment variable or via the SDK argument.

Environment variable option:

```bash
export MSP_SDK_CUSTOM_BASE_URL="https://dev-api.example.com/v1"
```

SDK argument option:

```python
from multisafepay import Sdk

sdk = Sdk(
    api_key="<api_key>",
    is_production=False,
    base_url="https://dev-api.example.com/v1",
)
```

Precedence when both are set:

- The explicit SDK argument base_url takes priority.
- If base_url is not passed, MSP_SDK_CUSTOM_BASE_URL is used.

In any non-dev profile (including default `release`), custom base URLs are blocked and the SDK will only use `test/live` URLs.

## Examples

Go to the folder `examples` to see how to use the SDK.

The event-stream example in `examples/event_manager/subscribe_events.py` requires:

```bash
export API_KEY="<account_api_key>"
export TERMINAL_GROUP_API_KEY_GROUP_DEFAULT="<terminal_group_api_key>"
export CLOUD_POS_TERMINAL_GROUP_ID="<terminal_group_id>"
export CLOUD_POS_TERMINAL_ID="<terminal_id>"
```

The SSE E2E test can also run against a dev-backed base URL and optionally resolve the terminal group automatically:

```bash
export E2E_NO_SANDBOX_BASE_URL="https://dev-api.example.com/v1/"
export MSP_SDK_BUILD_PROFILE=dev
export MSP_SDK_ALLOW_CUSTOM_BASE_URL=1
export MSP_SDK_CUSTOM_BASE_URL="https://dev-api.example.com/v1/"
export E2E_API_KEY="<account_api_key>"
export E2E_TERMINAL_GROUP_API_KEY_GROUP_DEFAULT="<terminal_group_api_key>"
export E2E_CLOUD_POS_TERMINAL_ID="<terminal_id>"
# Optional when CLOUD_POS_TERMINAL_GROUP_ID is not set
export E2E_PARTNER_API_KEY="<partner_api_key>"
```

## Code quality checks

### Linting

```bash
make lint
```

## Testing

```bash
make test
```

### E2E target environment

By default, E2E tests target `https://testapi.multisafepay.com/v1/`.

Use dedicated E2E variables instead of the general SDK variables:

```bash
export E2E_API_KEY="<test_api_key>"
export E2E_BASE_URL="https://testapi.multisafepay.com/v1/"  # optional
make test-e2e
```

`E2E_BASE_URL` is optional and can point to any HTTPS base URL used for E2E.
When omitted, E2E defaults to `testapi.multisafepay.com`.

The e2e suite does not use the shared `API_KEY` variable or the shared `MSP_SDK_*`
custom base URL settings.

Terminal endpoint examples and E2E checks use a dev-backed base URL because those endpoints are not exercised against the default shared E2E target.

```bash
export API_KEY="<account_api_key>"
export PARTNER_API_KEY="<partner_api_key>"  # optional
export MSP_SDK_BUILD_PROFILE=dev
export MSP_SDK_ALLOW_CUSTOM_BASE_URL=1
export MSP_SDK_CUSTOM_BASE_URL="https://dev-api.example.com/v1/"
export E2E_CLOUD_POS_TERMINAL_ID="<terminal_id>"
# Optional: set when you want to skip automatic terminal-group lookup
export CLOUD_POS_TERMINAL_GROUP_ID="<terminal_group_id>"
make test-e2e
```

## Support

Create an issue on this repository or email <a href="mailto:integration@multisafepay.com">
integration@multisafepay.com</a>

## Contributors

If you create a pull request to suggest an improvement, we'll send you some MultiSafepay swag as a thank you!

## License

[Open Software License (OSL 3.0)](https://github.com/MultiSafepay/php-sdk/blob/master/LICENSE.md)

## Want to be part of the team?

Are you a developer interested in working at MultiSafepay? Check out
our [job openings](https://www.multisafepay.com/careers/#jobopenings) and feel free to get in touch!
