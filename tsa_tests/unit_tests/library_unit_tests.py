"""
Copyright (c) 2018 Grumpy Cat Software S.L.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
from tsa.tsa_libraries.library import *


########################################################################################################################

class LibraryTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_info(self):
        info()

    def test_setBackend(self):
        set_backend(1)
        info()

    def test_setDevice(self):
        set_device(1)
        info()

    def test_setBackendCPU(self):
        set_backend(0)
        info()

if __name__ == '__main__':
    unittest.main()
