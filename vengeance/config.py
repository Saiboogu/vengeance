#!/usr/bin/env python
"""

Config
======

Config object that parses a config.ini for our specific options.

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

import ConfigParser

# =============================================================================
# CLASSES
# =============================================================================


class Config(object):
    """Parses ini file for configuration options"""
    def __init__(self, config_file):
        self._config = ConfigParser.ConfigParser()
        self._config.read(config_file)

        self._oauth = self._read_oauth()
        self._twitter_user = self._config.get('Target', "TwitterHandle")
        if self._twitter_user.startswith('@'):
            self._twitter_user = self._twitter_user[1:]
        self._base_url = self._config.get('Target', 'BaseURL')
        self._targets = self._read_targets()

        self._consumer = self._read_consumer()

    # Properties ==============================================================

    @property
    def oauth(self):
        """Returns a dict with OAuth keys"""
        return self._oauth

    @property
    def base_url(self):
        """Returns the base URL we are targeting"""
        return self._base_url

    @property
    def twitter_user(self):
        """Returns the twitter user we want to watch"""
        return self._twitter_user

    @property
    def targets(self):
        """Returns the items we are trying to purchase"""
        return self._targets

    @property
    def consumer(self):
        """Returns the consumer information to fulfill the transaction"""
        return self._consumer

    # Private Methods =========================================================

    def _read_oauth(self):
        """Reads the oauth section"""
        section = 'OAuth'
        keys = [
            'ConsumerKey',
            'ConsumerSecret',
            'AccessToken',
            'AccessTokenSecret'
        ]
        return {
            keys[i]: self._config.get(
                section, keys[i]
            ) for i in xrange(len(keys))
        }

    # =========================================================================

    def _read_targets(self):
        """Returns a dictionary of target items and quantities"""
        section = 'Target'
        targets = self._config.get(section, 'Products').split(',')
        quantities = self._config.get(section, 'Quantities').split(',')
        return {targets[i]: quantities[i] for i in xrange(len(targets))}

    # =========================================================================

    def _read_consumer(self):
        """Returns a dictionary of form information"""
        section = 'ConsumerInfo'
        keys = [
            'Email',
            'FirstName',
            'LastName',
            'Phone',
            'Address',
            'Apt',
            'City',
            'Country',
            'State',
            'Zip',
            'CCN',
            'ExpMo',
            'ExpYr',
            'Type',
            'CVV'
        ]
        return {
            keys[i]: self._config.get(
                section, keys[i]
            ) for i in xrange(len(keys))
        }

    # Public Methods ==========================================================

    def debug(self):
        """Prints all attributes"""
        print 'Oauth:', self.oauth
        print 'Twitter User:', self.twitter_user
        print 'Base URL:', self.base_url
        print 'Targets:', self.targets
        print 'Consumer:', self.consumer
