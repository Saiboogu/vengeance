#!/usr/bin/env python
"""

Vengeance Sites
===============

Per Site Configuration Files

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
# IMPORTS
# =============================================================================

from importlib import import_module

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "SiteConfig",
]

# =============================================================================
# GLOBALS
# =============================================================================

# =============================================================================
# CLASSES
# =============================================================================

class SiteConfig(object):
    """Controls site specific configuration options"""

    def __init__(self, site_name):
        """Copies the site configuration data into the site config object"""
        self._site = import_module('.' + site_name, 'sites')

        self._read_site_details()

        self._read_login()

        self._read_items()

        self._read_cart()

        self._read_consumer_info()

        self._read_credit_card()

    # Properties ==============================================================

    @property
    def billing_form(self):
        return self._billing_form_ids

    @property
    def cart_page(self):
        return self._cart_page

    @property
    def cc_forms(self):
        return self._cc_forms

    @property
    def cc_page_button(self):
        return self._cc_page_button

    @property
    def checkout(self):
        return self._checkout

    @property
    def checkout_button(self):
        return self._checkout_button

    @property
    def drop_add_button(self):
        return self._drop_add_button

    @property
    def drop_eval_item(self):
        return self._drop_eval_item

    @property
    def drop_eval_value(self):
        return self._drop_eval_value

    @property
    def drop_evaluate(self):
        return self._drop_evaluate

    @property
    def drops(self):
        return self._drops

    @property
    def login(self):
        return self._login

    @property
    def login_button(self):
        return self._login_button

    @property
    def login_password(self):
        return self._login_password

    @property
    def login_user(self):
        return self._login_user

    @property
    def override_shipping(self):
        return self._override_shipping

    @property
    def override_shipping_box(self):
        return self._override_shipping_box

    @property
    def process_order(self):
        return self._process_order

    @property
    def root(self):
        return self._root

    @property
    def shipping_form(self):
        return self._shipping_form_ids

    @property
    def site(self):
        return self._site

    @property
    def use_billing_form(self):
        return self._use_billing_form

    @property
    def use_billing_for_shipping(self):
        return self._use_billing_for_shipping

    @property
    def use_billing_for_shipping_box(self):
        return self._use_billing_for_shipping_box

    @property
    def use_shipping_form(self):
        return self._use_shipping_form

    # Private Methods =========================================================

    def _read_cart(self):
        """Reads and sets information about the shopping cart"""
        self._cart_page = self.site.CART_PAGE
        self._checkout = self.site.CHECKOUT
        self._checkout_button = self.site.CHECKOUT_BTN
        self._process_order = self.site.PROCESS_ORDER

    # =========================================================================

    def _read_consumer_info(self):
        """Reads and sets information about form fills for consumer info"""
        self._use_billing_form = self.site.BILLING_FORM
        self._billing_form_ids = self.site.BILLING_FORM_IDS

        self._use_billing_for_shipping = self.site.BILLING_FOR_SHIPPING
        self._use_billing_for_shipping_box = self.site.BILLING_FOR_SHIPPING_BOX

        self._use_shipping_form = self.site.SHIPPING_FORM
        self._shipping_form_ids = self.site.SHIPPING_FORM_IDS

        self._override_shipping = self.site.SHIPPING_SELECTION
        self._override_shipping_box = self.site.SHIPPING_SELECTION_BOX

    # =========================================================================

    def _read_credit_card(self):
        """Reads and sets credit card form information"""
        self._cc_page_button = self.site.CC_PAGE_BTN
        self._cc_forms = self.site.CREDIT_FORMS

    # =========================================================================

    def _read_items(self):
        """Reads and sets information about the items we're looking for"""
        self._drop_evaluate = self.site.DROP_EVALUATE
        self._drop_eval_item = self.site.ITEMS
        self._drop_eval_value = self.site.EVAL_VALUE
        self._drop_add_button = self.site.ADD_BTN

    # =========================================================================

    def _read_login(self):
        """Reads and sets login information"""
        self._login = self.site.LOGIN
        if self._login:
            self._login_user = self.site.LOGIN_USER
            self._login_password = self.site.LOGIN_PASSWORD
            self._login_button = self.site.LOGIN_BTN
        else:
            self._login_user = {}
            self._login_password = {}
            self._login_button = {}

    # =========================================================================

    def _read_site_details(self):
        """Reads and sets item drop configuration"""

        root = self.site.ROOT
        if root.startswith('http'):
            root = root.replace('http://', '')

        self._root = root
        self._drops = self.site.DROP_PAGES

    # Public Methods ==========================================================

    def debug(self):
        """Prints stored information"""
        print 'Root:', self.root
        print 'Drops:', self.drops
        print
        print 'Login:', self.login
        print 'Login User:', self.login_user
        print 'Login Password:', self.login_password
        print 'Login Button:', self.login_button
        print
        print 'Drop Evaluate:', self.drop_evaluate
        print 'Drop Eval Item:', self.drop_eval_item
        print 'Drop Eval Value:', self.drop_eval_value
        print 'Drop Add Button:', self.drop_add_button
        print
        print 'Cart Page:', self.cart_page
        print 'Checkout:', self.checkout
        print 'Checkout Button:', self.checkout_button
        print 'Process Order:', self.process_order
        print
        print 'Use Billing Info?:', self.use_billing_form
        print 'Billing Form:', self.billing_form
        print 'Use Billing For Shipping:', self.use_billing_for_shipping
        print 'Use Billing For Shipping Box:', self.use_billing_for_shipping_box
        print 'Use Shipping Info?:', self.use_shipping_form
        print 'Shipping Form:', self.shipping_form
        print 'Override Shipping:', self.override_shipping
        print 'Override Shipping Box:', self.override_shipping_box
        print
        print 'CC Page Button:', self.cc_page_button
        print 'CC Form:', self.cc_forms