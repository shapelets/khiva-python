# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
import requests
from khiva.library import *

########################################################################################################################

class LibraryTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_set_backend(self):
        backends = get_backends()
        cuda = backends & KHIVABackend.KHIVA_BACKEND_CUDA.value
        opencl = backends & KHIVABackend.KHIVA_BACKEND_OPENCL.value
        cpu = backends & KHIVABackend.KHIVA_BACKEND_CPU.value
        b = get_backend()
        if cuda:
            set_backend(KHIVABackend.KHIVA_BACKEND_CUDA)
            self.assertEqual(get_backend(), KHIVABackend.KHIVA_BACKEND_CUDA)
            set_backend(b)

        if opencl:
            set_backend(KHIVABackend.KHIVA_BACKEND_OPENCL)
            self.assertEqual(get_backend(), KHIVABackend.KHIVA_BACKEND_OPENCL)
            set_backend(b)

        if cpu:
            set_backend(KHIVABackend.KHIVA_BACKEND_CPU)
            self.assertEqual(get_backend(), KHIVABackend.KHIVA_BACKEND_CPU)
            set_backend(b)

    def test_get_device(self):
        backends = get_backends()
        cuda = backends & KHIVABackend.KHIVA_BACKEND_CUDA.value
        opencl = backends & KHIVABackend.KHIVA_BACKEND_OPENCL.value
        cpu = backends & KHIVABackend.KHIVA_BACKEND_CPU.value
        if cuda:
            set_backend(KHIVABackend.KHIVA_BACKEND_CUDA)
            for i in range(get_device_count()):
                set_device(i)
                self.assertEqual(get_device_id(), i)

        if opencl:
            set_backend(KHIVABackend.KHIVA_BACKEND_OPENCL)
            for i in range(get_device_count()):
                set_device(i)
                self.assertEqual(get_device_id(), i)

        if cpu:
            set_backend(KHIVABackend.KHIVA_BACKEND_CPU)
            for i in range(get_device_count()):
                set_device(i)
                self.assertEqual(get_device_id(), i)

    def test_version(self):
        self.assertEqual(version(), self.get_khiva_version_from_github())

    def get_khiva_version_from_github(self):
        # Hit Github API to get the list of tags.
        r = requests.get('https://api.github.com/repos/shapelets/khiva/tags')
        tag_name = ''
        if r.ok:
            response = r.json()
            number_tags = len(response)
            tag_name = response[number_tags - 1]['name']

            # Remove symbols from numbering
            tag_name = tag_name.replace('v', '')
            tag_name = tag_name.replace('-RC', '')

        return tag_name


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LibraryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)