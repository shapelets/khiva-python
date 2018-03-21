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

    def test_set_backend(self):
        backends = get_backends()
        cuda = backends & 2
        opencl = backends & 4
        cpu = backends & 1
        
        if cuda:
            set_backend(2)
            self.assertEqual(get_backend(), 2)
        if opencl:
            set_backend(4)
            self.assertEqual(get_backend(), 4)
        if cpu:
            set_backend(1)
            self.assertEqual(get_backend(), 1)

    def test_get_device(self):
        backends = get_backends()
        cuda = backends & 2
        opencl = backends & 4
        cpu = backends & 1

        if cuda:
            set_backend(2)
            set_device(0)
            self.assertEqual(get_device(), 0)
        if opencl:
            set_backend(4)
            set_device(0)
            self.assertEqual(get_device(), 0)
            set_device(1)
            self.assertEqual(get_device(), 1)
        if cpu:
            set_backend(1)
            set_device(0)
            self.assertEqual(get_device(), 0)


if __name__ == '__main__':
    unittest.main()
