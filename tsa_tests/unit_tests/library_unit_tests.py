# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


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
        cuda = backends & TSABackend.TSA_BACKEND_CUDA.value
        opencl = backends & TSABackend.TSA_BACKEND_OPENCL.value
        cpu = backends & TSABackend.TSA_BACKEND_CPU.value

        if cuda:
            set_backend(TSABackend.TSA_BACKEND_CUDA)
            self.assertEqual(get_backend(), TSABackend.TSA_BACKEND_CUDA)
        if opencl:
            set_backend(TSABackend.TSA_BACKEND_OPENCL)
            self.assertEqual(get_backend(), TSABackend.TSA_BACKEND_OPENCL)
        if cpu:
            set_backend(TSABackend.TSA_BACKEND_CPU)
            self.assertEqual(get_backend(), TSABackend.TSA_BACKEND_CPU)

    def test_get_device(self):
        backends = get_backends()
        cuda = backends & TSABackend.TSA_BACKEND_CUDA.value
        opencl = backends & TSABackend.TSA_BACKEND_OPENCL.value
        cpu = backends & TSABackend.TSA_BACKEND_CPU.value

        if cuda:
            set_backend(TSABackend.TSA_BACKEND_CUDA)
            for i in range(get_device_count()):
                set_device(i)
                self.assertEqual(get_device_id(), i)
        if opencl:
            set_backend(TSABackend.TSA_BACKEND_OPENCL)
            for i in range(get_device_count()):
                set_device(i)
                self.assertEqual(get_device_id(), i)

        if cpu:
            set_backend(TSABackend.TSA_BACKEND_CPU)
            for i in range(get_device_count()):
                set_device(i)
                self.assertEqual(get_device_id(), i)


if __name__ == '__main__':
    unittest.main()
