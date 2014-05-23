#!/usr/bin/env python
"""

Vengeance
=========

Watches a twitter handle for an 'on sale now' text string, then attempts to
buy indicated items from a store's website in a speedy fashion. Designed
after a seller's continued, repeated refusal to update their drop system
to something that would discourage scalpers.

Designed to hopefully be faster than the scalpers themselves.

Initial tests have clocked in the baseline Selenium implementation at buying
a single item in under 7 seconds from the tweet time. If the item is super
popular, this is still not fast enough to beat the other more advanced
scalpers.

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

# Vengeance Imports
from browser import BuyerSelenium
from config import Config
from streamer import sale_watch

# =============================================================================
# GLOBALS
# =============================================================================

# =============================================================================
# MAIN
# =============================================================================


def main():
    """Main script for vengeance"""

    # Note that we're reading from config.ini
    # sample_config.ini should be filled out and renamed.
    #
    # DO NOT COMMIT A FILLED OUT CONFIG.INI TO THE REPOSITORY.
    v_config = Config('../config.ini')
    v_config.debug()

    # buyer is the browser object that sale_watch will kick off.
    buyer = BuyerSelenium(v_config)

    # sale_watch watches the twitter than calls the run method of buyer.
    sale_watch(v_config, buyer)

    print 'done'

# =============================================================================
# RUNNER
# =============================================================================

if __name__ == '__main__':
    main()