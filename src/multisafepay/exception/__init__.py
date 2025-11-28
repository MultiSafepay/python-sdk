"""Exception module for MultiSafepay SDK errors and exceptions."""

from multisafepay.exception.api import ApiException
from multisafepay.exception.api_unavailable import ApiUnavailableException
from multisafepay.exception.invalid_api_key import InvalidApiKeyException
from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.exception.invalid_total_amount import (
    InvalidTotalAmountException,
)
from multisafepay.exception.missing_plugin_version import (
    MissingPluginVersionException,
)

__all__ = [
    "ApiException",
    "ApiUnavailableException",
    "InvalidApiKeyException",
    "InvalidArgumentException",
    "InvalidTotalAmountException",
    "MissingPluginVersionException",
]
