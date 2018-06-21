#!/bin/bash
# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    if [ ! -e "installers/khiva-v0.1.0.pkg" ]; then
        wget https://github.com/shapelets/khiva/releases/download/v0.1.0/khiva-v0.1.0-OnlyCPU.pkg -O installers/khiva-v0.1.0-OnlyCPU.pkg
    fi

    # Installs arrayfire
    sudo installer -pkg installers/khiva-v0.1.0-OnlyCPU.pkg -target /
else
    if [ ! -e "installers/khiva-v0.1.0-ci.sh" ]; then
        wget https://github.com/shapelets/khiva/releases/download/v0.1.0/khiva-v0.1.0-ci.sh -O installers/khiva-v0.1.0-ci.sh
        chmod +x installers/khiva-v0.1.0-ci.sh
    fi

    sudo ./installers/khiva-v0.1.0-ci.sh --prefix=/usr/local --skip-license

    sudo ldconfig
fi
