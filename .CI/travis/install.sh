#!/bin/bash
# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    brew upgrade pyenv
    export PATH=$HOME/.pyenv/shims:$PATH
    pyenv install ${TRAVIS_PYTHON_VERSION}.5
    pyenv init -

    which python${TRAVIS_PYTHON_VERSION}
    python${TRAVIS_PYTHON_VERSION} --version

    sudo pip${TRAVIS_PYTHON_VERSION} install -r requirements.txt
    sudo pip${TRAVIS_PYTHON_VERSION} install -r test-requirements.txt
    sudo pip${TRAVIS_PYTHON_VERSION} install codecov
else
    pip install -r requirements.txt
    pip install -r test-requirements.txt
    pip install codecov
fi


