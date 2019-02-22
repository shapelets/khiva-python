#!/bin/bash
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    brew install fftw freeimage
    if [ ! -e "./installers/arrayfire-no-gl.pkg" ]; then
        wget https://github.com/shapelets/arrayfire/releases/download/v3.6.2/arrayfire-no-gl.pkg -O installers/arrayfire-no-gl.pkg
    fi

    # Installs arrayfire
    sudo installer -pkg ./installers/arrayfire-no-gl.pkg -target /
else
    sudo apt-get update && \
    sudo apt-get install -y libboost-all-dev \
    libfftw3-dev \
    libfontconfig1-dev \
    libfreeimage-dev \
    liblapack-dev \
    liblapacke-dev \
    libopenblas-dev

    if [ ! -e "./installers/arrayfire-no-gl.sh" ]; then
        wget https://github.com/shapelets/arrayfire/releases/download/v3.6.2/arrayfire-no-gl.sh -O installers/arrayfire-no-gl.sh
    fi

    sudo mkdir -p /opt/arrayfire-3
    sudo bash installers/arrayfire-no-gl.sh --prefix=/opt/arrayfire-3 --skip-license
    sudo ln -s /opt/arrayfire-3/lib64 /opt/arrayfire-3/lib
    echo "/opt/arrayfire-3/lib" | sudo tee /etc/ld.so.conf.d/arrayfire.conf
    sudo ldconfig
fi
