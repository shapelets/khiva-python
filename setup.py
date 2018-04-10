#!/usr/bin/python

# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages
import subprocess

setup(
    author="Grumpy Cat Software S.L.",
    author_email="info@gcatsoft.com",
    name="tsa",
    version=subprocess.check_output(["git", "describe"]).strip().decode("utf-8")[-1:],
    description="Python bindings for tsa",
    license="MPL 2.0",
    url="http://gcatsoft.com",
    packages=find_packages()
)
