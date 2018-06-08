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

########################################################################################################################

with open("README.rst", "r") as handler:
    LONG_DESC = handler.read()

setup(
    author="Shapelets.io",
    author_email="dev@shapelets.io",
    name="khiva",
    version='v0.1.2',
    long_description = LONG_DESC,
    description="Python bindings for khiva",
    license="MPL 2.0",
    url="http://shapelets.io",
    packages=find_packages()
)