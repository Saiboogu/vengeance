#!/usr/bin/env python
"""

Streamer
========

Stores streaming objects and functions

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
from tweepy import OAuthHandler, Stream, StreamListener

# =============================================================================
# GLOBALS
# =============================================================================

__all__ = [
    'SaleListener',
    'sale_watch',
]

# =============================================================================
# CLASSES
# =============================================================================


class SaleListener(StreamListener):
    """ A listener handles tweets are the received from the stream."""
    def __init__(self, buyer):
        super(SaleListener, self).__init__()
        self.buyer = buyer

    def on_status(self, status):
        tweet = status.text.lower()
        print tweet
        if 'nba' in tweet:
            self.buyer.run()
            return False
        else:
            return True

    def on_error(self, status):
        print status

# =============================================================================
# PUBLIC FUNCTIONS
# =============================================================================


def sale_watch(config, buyer):
    """Uses a twitter stream to watch for a sale"""

    # Go to http://dev.twitter.com and create an app.
    # The consumer key and secret will be generated for you after
    consumer_key = config.oauth['ConsumerKey']
    consumer_secret = config.oauth['ConsumerSecret']

    # After the step above, you will be redirected to your app's page.
    # Create an access token under the the "Your access token" section
    access_token = config.oauth['AccessToken']
    access_token_secret = config.oauth['AccessTokenSecret']

    listener = SaleListener(buyer)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listener)
    stream.filter(track=['basketball'])
