<p align="center">
    <img src="https://raw.githubusercontent.com/MultiSafepay/MultiSafepay-logos/master/MultiSafepay-logo-color.svg" width="400px" position="center">
</p>

# MultiSafepay Python SDK
[![PyPI version](https://img.shields.io/pypi/v/multisafepay?style=for-the-badge)](https://pypi.org/project/multisafepay/)
[![Python versions](https://img.shields.io/pypi/pyversions/multisafepay?style=for-the-badge)](https://pypi.org/project/multisafepay/)
[![License](https://img.shields.io/github/license/multisafepay/python-sdk?style=for-the-badge)](https://github.com/MultiSafepay/python-sdk/blob/master/LICENSE)
[![Code Quality](https://img.shields.io/github/actions/workflow/status/multisafepay/python-sdk/code-quality.yaml?style=for-the-badge)](https://github.com/MultiSafepay/python-sdk/actions/workflows/code-quality.yaml)
[![Codecov](https://img.shields.io/codecov/c/github/multisafepay/python-sdk?style=for-the-badge)](https://app.codecov.io/gh/MultiSafepay/python-sdk)
[![Downloads](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=downloads&query=total_downloads&url=https%3A%2F%2Fpepy.tech%2Fapi%2Fprojects%2Fmultisafepay&style=for-the-badge)](https://pepy.tech/project/multisafepay)


## About MultiSafepay

MultiSafepay is a Dutch payment services provider, which takes care of contracts, processing transactions, and
collecting payment for a range of local and international payment methods. Start selling online today and manage all
your transactions in one place!

## Installation

Here's how to use pip to put the MultiSafepay library into your Python.

```bash
pip install multisafepay
```

## Getting started

### Initialize the client

```python
from multisafepay.sdk import Sdk

multisafepay_sdk: Sdk = Sdk(api_key='<api_key>', is_production=True)
```

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