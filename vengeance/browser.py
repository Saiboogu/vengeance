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
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# =============================================================================
# GLOBALS
# =============================================================================

__all__ = [
    'BuyerSelenium'
]

# =============================================================================
# CLASSES
# =============================================================================


class BuyerSelenium(object):
    """Reference implementation of the Buyer"""
    def __init__(self, config):
        self._profile = self.disable_images()
        self._config = config
        self._driver = webdriver.Firefox(self._profile)

        self.tweet_time = None
        self.start_time = None
        self.finish_time = None

    # Properties ==============================================================

    @property
    def config(self):
        return self._config

    @property
    def driver(self):
        return self._driver

    def build_url(self, relative):
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

    def check_out(self, dry_run=True):
        """Hits the final checkout button"""
        check_out_btn = self.driver.find_element_by_name('divCheckout')
        print "Final checkout page. divCheckout selected for clicking."
        if not dry_run:
            print "Live. Purchasing"
            check_out_btn.click()
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

    def run(self):
        """Main runner function"""
        self.start_time = datetime.utcnow()
        print "Delay of:", datetime.utcnow() - self.tweet_time
        print "Heading to", self.build_url('view_category.asp?cat=12')
        self.driver.get(self.build_url('view_category.asp?cat=12'))

        # Find the link we want
        links = self._get_links()
        for link in links:
            href = link.get_attribute('href').lower()
            if self.config.targets.keys()[0].lower() in href:
                print "Found link for", self.config.targets.keys()[0].lower()
                print href
                link.click()
                break

        # Add to our cart
        self.driver.find_element_by_name('Add').click()
        print "Added to Cart"

        self.driver.implicitly_wait(.1)
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
        print "Total time:", self.finish_time - self.tweet_time
        print "Running time:", self.finish_time - self.start_time
