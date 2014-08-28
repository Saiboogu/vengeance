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

def refresh_page_mondo(page, rate=5):
    """Refreshes a page and checks for change in available links"""
    previous = []
    first_run = True

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'vary': 'Accept-Encoding,Cookie'
    }

    while True:
        start_time = datetime.utcnow()

        request = requests.get(page, headers=headers)

        # Need to see if they're returning a forbidden style status code
        if 400 <= request.status_code < 500:
            print "Request got a bad status"
            print request.status_code
            print start_time
            sleep(rate * 5)
            continue
        elif request.status_code >= 500:
            print "Request got a broken website status"
            print request.status_code
            print start_time
            sleep(rate)
            continue
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
            print "Available != previous"
            if available:
                print "Available found, returning available"
                return available
            else:
                # If available is now empty, we need to empty out previous
                # So we can tell when a drop is back on.
                print "But available is now empty. Setting previous to be empty"
                previous = available
        elif first_run:
            # This was our first check, so we'll set our compare result
            print "First run completed, poster list is:"
            print available
            previous = available
            first_run = False

        # If our available list still matches our previous list, we just wait
        # a little bit then loop again.

        print "No changes detected, available list is as follows:"
        print available

        # We should make sure we're refreshing the page at most every 5 seconds
        # but don't wait if we've taken longer than 5 seconds.
        duration = datetime.utcnow() - start_time
        print datetime.utcnow(),
        print duration
        if duration.seconds < rate:
            sleep(rate - duration.seconds)


def refresh_page_tong(page, rate=5):
    """Refreshes a page and checks for change in available links"""
    previous = []
    first_run = True

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'vary': 'Accept-Encoding,Cookie'
    }

    while True:
        start_time = datetime.utcnow()

        request = requests.get(page, headers=headers)

        # Need to see if they're returning a forbidden style status code
        if 400 <= request.status_code < 500:
            print "Request got a bad status"
            print request.status_code
            print start_time
            sleep(rate * 5)
            continue
        elif request.status_code >= 500:
            print "Request got a broken website status"
            print request.status_code
            print start_time
            sleep(rate)
            continue
        main_soup = BeautifulSoup(request.text)

        # Find all links with a class of 'gallery_thumb'
        links = main_soup.find_all("a", class_='gallery_thumb')
        available = [link.get("href").lower() for link in links]
        available.sort()

        first_run = False

        if not first_run and available != previous:
            # If this isn't our first run and the new result doesn't match
            # previous, we've got new drops!
            print "Available != previous"
            if available:
                print "Available found, returning available"
                return available
            else:
                # If available is now empty, we need to empty out previous
                # So we can tell when a drop is back on.
                print "But available is now empty. Setting previous to be empty"
                previous = available
        elif first_run:
            # This was our first check, so we'll set our compare result
            print "First run completed, poster list is:"
            print available
            previous = available
            first_run = False

        # If our available list still matches our previous list, we just wait
        # a little bit then loop again.

        print "No changes detected, available list is as follows:"
        print available

        # We should make sure we're refreshing the page at most every 5 seconds
        # but don't wait if we've taken longer than 5 seconds.
        duration = datetime.utcnow() - start_time
        print datetime.utcnow(),
        print duration
        if duration.seconds < rate:
            sleep(rate - duration.seconds)
