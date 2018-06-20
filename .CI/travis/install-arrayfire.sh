#!/bin/bash
# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    if [ ! -e "installers/ArrayFire-no-gl-v3.5.1_OSX.pkg" ]; then
        wget http://arrayfire.s3.amazonaws.com/3.5.1/ArrayFire-no-gl-v3.5.1_OSX.pkg -O installers/ArrayFire-no-gl-v3.5.1_OSX.pkg
    fi

    # Installs arrayfire
    sudo installer -pkg installers/ArrayFire-no-gl-v3.5.1_OSX.pkg -target /
else
    if [ ! -e "installers/ArrayFire-no-gl-v3.5.1_Linux_x86_64.sh" ]; then
        wget http://arrayfire.s3.amazonaws.com/3.5.1/ArrayFire-no-gl-v3.5.1_Linux_x86_64.sh -O installers/ArrayFire-no-gl-v3.5.1_Linux_x86_64.sh
        chmod +x installers/ArrayFire-no-gl-v3.5.1_Linux_x86_64.sh
    fi

    sudo ./installers/ArrayFire-no-gl-v3.5.1_Linux_x86_64.sh --prefix=/usr/local --skip-license
fi
