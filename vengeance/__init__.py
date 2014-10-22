#!/usr/bin/env python
"""

Vengeance
=========

Watches a page for updates to sale items, then attempts to purchase specified
items if they match an item name in the config file.

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
from browser import SeleniumBrowser
from config import Config
from refresher import refresh_page
from sites import SiteConfig

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

    s_config = SiteConfig(v_config.site)

    buyer = SeleniumBrowser(v_config, s_config)
    buyer.login()

    return

    drops = refresh_page(buyer.build_url(), rate=15)
    print drops
    buyer.run(drops)

    print 'done'

# =============================================================================
# RUNNER
# =============================================================================

if __name__ == '__main__':
    main()