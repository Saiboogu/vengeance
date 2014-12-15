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
# GLOBALS
# =============================================================================

__all__ = [
    'Config',
]

# =============================================================================
# CLASSES
# =============================================================================


class Config(object):
    """Parses ini file for configuration options"""
    def __init__(self, config_file):
        self._config = ConfigParser.ConfigParser()
        self._config.read(config_file)

        self._site = self._config.get('Target', 'Site').lower()
        self._targets = self._read_targets()
        self._exclusions = self._read_excludes()

        self._login = self._read_login()
        self._consumer = self._read_consumer()

    # Properties ==============================================================

    @property
    def exclusions(self):
        """Returns the words to exclude from matched targets"""
        return self._exclusions

    @property
    def site(self):
        """Returns the site we are targeting"""
        return self._site

    @property
    def login(self):
        """Returns the login information"""
        return self._login

    @property
    def targets(self):
        """Returns the items we are trying to purchase"""
        return self._targets

    @property
    def consumer(self):
        """Returns the consumer information to fulfill the transaction"""
        return self._consumer

    # Private Methods =========================================================

    def _read_consumer(self):
        """Returns a dictionary of form information"""
        section = 'ConsumerInfo'
        keys = [
            'email',
            'first',
            'last',
            'company',
            'phone',
            'address',
            'address2',
            'city',
            'country',
            'province',
            'zip',
            'ccn',
            'exp_mo',
            'exp_yr',
            'type',
            'ccv'
        ]
        return {
            keys[i]: self._config.get(
                section, keys[i]
            ) for i in xrange(len(keys))
        }

    # =========================================================================

    def _read_excludes(self):
        """Returns a list of excluded items"""
        section = 'Target'
        excludes = self._config.get(section, 'Exclude').split(',')
        return [exclusion.lower() for exclusion in excludes]

    # =========================================================================

    def _read_login(self):
        """Returns a dictionary of the login information"""
        section = 'Login'
        keys = [
            'User',
            'Password'
        ]
        return {
            keys[i]: self._config.get(
                section, keys[i]
            ) for i in xrange(len(keys))
        }

    # =========================================================================

    def _read_targets(self):
        """Returns a list of target items"""
        section = 'Target'
        targets = self._config.get(section, 'Products').split(',')
        return [target.lower() for target in targets]

    # Public Methods ==========================================================

    def debug(self):
        """Prints all attributes"""
        print 'Site:', self.site
        print 'Targets:', self.targets
        print 'Excluded:', self.exclusions
        print 'Login:', self.login
        print 'Consumer:', self.consumer
