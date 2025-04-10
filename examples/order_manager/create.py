import time
import os
from dotenv import load_dotenv
from multisafepay.value_object.weight import Weight
from multisafepay.api.shared.cart.cart_item import CartItem
from multisafepay.api.paths.orders.request.components.checkout_options import CheckoutOptions
from multisafepay.api.paths.orders.request.components.payment_options import PaymentOptions
from multisafepay.api.paths.orders.request.components.plugin import Plugin
from multisafepay.api.paths.orders.request.order_request import OrderRequest
from multisafepay.api.shared.cart.shopping_cart import ShoppingCart
from multisafepay.api.shared.customer import Customer
from multisafepay.sdk import Sdk
from multisafepay.value_object.amount import Amount
from multisafepay.value_object.country import Country
from multisafepay.value_object.currency import Currency
from multisafepay.api.shared.description import Description
from multisafepay.value_object.email_address import EmailAddress
from multisafepay.value_object.ip_address import IpAddress
from multisafepay.value_object.phone_number import PhoneNumber
from multisafepay.api.paths.orders.response.order_response import Order

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("API_KEY")

if __name__ == "__main__":
    # Initialize the MultiSafepay SDK with the API key and disable test mode
    multisafepay_sdk = Sdk(API_KEY, False)

    # Generate a unique order ID based on the current time
    order_id = f'{str(time.time())}'

    # Create an Amount object with the order amount
    amount = Amount(amount=37485)
    # Create a Currency object with the order currency
    currency = Currency(currency='EUR')
    # Create a Country object with the order country
    countryTmp = Country(code='NL')
    # Create a Description object with the order description
    description = Description(description='Order description')
    # Create an EmailAddress object with the customer's email
    email = EmailAddress(email_address='example@multisafepay.com')
    # Create a PhoneNumber object with the customer's phone number
    phone_number = PhoneNumber(phone_number='0208500500')
    # Create an IpAddress object with the customer's IP address
    ip_address = IpAddress(ip_address='192.0.0.1')

    # Create a Customer object and add the customer's details
    customer = (Customer()
                .add_first_name('John')
                .add_last_name('Doe')
                .add_address1('Kraanspoor')
                .add_address2('39')
                .add_zip_code('1033SC')
                .add_city('Amsterdam')
                .add_country(countryTmp)
                .add_email(email)
                .add_house_number('39')
                .add_locale('en_US')
                .add_phone(phone_number)
                .add_ip_address(ip_address)
                .add_forwarded_ip(ip_address)
                .add_referrer('https://www.example.com')
                .add_user_agent('Mozilla/5.0')
                )

    # Create a PluginDetails object and add the plugin details
    plugin = (Plugin()
              .add_plugin_version('1.0.0')
              .add_shop("CMS - Framework name")
              .add_shop_version('1.0.0')
              .add_partner('MultiSafepay')
              .add_shop_root_url('https://www.multisafepay.com'))

    # Create a PaymentOptions object and add the payment options
    payment_options = (PaymentOptions()
                       .add_notification_url('https://multisafepay.com/notification_url')
                       .add_redirect_url('https://multisafepay.com/redirect_url')
                       .add_cancel_url('https://multisafepay.com/cancel_url')
                       .add_close_window(True))

    # Create cart items
    cart_items = [
        CartItem()
        .add_name('Geometric Candle Holders')
        .add_description('Geometric Candle Holders description')
        .add_unit_price(90)
        .add_quantity(3)
        .add_merchant_item_id('1111')
        .add_tax_rate_percentage(21)
        .add_weight(Weight(value=1.0, unit='kg')),

        CartItem()
        .add_name('Nice apple')
        .add_description('Nice apple description')
        .add_unit_price(35)
        .add_quantity(1)
        .add_merchant_item_id('666666')
        .add_tax_rate_percentage(9)
        .add_weight(Weight(value=20, unit='kg')),

        CartItem()
        .add_name('Flat Rate - Fixed')
        .add_description('Shipping')
        .add_unit_price(10)
        .add_quantity(1)
        .add_merchant_item_id('msp-shipping')
        .add_tax_rate_percentage(0)
        .add_weight(Weight(value=0, unit='kg'))
    ]

    # Create shopping_cart
    shopping_cart = ShoppingCart().add_items(cart_items)

    # Create an OrderRequest object and add the order details
    order_request = (OrderRequest()
                     .add_type('direct')
                     .add_order_id(order_id)
                     .add_description(description)
                     .add_amount(amount)
                     .add_currency(currency)
                     .add_gateway('IDEAL')
                     .add_customer(customer)
                     .add_delivery(customer)
                     .add_plugin(plugin)
                     .add_payment_options(payment_options)
                     .add_shopping_cart(shopping_cart)
                     .add_checkout_options(CheckoutOptions.generate_from_shopping_cart(shopping_cart))
                     )

    # Get the order manager from the SDK
    order_manager = multisafepay_sdk.get_order_manager()
    # Create the order using the order manager
    create_response = order_manager.create(order_request)
    # Print the API response containing the order information
    # print(create_response)

    order: Order = create_response.get_data()

    print(order)
