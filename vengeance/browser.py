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

# =============================================================================
# PUBLIC FUNCTIONS
# =============================================================================

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get('')

    # The link text is the visible text, not the a ref url
    target_elem = driver.find_element_by_link_text('')
    # If we don't wait here, it doesn't get clicked.
    driver.implicitly_wait(1)
    target_elem.click()

    # Add To Cart
    add = driver.find_element_by_name('Add')
    add.click()

    # Proceed to Checkout
    proceed = driver.find_element_by_xpath("//input[@value='Proceed to Checkout']")
    proceed.click()

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

    # Got to be a better way than this
    # We also leave Country at it's default.
    state = driver.find_element_by_name('shipping_state')
    state.send_keys(Keys.ARROW_DOWN)
    state.send_keys(Keys.ARROW_DOWN)
    state.send_keys(Keys.ARROW_DOWN)
    state.send_keys(Keys.ARROW_DOWN)
    state.send_keys(Keys.ARROW_DOWN)

    proceed = driver.find_element_by_name("Add22")
    proceed.click()

    use_shipping = driver.find_element_by_name('check1')
    use_shipping.click()

    cc_num = driver.find_element_by_name('ff11_ocardno')
    cc_num.send_keys('32168712368')

    # Exp Month and Year are not working
    cc_mo = driver.find_element_by_name('ff11_ocardexpiresmonth')
    cc_mo.send_keys('12')
    cc_year = driver.find_element_by_name('ff11_ocardexpiresyear')
    cc_year.send_keys('2020')

    # Card Type is not working
    cc_type = driver.find_element_by_name('ff11_ocardtype')
    cc_type.send_keys('Mastercard')
    cc_cvv = driver.find_element_by_name('ff11_ocardcvv2')
    cc_cvv.send_keys('777')

    check_out = driver.find_element_by_name('divCheckout')
    # Don't uncomment this.
    # check_out.click()
