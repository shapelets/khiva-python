#!/usr/bin/python

# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

########################################################################################################################
# IMPORT
########################################################################################################################
from setuptools import setup, find_packages
import subprocess
import platform
import logging
from pathlib import Path
########################################################################################################################


library_installed = False

if platform.system() == 'Darwin':
    tsalibrary = Path("/usr/local/lib/libtsa_c.dylib")
    library_installed = tsalibrary.is_file()
elif platform.system() == 'Windows':
    tsalibrary = Path("C:\\Program Files\\TSA\\lib\\tsa_c.dll")
    library_installed = tsalibrary.is_file()
elif platform.system() == 'Linux':
    tsalibrary = Path("/usr/local/lib/libtsa_c.so")
    library_installed = tsalibrary.is_file()

if library_installed:
    setup(
        author="Grumpy Cat Software S.L.",
        author_email="info@gcatsoft.com",
        name="tsa",
        version=subprocess.check_output(["git", "describe"]).strip().decode("utf-8")[1:].split('-')[0],
        description="Python bindings for tsa",
        license="MPL 2.0",
        url="http://gcatsoft.com",
        packages=find_packages()
    )
else:
    logging.error("C++ TSA library not installed. Please, follow the steps for installing the library in: <C++ TSA "
                  "Library>")