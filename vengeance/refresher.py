#!/usr/bin/env python
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
import requests


def refresh_page(page, rate=5):
    """Refreshes a page and checks for change in available links"""
    previous = []
    first_run = True

    while True:
        start_time = datetime.utcnow()
        request = requests.get(page)
        main_soup = BeautifulSoup(request.text)
        links = main_soup.find_all("li")
        available = [link.find("a").get("href") for link in links]
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


print refresh_page('http://www.mondotees.com/')