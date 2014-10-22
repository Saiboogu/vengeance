#!/usr/bin/env python
"""

Vengeance Mondo
===============

Mondo configuration data

## License

The MIT License (MIT)

Copyright (c) 2014 Sean Wallitsch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

# =============================================================================
# GLOBALS
# =============================================================================

# Site Details ================================================================

# This is the root page of the website
ROOT = 'mondotees.com'

# This is a list of pages to check for the drops. A single blank entry will
# cause only the root page to be checked.
DROP_PAGES = ['']

# Login Page ==================================================================

# This is the login page. If not using a login, set to False
LOGIN = 'mondotees.com/account/login'
LOGIN_USER = {
    'class': 'input',
    'attrib': 'id',
    'value': 'customer_email'
}
LOGIN_PASSWORD = {
    'class': 'input',
    'attrib': 'id',
    'value': 'customer_password'
}
LOGIN_BTN = {
    'class': 'input',
    'attrib': 'value',
    'value': 'Sign In'
}

# Items =======================================================================

# Do we need to evaluate the drops (True) or are we just looking for an "add to
# cart" button (False)?
DROP_EVALUATE = True

# We'll use this to describe the item we're looking for
ITEMS = {
    'class': 'div',
    'attrib': 'class',
    'value': 'drop-overlay',
}

# This describes the child element's tag to evaluate
EVAL = {
    'class': 'a',
    'attrib': 'class',
}

# These describe how to find the add-to-cart button, as a child of the above.
ADD_BTN = {
    'class': 'button',
    'attrib': 'class',
    'value': 'js-add-to-cart',
}

# Shopping Cart & Checkout ====================================================

# Page to go to to checkout. Make sure this URL doesn't contain a specific
# reference to your cart. If cart is accessible from the refresh page, put this
# as False
CART_PAGE = False

# Find the checkout button
CHECKOUT = {
    'class': 'div',
    'attrib': 'class',
    'value': 'hdr-cart-actions'
}

CHECKOUT_BTN = {
    'class': 'input',
    'attrib': 'name',
    'value': 'checkout'
}

# Billing & Shipping Forms ====================================================

# If your login information will autofill billing, leave this as False,
# else True
BILLING_FORM = False

BILLING_FORM_IDS = {
    'first': 'billing_address_first_name',
    'last': 'billing_address_last_name',
    'company': 'billing_address_company',
    'address1': 'billing_address_address1',
    'address2': 'billing_address_address2',
    'city': 'billing_address_city',
    'zip': 'billing_address_zip',
    'country': 'billing_address_country',
    'province': 'billing_address_province',
    'phone': 'billing_address_phone'
}

# If there is a "Use billing address as shipping address" (or vice versa)
# checkbox, and you want to either use or make sure not to use that checkbox,
# set that here.
BILLING_FOR_SHIPPING = True
BILLING_FOR_SHIPPING_BOX = {
    'class': 'input',
    'attrib': 'id',
    'value': 'shipping-toggle'
}

SHIPPING_FORM = False

SHIPPING_FORM_IDS = {
    'first': 'shipping_address_first_name',
    'last': 'shipping_address_last_name',
    'company': 'shipping_address_company',
    'address1': 'shipping_address_address1',
    'address2': 'shipping_address_address2',
    'city': 'shipping_address_city',
    'zip': 'shipping_address_zip',
    'country': 'shipping_address_country',
    'province': 'shipping_address_province',
    'phone': 'shipping_address_phone'
}

# Do you want to change the default shipping option?
SHIPPING_SELECTION = False
SHIPPING_SELECTION_BOX = {
    'class': 'select',
    'attrib': 'id',
    'value': 'shipping-rates'
}

# Credit Card Information =====================================================

# If you need to navigate to a different page for credit card information,
# set that here. Else, False
CC_PAGE_BUTTON = {
    'class': 'input',
    'attrib': 'id',
    'value': 'commit-button'
}

CREDIT_FORMS = {
    'first': 'credit_card_first_name',
    'last': 'credit_card_last_name',
    'ccn': 'credit_card_number',
    'exp_mo': 'credit_card_month',
    'exp_yr': 'credit_card_year',
    'ccv': 'credit_card_verification_value'
}

# Process Order ===============================================================

# Button you click to complete checkout
PROCESS_ORDER = {
    'class': 'input',
    'attrib': 'id',
    'value': 'complete-purchase'
}