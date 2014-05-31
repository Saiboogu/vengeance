#!/usr/bin/env python
"""

Refresher
=======

Contains a pretty simple page refresher that checks a page for new links
at a designated rate. If new links are found, return the list of links

## License

Copyright (c) 2014 Robert Graham, Sean Wallitsch

Based off of Manatee, https://github.com/rpgraham84/manatee , a currently
unlicensed work of Robert Graham. Will need a compatible license here.

"""

# =============================================================================
# IMPORTS
# =============================================================================

from bs4 import BeautifulSoup
from datetime import datetime
import requests
from time import sleep


# =============================================================================
# PUBLIC FUNCTIONS
# =============================================================================

def refresh_page(page, rate=5):
    """Refreshes a page and checks for change in available links"""
    previous = []
    first_run = True

    while True:
        start_time = datetime.utcnow()

        request = requests.get(page)
        main_soup = BeautifulSoup(request.text)

        # Each drop on the page should be inside of a "li" class, and
        # drops seem to be the only thing inside of "li", however
        # that's not required for this to work.
        links = main_soup.find_all("li")
        available = [link.find("a").get("href").lower() for link in links]
        available.sort()

        if not first_run and available != previous:
            # If this isn't our first run and the new result doesn't match
            # previous, we've got new drops!
            if available:
                return available
            else:
                # If available is now empty, we need to empty out previous
                # So we can tell when a drop is back on.
                previous = available
        elif first_run:
            # This was our first check, so we'll set our compare result
            previous = available
            first_run = False

        # If our available list still matches our previous list, we just wait
        # a little bit then loop again.

        # We should make sure we're refreshing the page at most every 5 seconds
        # but don't wait if we've taken longer than 5 seconds.
        duration = datetime.utcnow() - start_time
        if duration.seconds < rate:
            sleep(rate - duration.seconds)
