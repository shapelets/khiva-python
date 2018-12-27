#!/bin/bash
# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    brew install --force fftw freeimage fontconfig glfw glbinding
    if [ ! -e "./installers/ArrayFire-v3.6.2_OSX_x86_64.pkg" ]; then
        wget http://arrayfire.s3.amazonaws.com/3.6.2/ArrayFire-v3.6.2_OSX_x86_64.pkg -O installers/ArrayFire-v3.6.2_OSX_x86_64.pkg
    fi

    # Installs arrayfire
    sudo installer -pkg ./installers/ArrayFire-v3.6.2_OSX_x86_64.pkg -target /

    # The new ArrayFire installer installs to /opt/arrayfire, moving to /usr/local/lib
    sudo mv /opt/arrayfire/include/* /usr/local/include
    sudo mv /opt/arrayfire/lib/* /usr/local/lib
    sudo mv /opt/arrayfire/share/* /usr/local/share
    sudo rm -rf /opt/arrayfire
else
    if [ ! -e "./installers/ArrayFire-v3.6.2_Linux_x86_64.sh" ]; then
        wget http://arrayfire.s3.amazonaws.com/3.6.2/ArrayFire-v3.6.2_Linux_x86_64.sh -O installers/ArrayFire-v3.6.2_Linux_x86_64.sh
    fi

    sudo mkdir -p /opt/arrayfire-3
    sudo bash installers/ArrayFire-v3.6.2_Linux_x86_64.sh --prefix=/opt/arrayfire-3 --skip-license
    sudo ln -s /opt/arrayfire-3/lib64 /opt/arrayfire-3/lib
    echo "/opt/arrayfire-3/lib" | sudo tee /etc/ld.so.conf.d/arrayfire.conf
    sudo ldconfig
fi
