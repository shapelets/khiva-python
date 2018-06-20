#!/bin/bash
# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

mkdir -p installers

if [ ! -e "installers/ArrayFire-no-gl-v3.5.1_OSX.pkg" ]; then
    wget http://arrayfire.s3.amazonaws.com/3.5.1/ArrayFire-no-gl-v3.5.1_OSX.pkg -O installers/ArrayFire-no-gl-v3.5.1_OSX.pkg
fi

sudo installer -pkg installers/ArrayFire-no-gl-v3.5.1_OSX.pkg -target /
