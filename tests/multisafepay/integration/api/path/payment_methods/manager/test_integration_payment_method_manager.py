# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from unittest.mock import MagicMock

from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.payment_methods.payment_method_manager import (
    PaymentMethodManager,
)
from multisafepay.api.paths.payment_methods.response.components.allowed_amount import (
    AllowedAmount,
)
from multisafepay.api.paths.payment_methods.response.components.app import App
from multisafepay.api.paths.payment_methods.response.components.apps import (
    Apps,
)
from multisafepay.api.paths.payment_methods.response.components.brand import (
    Brand,
)
from multisafepay.api.paths.payment_methods.response.components.icon_urls import (
    IconUrls,
)
from multisafepay.api.paths.payment_methods.response.components.qr import Qr
from multisafepay.api.paths.payment_methods.response.components.tokenization import (
    Tokenization,
)
from multisafepay.api.paths.payment_methods.response.components.tokenizations.models import (
    Models,
)
from multisafepay.api.paths.payment_methods.response.payment_method import (
    PaymentMethod,
)


def test_payment_method_instance_correctly():
    """
    Test the get_payment_methods method of PaymentMethodManager with a valid response.

    This test mocks the client to return a valid ApiResponse and verifies
    that the get_payment_methods method returns a CustomApiResponse with the expected
    PaymentMethod data.

    """
    client = MagicMock()
    client.create_get_request.return_value = ApiResponse(
        headers={},
        status_code=200,
        body={
            "data": [
                {
                    "additional_data": {},
                    "allowed_amount": {"max": None, "min": 0},
                    "allowed_countries": [],
                    "allowed_currencies": ["CAD", "EUR", "GBP", "JPY", "USD"],
                    "apps": {
                        "fastcheckout": {
                            "is_enabled": True,
                            "qr": {"supported": False},
                        },
                        "payment_components": {
                            "has_fields": True,
                            "is_enabled": True,
                            "qr": {"supported": False},
                        },
                    },
                    "brands": [
                        {
                            "allowed_countries": ["IT"],
                            "icon_urls": {
                                "large": "https://testmedia.multisafepay.com/img/methods/3x/postepay.png",
                                "medium": "https://testmedia.multisafepay.com/img/methods/2x/postepay.png",
                                "vector": "https://testmedia.multisafepay.com/img/methods/svg/postepay.svg",
                            },
                            "id": "POSTEPAY",
                            "name": "PostePay",
                        },
                    ],
                    "description": "description x",
                    "icon_urls": {
                        "large": "https://testmedia.multisafepay.com/img/methods/3x/master.png",
                        "medium": "https://testmedia.multisafepay.com/img/methods/2x/master.png",
                        "vector": "https://testmedia.multisafepay.com/img/methods/svg/master.svg",
                    },
                    "id": "MASTERCARD",
                    "label": None,
                    "name": "MasterCard",
                    "preferred_countries": [],
                    "required_customer_data": [],
                    "shopping_cart_required": False,
                    "tokenization": {
                        "is_enabled": True,
                        "models": {
                            "cardonfile": True,
                            "subscription": True,
                            "unscheduled": True,
                        },
                    },
                    "type": "payment-method",
                },
            ],
            "success": True,
        },
    )
    manager = PaymentMethodManager(client)
    response = manager.get_payment_methods()
    assert isinstance(response, CustomApiResponse)
    assert isinstance(response.get_data(), list)
    assert response.get_data() == [
        PaymentMethod(
            additional_data={},
            allowed_amount=AllowedAmount(min=0, max=None),
            allowed_countries=[],
            allowed_currencies=["CAD", "EUR", "GBP", "JPY", "USD"],
            apps=Apps(
                fastcheckout=App(is_enabled=True, qr=Qr(supported=False)),
                payment_components=App(
                    has_fields=True,
                    is_enabled=True,
                    qr=Qr(supported=False),
                ),
            ),
            brands=[
                Brand(
                    allowed_countries=["IT"],
                    icon_urls=IconUrls(
                        large="https://testmedia.multisafepay.com/img/methods/3x/postepay.png",
                        medium="https://testmedia.multisafepay.com/img/methods/2x/postepay.png",
                        vector="https://testmedia.multisafepay.com/img/methods/svg/postepay.svg",
                    ),
                    id="POSTEPAY",
                    name="PostePay",
                ),
            ],
            description="description x",
            icon_urls=IconUrls(
                large="https://testmedia.multisafepay.com/img/methods/3x/master.png",
                medium="https://testmedia.multisafepay.com/img/methods/2x/master.png",
                vector="https://testmedia.multisafepay.com/img/methods/svg/master.svg",
            ),
            id="MASTERCARD",
            label=None,
            name="MasterCard",
            preferred_countries=[],
            required_customer_data=[],
            shopping_cart_required=False,
            tokenization=Tokenization(
                is_enabled=True,
                models=Models(
                    cardonfile=True,
                    subscription=True,
                    unscheduled=True,
                ),
            ),
            type="payment-method",
        ),
    ]
