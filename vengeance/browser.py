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
from selenium.common.exceptions import (
    NoSuchElementException, WebDriverException
)
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# =============================================================================
# GLOBALS
# =============================================================================

__all__ = [
    'SeleniumBrowser'
]

# =============================================================================
# CLASSES
# =============================================================================


class SeleniumBrowser(object):
    """Reference implementation of the Buyer"""
    def __init__(self, config, site_config):
        self._profile = self.disable_images()
        self._config = config
        self._site = site_config
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

    @property
    def site(self):
        return self._site

    # Private Methods =========================================================

    # =========================================================================

    def _find_element(self, element_dict, single=True, source=None):
        """Determines the best method to find an element, then returns it"""
        value = element_dict['value']
        tag = element_dict.get('attrib', None)

        if not source:
            source = self.driver

        if tag is 'id':
            found = source.find_elements_by_id(value)
        elif tag is 'name':
            found = source.find_elements_by_name(value)
        elif tag is 'class':
            found = source.find_elements_by_class_name(value)
        else:
            found = source.find_elements_by_xpath(
                "//{html_class}[@{tag}='{value}']".format(
                    html_class=element_dict['class'],
                    tag=tag,
                    value=element_dict['value']
                )
            )

        if single:
            try:
                return found[0]
            except IndexError:
                raise NoSuchElementException(
                    'Could not find any elements matching {elem}'.format(elem=element_dict)
                )
        else:
            return found



    def _find_parent(self, element, parent_tag):
        """Finds the parent of the element matching the parent_tag"""
        return element.find_element_by_xpath(
            './parent::{tag}'.format(tag=parent_tag)
        )

    # =========================================================================

    def _fill_form_dict(self, form_dict):
        """Fills an entire form using a dictionary to dictate name & values"""
        for form in form_dict:
            form_item = {
                'class': 'input',
                'attrib': 'id',
                'value': form
            }
            self._fill_form_item(form_item, form_dict[form])

    # =========================================================================

    def _fill_form_item(self, form_info, value):
        """Fills a single form item"""
        tries = 0

        while tries < 2:
            try:
                form = self._find_element(form_info)
            except NoSuchElementException:
                # Page is probably still loading.
                self.driver.implicitly_wait(1)
                tries += 1
            else:
                try:
                    # Clear if we can
                    form.clear()
                except WebDriverException:
                    # Happens on drop down forms
                    pass
                form.send_keys(value)
                return

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

    def add_to_cart(self, link):
        """Adds the product on page link to the cart"""
        if self.site.drop_add_from_root:
            if self.driver.current_url != self.build_url():
                self.driver.get(self.build_url())
            link_dict = dict(self.site.drop_eval_value)
            link_dict['value'] = link

            parent = self._find_parent(
                self._find_element(link_dict),
                self.site.drop_eval_item['class']
            )

            buttons = self._find_element(
                self.site.drop_add_button,
                single=False,
                source=parent
            )

            if len(buttons) != 1:
                raise Exception('Found {0} buttons instead of 1!'.format(
                    len(buttons)
                ))
            else:
                buttons[0].click()
        else:
            # This involves going to each found item, adding it to the cart
            # manually. Not set up yet.
            pass

    # =========================================================================

    def build_url(self, relative=''):
        """Builds a url with our base"""
        if relative.startswith(self.site.root):
            relative = relative[len(self.site.root):]
        if relative.startswith('/'):
            relative = relative[1:]
        url = 'http://{base}/{rel}'.format(
            base=self.site.root,
            rel=relative,
        )
        return url

    # =========================================================================

    def check_out(self):
        """Initiates the check out process"""
        if self.site.cart_page:
            self.driver.get(self.site.cart_page)

        # Wait to make sure site got all of our additions to cart
        #self.driver.implicitly_wait(1)

        # We'll try to checkout twice.
        tries = 0
        while tries < 2:
            try:
                button = self._find_element(self.site.checkout_button)
            except (IndexError, NoSuchElementException):
                # Page is still loading.
                tries += 1
                self.driver.implicitly_wait(1)
            else:
                #self.driver.implicitly_wait(1)
                button.click()
                return True

    # =========================================================================

    def check_out_2(self):
        """Second page of check out, if any"""
        checkout_button = self._find_element(self.site.checkout_2)
        checkout_button.click()

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
        pass

    # =========================================================================

    def fill_cc(self):
        """Fills out credit card information"""
        form_dict = {
            self.site.cc_forms[key]: self.config.consumer[key]
            for key in self.site.cc_forms
        }
        self.driver.implicitly_wait(1)
        self._fill_form_dict(form_dict)

    # =========================================================================

    def fill_shipping(self):
        """Fills out shipping page"""
        pass

    # =========================================================================

    def filter_links(self, links):
        """Filters a list down to a set of only interesting links"""
        good_links = []
        for product in self.config.targets:
            for link in links:
                p_page = link.split('/')[-1]
                if product in p_page:
                    good_links.append(link)

        # Filter out duplicates
        good_links = list(set(good_links))

        # Remove excluded products
        for link in good_links[:]:
            for exclude in self.config.exclusions:
                if exclude in link:
                    good_links.remove(link)

        return good_links

    # =========================================================================

    def login(self):
        """Logs into the store using a provided login and password"""
        if not self.site.login:
            # How was this called anyway?
            return False

        self.driver.get(self.build_url(self.site.login))
        self._fill_form_item(
            self.site.login_user,
            self.config.login['User']
        )
        self._fill_form_item(
            self.site.login_password,
            self.config.login['Password']
        )

        self._find_element(self.site.login_button).click()

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

        good_links = self.filter_links(links, elements)

        # Add to our cart
        for link in good_links:
            self.add_to_cart(link)

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
