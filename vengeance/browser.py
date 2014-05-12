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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# =============================================================================
# GLOBALS
# =============================================================================

all = [
]

# =============================================================================
# CLASSES
# =============================================================================


class BuyerSelenium(object):
    """Reference implementation of the Buyer"""
    def __init__(self, config):
        self._config = config
        self._driver = webdriver.Firefox()

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

    def fill_form_dict(self, form_dict):
        """Fills an entire form using a dictionary to dictate name & values"""
        for form in form_dict:
            self.fill_form(form, form_values[form])

    def fill_form_item(self, name, value):
        """Fills a single form item"""
        form = self.driver.find_element_by_name(name)
        form.send_keys(value)

    def get_links(self):
        """Fetches all links from the current page and returns as list"""
        return self.driver.find_elements_by_tag_name('a')

    def run(self):
        self.driver.get(self.build_url('view_category.asp?cat=12'))

        # Find the link we want
        links = self.get_links()
        for link in links:
            href = link.get_attribute('href').lower()
            if self.config.targets[0].lower() in href:
                link.click()
                break

        # Add to our cart
        self.driver.find_element_by_name('Add').click()

        # Head to checkout
        self.driver.get(self.build_url('checkout.asp?step=1'))

# =============================================================================
# PUBLIC FUNCTIONS
# =============================================================================

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get('')

    links = driver.find_elements_by_tag_name('a')
    for link in links:
        href = link.get_attribute('href').lower()
        if '' in href:
            link.click()
            break

    # Add To Cart
    driver.find_element_by_name('Add').click()

    # Proceed to Checkout
    driver.find_element_by_xpath("//input[@value='Proceed to Checkout']").click()

    def fill_form(name, value):
        form = driver.find_element_by_name(name)
        driver.implicitly_wait(0.1)
        form.send_keys(value)

    form_values = {
        'email': 'blah@gmail.com',
        'shipping_firstname': 'first_name',
        'shipping_lastname': 'last_name',
        'shipping_company': 'company',
        'shipping_phone': '8183456578',
        'shipping_address': '2671 address',
        'shipping_address2': 'apt 5',
        'shipping_city': 'Hilo',
        'shipping_zip': '90066'
    }

    for form in form_values:
        fill_form(form, form_values[form])

    # Country
    driver.find_element_by_xpath("//select[@name='shipping_country']/option[text()='United States']").click()

    # State
    driver.find_element_by_xpath("//select[@name='shipping_state']/option[text()='California']").click()

    driver.find_element_by_name("Add22").click()

    use_shipping = driver.find_element_by_name('check1')
    use_shipping.click()

    cc_num = driver.find_element_by_name('ff11_ocardno')
    cc_num.send_keys('32168712368')

    # Exp Month and Year
    driver.find_element_by_xpath("//select[@name='ff11_ocardexpiresmonth']/option[text()='12']").click()
    driver.find_element_by_xpath("//select[@name='ff11_ocardexpiresyear']/option[text()='2020']").click()

    # Card Type
    driver.find_element_by_xpath("//select[@name='ff11_ocardtype']/option[text()='Mastercard']").click()
    driver.find_element_by_name('ff11_ocardcvv2').send_keys('777')

    check_out = driver.find_element_by_name('divCheckout')
    # Don't uncomment this.
    # check_out.click()