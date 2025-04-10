# Copyright (c) MultiSafepay, Inc. All rights reserved.
# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.paths.orders.response.components.order_adjustment import (
    OrderAdjustment,
)
from multisafepay.api.paths.orders.response.components.payment_details import (
    PaymentDetails,
)
from multisafepay.api.paths.orders.response.order_response import Order
from multisafepay.api.shared.cart.cart_item import CartItem
from multisafepay.api.shared.cart.shopping_cart import ShoppingCart
from multisafepay.api.shared.checkout.checkout_options import CheckoutOptions
from multisafepay.api.shared.checkout.default_tax_rate import DefaultTaxRate
from multisafepay.api.shared.checkout.tax_rate import TaxRate
from multisafepay.api.shared.checkout.tax_rule import TaxRule
from multisafepay.api.shared.costs import Costs
from multisafepay.api.shared.customer import Customer
from multisafepay.api.shared.payment_method import PaymentMethod
from multisafepay.value_object.weight import Weight


def test_afterpay_response():
    data = {
        "amount": 37485,
        "amount_refunded": 0,
        "checkout_options": {
            "alternate": [
                {
                    "name": "BTW21",
                    "rules": [{"country": "", "rate": 0.21}],
                    "standalone": True,
                },
                {
                    "name": "BTW9",
                    "rules": [{"country": "", "rate": 0.09}],
                    "standalone": True,
                },
                {
                    "name": "BTW6",
                    "rules": [{"country": "", "rate": 0.06}],
                    "standalone": True,
                },
                {
                    "name": "BTW0",
                    "rules": [{"country": "", "rate": 0}],
                    "standalone": True,
                },
                {
                    "name": "none",
                    "rules": [{"country": "", "rate": 0}],
                    "standalone": "",
                },
                {
                    "name": "FEE",
                    "rules": [{"country": "", "rate": 0}],
                    "standalone": "",
                },
            ],
            "default": {"rate": 0.21, "shipping_taxed": True},
        },
        "costs": [
            {
                "amount": 3.75,
                "description": "1 % For AfterPay Transactions",
                "transaction_id": 11975632,
                "type": "SYSTEM",
            },
            {
                "amount": 1,
                "description": "1 For AfterPay Transactions",
                "transaction_id": 11975633,
                "type": "SYSTEM",
            },
        ],
        "created": "2025-03-12T13:25:28",
        "currency": "EUR",
        "custom_info": {"custom_1": None, "custom_2": None, "custom_3": None},
        "customer": {
            "address1": "Hogehilweg",
            "address2": None,
            "city": "Amsterdam",
            "company_name": None,
            "country": "NL",
            "country_name": "Netherlands",
            "email": "example@multisafepay.com",
            "first_name": "Test",
            "house_number": "8",
            "last_name": "Rejected",
            "locale": "nl_NL",
            "phone1": "0612345678",
            "phone2": None,
            "state": None,
            "zip_code": "1101CC",
        },
        "description": "Test Order Description",
        "fastcheckout": "NO",
        "financial_status": "uncleared",
        "items": '<table border="0" cellpadding="5" width="100%">\n<tr>\n<th width="10%"><font size="2" face="Verdana">Aantal </font></th>\n<th align="left"></th>\n<th align="left"><font size="2" face="Verdana">Details </font></th>\n<th width="19%" align="right"><font size="2" face="Verdana">Prijs </font></th>\n</tr>\n<tr>\n<td align="center"><font size="2" face="Verdana">3</font></td>\n<td width="6%"></td>\n<td width="65%"><font size="2" face="Verdana">Geometric Candle Holders</font></td>\n<td align="right">&euro;<font size="2" face="Verdana">90.00</font>\n</td>\n</tr>\n<tr>\n<td align="center"><font size="2" face="Verdana">1</font></td>\n<td width="6%"></td>\n<td width="65%"><font size="2" face="Verdana">Nice apple</font></td>\n<td align="right">&euro;<font size="2" face="Verdana">35.00</font>\n</td>\n</tr>\n<tr>\n<td align="center"><font size="2" face="Verdana">1</font></td>\n<td width="6%"></td>\n<td width="65%"><font size="2" face="Verdana">Flat Rate - Fixed</font></td>\n<td align="right">&euro;<font size="2" face="Verdana">10.00</font>\n</td>\n</tr>\n<tr bgcolor="#E9F1F7">\n<td colspan="3" align="right"><font size="2" face="Verdana">BTW:</font></td>\n<td align="right">&euro;<font size="2" face="Verdana">59.85</font>\n</td>\n</tr>\n<tr bgcolor="#E9F1F7">\n<td colspan="3" align="right"><font size="2" face="Verdana">Totaal:</font></td>\n<td align="right">&euro;<font size="2" face="Verdana">374.85</font>\n</td>\n</tr>\n</table>\n',
        "modified": "2025-03-12T13:25:28",
        "order_adjustment": {"total_adjustment": 59.85, "total_tax": 59.85},
        "order_id": "apitool_4325026",
        "order_total": 374.85,
        "payment_details": {
            "account_holder_name": None,
            "account_id": "1970-07-10",
            "collecting_flow": None,
            "external_transaction_id": "c7cef390-52d7-46b7-99e4-054e617bae2e",
            "recurring_flow": None,
            "recurring_id": None,
            "recurring_model": None,
            "type": "AFTERPAY",
        },
        "payment_methods": [
            {
                "account_id": "1970-07-10",
                "amount": 37485,
                "currency": "EUR",
                "description": "Test Order Description",
                "external_transaction_id": "c7cef390-52d7-46b7-99e4-054e617bae2e",
                "payment_description": "Riverty",
                "status": "uncleared",
                "type": "AFTERPAY",
            },
        ],
        "reason": None,
        "reason_code": None,
        "related_transactions": None,
        "shopping_cart": {
            "items": [
                {
                    "cashback": "",
                    "currency": "EUR",
                    "description": "",
                    "image": "",
                    "merchant_item_id": "1111",
                    "name": "Geometric Candle Holders",
                    "options": [],
                    "product_url": "",
                    "quantity": 3,
                    "tax_table_selector": "BTW21",
                    "unit_price": 90,
                    "weight": {"unit": "KG", "value": "12"},
                },
                {
                    "cashback": "",
                    "currency": "EUR",
                    "description": "",
                    "image": "",
                    "merchant_item_id": "666666",
                    "name": "Nice apple",
                    "options": [],
                    "product_url": "",
                    "quantity": 1,
                    "tax_table_selector": "BTW9",
                    "unit_price": 35,
                    "weight": {"unit": "KG", "value": "20"},
                },
                {
                    "cashback": "",
                    "currency": "EUR",
                    "description": "Shipping",
                    "image": "",
                    "merchant_item_id": "msp-shipping",
                    "name": "Flat Rate - Fixed",
                    "options": [],
                    "product_url": "",
                    "quantity": 1,
                    "tax_table_selector": "none",
                    "unit_price": 10,
                    "weight": {"unit": "KG", "value": "100"},
                },
            ],
        },
        "status": "completed",
        "transaction_id": 1741782328102572,
        "var1": None,
        "var2": None,
        "var3": None,
        "payment_url": "https://example.com/notification?type=redirect&transactionid=apitool_4325026",
        "cancel_url": "https://example.com/notification?type=cancel&transactionid=apitool_4325026",
    }
    order_from_dict = Order.from_dict(data)
    order = Order(
        order_id="apitool_4325026",
        amount_refunded=0,
        transaction_id=1741782328102572,
        status="completed",
        financial_status="uncleared",
        created="2025-03-12T13:25:28",
        modified="2025-03-12T13:25:28",
        order_total=374.85,
        amount=37485,
        currency="EUR",
        description="Test Order Description",
        fastcheckout="NO",
        custom_info={"custom_1": None, "custom_2": None, "custom_3": None},
        var1=None,
        var2=None,
        var3=None,
        reason=None,
        reason_code=None,
        related_transactions=None,
        customer=Customer(
            first_name="Test",
            last_name="Rejected",
            email="example@multisafepay.com",
            address1="Hogehilweg",
            address2=None,
            house_number="8",
            zip_code="1101CC",
            city="Amsterdam",
            state=None,
            country="NL",
            country_name="Netherlands",
            phone1="0612345678",
            phone2=None,
            company_name=None,
            locale="nl_NL",
        ),
        payment_details=PaymentDetails(
            account_id="1970-07-10",
            external_transaction_id="c7cef390-52d7-46b7-99e4-054e617bae2e",
            type="AFTERPAY",
            collecting_flow=None,
            recurring_flow=None,
            recurring_id=None,
            recurring_model=None,
            account_holder_name=None,
        ),
        payment_methods=[
            PaymentMethod(
                type="AFTERPAY",
                account_id="1970-07-10",
                amount=37485,
                currency="EUR",
                description="Test Order Description",
                external_transaction_id="c7cef390-52d7-46b7-99e4-054e617bae2e",
                payment_description="Riverty",
                status="uncleared",
            ),
        ],
        costs=[
            Costs(
                amount=3.75,
                description="1 % For AfterPay Transactions",
                transaction_id=11975632,
                type="SYSTEM",
            ),
            Costs(
                amount=1,
                description="1 For AfterPay Transactions",
                transaction_id=11975633,
                type="SYSTEM",
            ),
        ],
        order_adjustment=OrderAdjustment(
            total_adjustment=59.85,
            total_tax=59.85,
        ),
        checkout_options=CheckoutOptions(
            alternate=[
                TaxRule(
                    name="BTW21",
                    rules=[TaxRate(rate=0.21, country="")],
                    standalone=True,
                ),
                TaxRule(
                    name="BTW9",
                    rules=[TaxRate(rate=0.09, country="")],
                    standalone=True,
                ),
                TaxRule(
                    name="BTW6",
                    rules=[TaxRate(rate=0.06, country="")],
                    standalone=True,
                ),
                TaxRule(
                    name="BTW0",
                    rules=[TaxRate(rate=0, country="")],
                    standalone=True,
                ),
                TaxRule(
                    name="none",
                    rules=[TaxRate(rate=0, country="")],
                    standalone="",
                ),
                TaxRule(
                    name="FEE",
                    rules=[TaxRate(rate=0, country="")],
                    standalone="",
                ),
            ],
            default=DefaultTaxRate(rate=0.21, shipping_taxed=True),
        ),
        shopping_cart=ShoppingCart(
            items=[
                CartItem(
                    name="Geometric Candle Holders",
                    description="",
                    unit_price=90,
                    quantity=3,
                    merchant_item_id="1111",
                    tax_table_selector="BTW21",
                    weight=Weight(unit="KG", value="12"),
                    currency="EUR",
                    image="",
                    product_url="",
                    options=[],
                    cashback="",
                ),
                CartItem(
                    name="Nice apple",
                    description="",
                    unit_price=35,
                    quantity=1,
                    merchant_item_id="666666",
                    tax_table_selector="BTW9",
                    weight=Weight(unit="KG", value="20"),
                    currency="EUR",
                    image="",
                    product_url="",
                    options=[],
                    cashback="",
                ),
                CartItem(
                    name="Flat Rate - Fixed",
                    description="Shipping",
                    unit_price=10,
                    quantity=1,
                    merchant_item_id="msp-shipping",
                    tax_table_selector="none",
                    weight=Weight(unit="KG", value="100"),
                    currency="EUR",
                    image="",
                    product_url="",
                    options=[],
                    cashback="",
                ),
            ],
        ),
        items='<table border="0" cellpadding="5" width="100%">\n<tr>\n<th width="10%"><font size="2" face="Verdana">Aantal </font></th>\n<th align="left"></th>\n<th align="left"><font size="2" face="Verdana">Details </font></th>\n<th width="19%" align="right"><font size="2" face="Verdana">Prijs </font></th>\n</tr>\n<tr>\n<td align="center"><font size="2" face="Verdana">3</font></td>\n<td width="6%"></td>\n<td width="65%"><font size="2" face="Verdana">Geometric Candle Holders</font></td>\n<td align="right">&euro;<font size="2" face="Verdana">90.00</font>\n</td>\n</tr>\n<tr>\n<td align="center"><font size="2" face="Verdana">1</font></td>\n<td width="6%"></td>\n<td width="65%"><font size="2" face="Verdana">Nice apple</font></td>\n<td align="right">&euro;<font size="2" face="Verdana">35.00</font>\n</td>\n</tr>\n<tr>\n<td align="center"><font size="2" face="Verdana">1</font></td>\n<td width="6%"></td>\n<td width="65%"><font size="2" face="Verdana">Flat Rate - Fixed</font></td>\n<td align="right">&euro;<font size="2" face="Verdana">10.00</font>\n</td>\n</tr>\n<tr bgcolor="#E9F1F7">\n<td colspan="3" align="right"><font size="2" face="Verdana">BTW:</font></td>\n<td align="right">&euro;<font size="2" face="Verdana">59.85</font>\n</td>\n</tr>\n<tr bgcolor="#E9F1F7">\n<td colspan="3" align="right"><font size="2" face="Verdana">Totaal:</font></td>\n<td align="right">&euro;<font size="2" face="Verdana">374.85</font>\n</td>\n</tr>\n</table>\n',
        payment_url="https://example.com/notification?type=redirect&transactionid=apitool_4325026",
        cancel_url="https://example.com/notification?type=cancel&transactionid=apitool_4325026",
    )
    assert order == order_from_dict
