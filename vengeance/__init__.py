#!/usr/bin/env python
"""

Vengeance
=========

Watches a twitter handle for an 'on sale now' text string or watches a page
for new links, then attempts to buy indicated items from a store's website
in a speedy fashion. Designed after a seller's continued, repeated refusal to
update their drop system to something that would more discourage scalpers.

Designed to hopefully be faster than the scalpers themselves.

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
from browser import SeleniumBrowserTong
from config import Config
from refresher import refresh_page_tong
from streamer import tweet_watch

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

    buyer = SeleniumBrowserTong(v_config)

    if v_config.method == 'twitter':
        tweet_watch(v_config, buyer)
    elif v_config.method == 'refresh':
        drops = refresh_page_tong(buyer.build_url('for_sale'), rate=15)
        print drops
        buyer.run(drops)
    else:
        raise ValueError("Config Method must be set to 'twitter' or 'refresh'")

    print 'done'

# =============================================================================
# RUNNER
# =============================================================================

if __name__ == '__main__':
    main()