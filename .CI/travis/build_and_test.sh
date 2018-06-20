#!/bin/bash
# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Build the project

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    sudo python3 setup.py install
    python3 -m unittest discover tests/unit_tests *_tests.py -f -v
else
    python setup.py install
    coverage run -m unittest discover tests/unit_tests *_tests.py -f -v
fi
