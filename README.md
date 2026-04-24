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
- If you do not provide a transport, the SDK defaults to `RequestsTransport`.
- `requests` is an optional extra:
    - To use the default transport, install `multisafepay[requests]`.
    - To avoid `requests`, inject your own transport (for example, `httpx` or `urllib3`).

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
    terminal_group_api_keys={
        "Default": "<terminal_group_api_key>",
    },
    partner_affiliate_api_key="<partner_api_key>",
)

sdk = Sdk(
    is_production=False,
    credential_resolver=credential_resolver,
)
```

Resolver behavior:

- `default_api_key` is used for regular account-scoped requests.
- `partner_affiliate_api_key` is used for partner-affiliate scoped requests and falls back to `default_api_key` when omitted.

### Terminal and terminal-group operations

The SDK exposes dedicated managers for POS terminal listing/creation and for listing terminals inside a specific terminal group.

```python
from multisafepay.client import ScopedCredentialResolver
from multisafepay import Sdk


credential_resolver = ScopedCredentialResolver(
    default_api_key="<default_api_key>",
    partner_affiliate_api_key="<partner_api_key>",
)

sdk = Sdk(
    is_production=False,
    credential_resolver=credential_resolver,
)

terminal_manager = sdk.get_terminal_manager()
terminal_group_manager = sdk.get_terminal_group_manager()

terminals = terminal_manager.get_terminals(options={"limit": 10, "page": 1})
group_terminals = terminal_group_manager.get_terminals_by_group(
    terminal_group_id="<terminal_group_id>",
    options={"limit": 10, "page": 1},
)
```

See terminal examples in `examples/terminal_manager/` and `examples/terminal_group_manager/`.

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
