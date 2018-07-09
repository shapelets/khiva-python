# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
import os
import re
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
        self.assertEqual(version(), self.get_khiva_version_from_file())

    def get_khiva_version_from_github(self):
        # Hit Github API to get the list of tags.
        r = requests.get('https://api.github.com/repos/shapelets/khiva/tags')
        tag_name = '0.1.0'

        if r.status_code == 200:
            response = r.json()
            number_tags = len(response)
            tag_name = response[number_tags - 1]['name']

            # Remove symbols from numbering
            tag_name = tag_name.replace('v', '')
            tag_name = tag_name.replace('-RC', '')

        return tag_name

    def get_khiva_version_from_file(self):

        version = ""
        if os.name == 'nt':
            path_file = "C:/Program Files/Khiva/include/khiva/version.h"
        else:
            path_file = "/usr/local/include/khiva/version.h"

        version_file = open(path_file, "rt")
        contents = version_file.read()
        version_file.close()

        regex = r"([0-9]+.[0-9]+.[0-9]+)"
        match = re.search(regex, contents)
        if match:
           version = match.group(0)
        return version

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LibraryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)