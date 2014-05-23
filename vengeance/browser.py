#!/usr/bin/env python
"""

Browser
=======

Contains the various implementation of the browser fetchers that do the actual
buying of items.

Currently only includes a Selenium implementation of Vengeance. Slower, but
more reliable. This should be considered the base result, with other results
being more unstable.

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
from selenium.common.exceptions import NoSuchElementException
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
    """Reference implementation of the Buyer using Selenium

    Description
    ~~~~~~~~~~~

    Selenium launches an actual browser window, then controls that browser
    window. We'll search for elements, click buttons and fill out forms,
    all using an actual browser.

    This gives us maximum compatibility, but will also be the slowest
    implementation

    **Attributes:**

        config : (:class:`config.Config`)
            Config object that holds all the product and form information
            we need to buy something, such as shipping addresses and credit
            card information.

        driver : (:class:`webdriver.Driver`)
            The webbrowser implementation to use. This is by default firefox,
            and you'd have to modify the code to change it.

        finish_time : (:class:`datetime.DateTime`)
            DateTime object for when the final check out action is completed.

        start_time : (:class:`datetime.DateTime`)
            DateTime object for when the BuyerSelenium class begins it's work

        tweet_time : (:class:`datetime.DateTime`)
            DateTime object for when the kickoff tweet happened, this let's us
            calculate the total runtime of the Selenium browser alone, which
            accounts for the delay before the tweet was sent to us.

    **Public Methods:**

        add_link_to_cart()
            Goes to a product page, finds the `Add` button (if present) and
            adds product to cart. Will handle out of stock gracefully.

            Has a short wait after adding an item to the cart to give server
            time to handle the add.

        check_out()
            When activated on the final checkout page, clicks the checkout
            button. Has a parameter ``dry_run`` which, when False, will click
            the button for real.

        fill_billing()
            While on the billing page, fills out all billing information.

        fill_shipping()
            While on the shipping page (first page of checkout), fills out
            all shipping information.

        filter_links()
            Compares a list of links to our interested product list, and
            returns only links we're interested on adding to our cart.

        run()
            Main run function, calling this starts the buyer process into
            motion, logs the start and finish times. Parses the main
            item page for links, filters those links down to interested
            links, adds items to the cart, begins checkout process.

    """
    def __init__(self, config):
        """Initializes all instance variables for this buyer."""
        # Set our profile to turn off image loading, css and flash.
        self._profile = self._disable_images()

        # Config contains all the product and consumer information that we
        # need to buy and checkout.
        self._config = config

        # This initializes and opens our browser.
        self._driver = webdriver.Firefox(self._profile)

        self.tweet_time = None
        self.start_time = None
        self.finish_time = None

    # Properties ==============================================================

    @property
    def config(self):
        """Our Config instance from config.ini"""
        return self._config

    @property
    def driver(self):
        """Our webbrowser"""
        return self._driver

    # Private Methods =========================================================

    def _build_url(self, relative):
        """Builds a url with our base from config"""
        url = 'http://{base}/{rel}'.format(
            base=self.config.base_url,
            rel=relative,
        )
        return url

    # =========================================================================

    @staticmethod
    def _disable_images():
        """Disables css, images and flash inside browser"""
        # get the Firefox profile object
        firefox_profile = FirefoxProfile()
        # Disable CSS
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        # Disable images
        firefox_profile.set_preference('permissions.default.image', 2)
        # Disable Flash
        firefox_profile.set_preference(
            'dom.ipc.plugins.enabled.libflashplayer.so',
            'false'
        )

        return firefox_profile

    # =========================================================================

    def _fill_form_dict(self, form_dict):
        """Fills an entire form using a dictionary to dictate name & values"""
        for form in form_dict:
            self._fill_form_item(form, form_dict[form])

    # =========================================================================

    def _fill_form_item(self, name, value):
        """Fills a single form text field item"""
        form = self.driver.find_element_by_name(name)
        form.send_keys(value)

    # =========================================================================

    def _get_links(self):
        """Fetches all links from the current page and returns as list"""
        # We'll search for all 'a' elements
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

    def filter_links(self, links):
        """Filters a list down to a set of only interesting links"""
        good_links = []
        for product in self.config.targets:
            for link in links:
                href = link.get_attribute('href').lower()
                p_page = href.split('/')[-1]
                if product in p_page:
                    good_links.append(href)
        # Filter out duplicates
        good_links = list(set(good_links))
        return good_links

    # =========================================================================

    def run(self):
        """Main runner function"""
        self.start_time = datetime.utcnow()
        print "Delay of:", datetime.utcnow() - self.tweet_time
        print "Heading to", self._build_url('view_category.asp?cat=12')
        self.driver.get(self._build_url('view_category.asp?cat=12'))

        # Find the link we want
        links = self._get_links()
        good_links = self.filter_links(links)

        # Add to our cart
        for link in good_links:
            self.add_link_to_cart(link)

        # Head to checkout
        self.driver.get(self._build_url('checkout.asp?step=1'))
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
