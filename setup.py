#!/usr/bin/python

# Copyright (c) 2018 Shapelets.io
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
    khivalibrary = Path("/usr/local/lib/libkhiva_c.dylib")
    library_installed = khivalibrary.is_file()
elif platform.system() == 'Windows':
    khivalibrary = Path("C:\\Program Files\\KHIVA\\lib\\khiva_c.dll")
    library_installed = khivalibrary.is_file()
elif platform.system() == 'Linux':
    khivalibrary = Path("/usr/local/lib/libkhiva_c.so")
    library_installed = khivalibrary.is_file()

if library_installed:
    setup(
        author="Shapelets.io",
        author_email="info@gcatsoft.com",
        name="khiva",
        version=subprocess.check_output(["git", "describe"]).strip().decode("utf-8")[1:].split('-')[0],
        description="Python bindings for khiva",
        license="MPL 2.0",
        url="https://shapelets.io",
        packages=find_packages()
    )
else:
    logging.error("C++ KHIVA library not installed. Please, follow the steps for installing the library in: <C++ KHIVA "
                  "Library>")