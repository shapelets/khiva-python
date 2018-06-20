#!/bin/bash
# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    brew install pyenv
    export PATH=$HOME/.pyenv/shims:$PATH
    pyenv install $PYTHONVERSION
    pyenv init -
fi

pip install -r requirements.txt
pip install -r test-requirements.txt
pip install codecov
