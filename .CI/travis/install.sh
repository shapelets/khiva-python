#!/bin/bash
# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    sudo pip${PYTHON_VERSION} install -r requirements.txt
    sudo pip${PYTHON_VERSION} install -r test-requirements.txt
    sudo pip${PYTHON_VERSION} install codecov
else
    pip install -r requirements.txt
    pip install -r test-requirements.txt
    pip install codecov
fi


