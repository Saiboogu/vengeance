#!/usr/bin/env python
"""

Browser
=======

Contains a Selenium implementation of Vengeance. Slower, but more reliable.
This should be considered the base result, with other results being
more unstable.

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

# Standard Imports
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import httplib
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# =============================================================================
# GLOBALS
# =============================================================================

__all__ = [
    'SeleniumBrowser'
]

# httplib.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

# =============================================================================
# CLASSES
# =============================================================================


class RequestsBrowser(object):
    """Requests based implementation"""
    def __init__(self, config):
        self._config = config
        self._session = requests.Session()

        self.drop_time = None
        self.start_time = None
        self.finish_time = None

        self._setup_session()

    # Properties ==============================================================

    @property
    def cookies(self):
        return self.session.cookies

    @property
    def config(self):
        return self._config

    @property
    def session(self):
        return self._session

    # Private Methods =========================================================

    def _setup_session(self):
        """Sets up the session and fetches base page once"""
        self.session.headers = {
            'Host': self.config.base_url,
            'User-Agent': 'Mozilla/5.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': self.build_url(),
            'Connection': 'keep-alive',
            'vary': 'Accept-Encoding,Cookie'
        }
        self.session.get(self.build_url())
        self.session.get(
            self.build_url(
                'assets/templates/mondo/includes/jquery.jqzoom-1.0.1.js'
            )
        )
        #self.session.get(
        #    self.build_url(
        #        'view_category.asp?cat=12'
        #    )
        #)

        for cookie in self.cookies:
            print cookie

    def add_to_cart(self, item_id):
        """Add an item to a cart using a POST"""
        self.session.headers['Referer'] = 'http://www.mondotees.com/Spring-Rocker_p_1509.html'
        data = {
            'item_id': '1509',
            'category_id': '12',
            'qty-0': '1'
        }
        payload = (
            'Content-Type: multipart/form-data; boundary=---------------------------98516585583522581473857174\r\nContent-Length: 395\r\n\r\n-----------------------------98516585583522581473857174\r\nContent-Disposition: form-data; name="item_id"\r\n\r\n1509\r\n-----------------------------98516585583522581473857174\r\nContent-Disposition: form-data; name="category_id"\r\n\r\n12\r\n-----------------------------98516585583522581473857174\r\nContent-Disposition: form-data; name="qty-0"\r\n\r\n1\r\n-----------------------------98516585583522581473857174--\r\n'
        )
        post = self.session.post(
            self.build_url('add_cart.asp'),
            data=payload,
        )
        print "First in post history:", post.history[0].url
        print "Final post url:", post.url
        #print post.text

    def build_url(self, relative=''):
        """Builds a url with our base"""
        url = 'http://{base}/{rel}'.format(
            base=self.config.base_url,
            rel=relative,
        )
        return url

    def run(self):
        self.add_to_cart(1509)
        #self.view_cart()

    def view_cart(self):
        """Goes to the cart page"""
        cart_response = self.session.get(self.build_url('view_cart.asp'))
        cart = BeautifulSoup(cart_response.text)
        items = cart.find_all("item")
        for item in items:
            print item


class SeleniumBrowser(object):
    """Reference implementation of the Buyer"""
    def __init__(self, config):
        self._profile = self.disable_images()
        self._config = config
        self._driver = webdriver.Firefox(self._profile)

        self.drop_time = None
        self.start_time = None
        self.finish_time = None

    # Properties ==============================================================

    @property
    def config(self):
        return self._config

    @property
    def driver(self):
        return self._driver

    def build_url(self, relative=''):
        """Builds a url with our base"""
        url = 'http://{base}/{rel}'.format(
            base=self.config.base_url,
            rel=relative,
        )
        return url

    # Private Methods =========================================================

    def _fill_form_dict(self, form_dict):
        """Fills an entire form using a dictionary to dictate name & values"""
        for form in form_dict:
            self._fill_form_item(form, form_dict[form])

    # =========================================================================

    def _fill_form_item(self, name, value):
        """Fills a single form item"""
        form = self.driver.find_element_by_name(name)
        form.send_keys(value)

    # =========================================================================

    def _get_links(self):
        """Fetches all links from the current page and returns as list"""
        return self.driver.find_elements_by_tag_name('a')

    # =========================================================================

    def _out_of_stock_handler(self, click=True):
        """Acknowledges out of stock warnings and skips past them"""
        oos = True
        found_oos = False
        while oos:
            try:
                elem = self.driver.find_element_by_xpath(
                    "//input[@value='Click here to continue']"
                )
            except NoSuchElementException:
                # No items removed
                oos = False
            else:
                print "An item was removed from the cart"
                found_oos = True
                if click:
                    elem.click()
                else:
                    # When we don't need to click, we're only
                    # checking on the status of a single item.
                    # The function calling this handler will
                    # handle moving on to the next page.
                    break
        return found_oos

    # =========================================================================

    def _xpath_select_dict(self, select_dict):
        """Does multiple section boxes based on incoming selection dict"""
        for select in select_dict:
            self._xpath_select_item(select, select_dict[select])

    # =========================================================================

    def _xpath_select_item(self, name, value):
        """Selects a specified text element from dropdown"""
        self.driver.find_element_by_xpath(
            "//select[@name='{form_name}']"
            "/option[text()='{form_value}']".format(
                form_name=name,
                form_value=value
            )
        ).click()

    # Public Methods ==========================================================

    def add_link_to_cart(self, link):
        """Adds the product on page link to the cart"""
        self.driver.get(link)
        try:
            self.driver.find_element_by_name('Add').click()
        except NoSuchElementException:
            print "Product on page {link} is sold out.".format(
                link=link
            )
        else:
            print "Added product found on {link} to cart.".format(
                link=link
            )
            self.driver.implicitly_wait(0.1)
            if self._out_of_stock_handler(click=False):
                print "Product on {link} removed from cart.".format(
                    link=link
                )

    # =========================================================================

    def check_out(self, dry_run=True):
        """Hits the final checkout button"""
        check_out_btn = self.driver.find_element_by_name('divCheckout')
        print "Final checkout page. divCheckout selected for clicking."
        if not dry_run:
            print "Live. Purchasing"
            check_out_btn.click()

            # See if items have been removed from our cart
            self._out_of_stock_handler()

            print "Purchase complete."
        else:
            print "dry_run is engaged. No purchase made."

    # =========================================================================

    @staticmethod
    def disable_images():
        """Disables css, images and flash inside browser"""
        ## get the Firefox profile object
        firefox_profile = FirefoxProfile()
        ## Disable CSS
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        ## Disable images
        firefox_profile.set_preference('permissions.default.image', 2)
        ## Disable Flash
        firefox_profile.set_preference(
            'dom.ipc.plugins.enabled.libflashplayer.so',
            'false'
        )

        return firefox_profile

    # =========================================================================

    def fill_billing(self):
        """Fills out billing page"""
        # Use shipping for billing
        self.driver.find_element_by_name('check1').click()

        # See if items have been removed from our cart
        self._out_of_stock_handler()

        # Credit Card Number and CVV2
        self._fill_form_dict(
            {
                'ff11_ocardno': self.config.consumer['CCN'],
                'ff11_ocardcvv2': self.config.consumer['CVV']
            }
        )

        # Exp Month, Year and Card Type
        self._xpath_select_dict(
            {
                'ff11_ocardexpiresmonth': self.config.consumer['ExpMo'],
                'ff11_ocardexpiresyear': self.config.consumer['ExpYr'],
                'ff11_ocardtype': self.config.consumer['Type'],
            }
        )

    # =========================================================================

    def fill_shipping(self):
        """Fills out shipping page"""

        # See if items have been removed from our cart
        self._out_of_stock_handler()

        shipping_values = {
            'email': self.config.consumer['Email'],
            'shipping_firstname': self.config.consumer['FirstName'],
            'shipping_lastname': self.config.consumer['LastName'],
            'shipping_phone': self.config.consumer['Phone'],
            'shipping_address': self.config.consumer['Address'],
            'shipping_city': self.config.consumer['City'],
            'shipping_zip': self.config.consumer['Zip'],
        }

        self._fill_form_dict(shipping_values)

        # State and Country
        self._xpath_select_dict(
            {
                'shipping_country': self.config.consumer['Country'],
                'shipping_state': self.config.consumer['State']
            }
        )

    # =========================================================================

    def filter_element_links(self, links, elements=True):
        """Filters a list down to a set of only interesting links"""
        good_links = []
        for product in self.config.targets:
            for link in links:
                if elements:
                    href = link.get_attribute('href').lower()
                else:
                    href = link
                p_page = href.split('/')[-1]
                if product in p_page:
                    good_links.append(href)
        # Filter out duplicates
        good_links = list(set(good_links))
        return good_links

    # =========================================================================

    def run(self, drops=None):
        """Main runner function"""
        self.start_time = datetime.utcnow()
        if not self.drop_time:
            self.drop_time = self.start_time
        print "Delay of:", datetime.utcnow() - self.drop_time

        if not drops:
            # If we weren't handed a list of links, we gotta find them.
            print "Heading to", self.build_url('view_category.asp?cat=12')
            self.driver.get(self.build_url('view_category.asp?cat=12'))

            # Find the link we want
            links = self._get_links()
            elements = True
        else:
            links = drops
            elements = False

        good_links = self.filter_element_links(links, elements)

        # Add to our cart
        for link in good_links:
            self.add_link_to_cart(link)

        # Head to checkout
        self.driver.get(self.build_url('checkout.asp?step=1'))
        print "On Shipping Page"

        # Fill Shipping Page
        self.fill_shipping()

        # Leave Shipping Page
        self.driver.find_element_by_name("Add22").click()
        print "On Billing Page"

        # Fill Billing Page
        self.fill_billing()

        # Checkout
        self.check_out(dry_run=True)

        self.finish_time = datetime.utcnow()
        print "Total time:", self.finish_time - self.drop_time
        print "Running time:", self.finish_time - self.start_time
