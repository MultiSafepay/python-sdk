"""API path endpoints for MultiSafepay SDK operations."""

from multisafepay.api.paths.auth.auth_manager import AuthManager
from multisafepay.api.paths.capture.capture_manager import CaptureManager
from multisafepay.api.paths.categories.category_manager import (
    CategoryManager,
)
from multisafepay.api.paths.events.event_manager import EventManager
from multisafepay.api.paths.gateways.gateway_manager import GatewayManager
from multisafepay.api.paths.issuers.issuer_manager import IssuerManager
from multisafepay.api.paths.me.me_manager import MeManager
from multisafepay.api.paths.orders.order_manager import OrderManager
from multisafepay.api.paths.payment_methods.payment_method_manager import (
    PaymentMethodManager,
)
from multisafepay.api.paths.pos.pos_manager import PosManager
from multisafepay.api.paths.recurring.recurring_manager import (
    RecurringManager,
)
from multisafepay.api.paths.terminal_groups.terminal_group_manager import (
    TerminalGroupManager,
)
from multisafepay.api.paths.terminals.terminal_manager import (
    TerminalManager,
)
from multisafepay.api.paths.transactions.transaction_manager import (
    TransactionManager,
)

__all__ = [
    "AuthManager",
    "CaptureManager",
    "CategoryManager",
    "EventManager",
    "GatewayManager",
    "IssuerManager",
    "MeManager",
    "OrderManager",
    "PaymentMethodManager",
    "PosManager",
    "RecurringManager",
    "TerminalGroupManager",
    "TerminalManager",
    "TransactionManager",
]
