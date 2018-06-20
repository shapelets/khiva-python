#!/bin/bash
# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    brew upgrade pyenv
    export PATH=$HOME/.pyenv/shims:$PATH
    export PYTHON_VERSION=$(echo $TRAVIS_PYTHON_VERSION | awk -F'.' '{print $1 "." $2}')
    pyenv install ${TRAVIS_PYTHON_VERSION}
    pyenv init -

    pyenv local ${TRAVIS_PYTHON_VERSION}

    which python${PYTHON_VERSION}
    python${PYTHON_VERSION} --version

    sudo pip${PYTHON_VERSION} install -r requirements.txt
    sudo pip${PYTHON_VERSION} install -r test-requirements.txt
    sudo pip${PYTHON_VERSION} install codecov
else
    pip install -r requirements.txt
    pip install -r test-requirements.txt
    pip install codecov
fi


