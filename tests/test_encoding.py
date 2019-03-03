#!/usr/bin/env python2.7
# coding=utf-8
# Author: echel0n <echel0n@sickrage.ca>
# URL: https://sickrage.ca
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.



import locale
import os.path
import unittest

import sickrage
import tests
from sickrage.core.helpers import sanitizeFileName


class EncodingTests(tests.SiCKRAGETestCase):
    def test_encoding(self):
        rootDir = 'C:\\Temp\\TV'
        strings = ['Les Enfants De La T\xe9l\xe9', 'RT� One']

        sickrage.app.sys_encoding = None

        try:
            locale.setlocale(locale.LC_ALL, "")
            sickrage.app.sys_encoding = locale.getpreferredencoding()
        except (locale.Error, IOError):
            pass

        # For OSes that are poorly configured I'll just randomly force UTF-8
        if not sickrage.app.sys_encoding or sickrage.app.sys_encoding in ('ANSI_X3.4-1968', 'US-ASCII', 'ASCII'):
            sickrage.app.sys_encoding = 'UTF-8'

        for s in strings:
            show_dir = os.path.join(rootDir, sanitizeFileName(s))
            self.assertIsInstance(show_dir, unicode)


if __name__ == "__main__":
    print "=================="
    print "STARTING - ENCODING TESTS"
    print "=================="
    print "######################################################################"
    unittest.main()
