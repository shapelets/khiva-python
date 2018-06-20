#!/bin/bash
# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

if [ ! -e "installers/khiva-v0.1.0.sh" ]; then
    wget https://github.com/shapelets/khiva/releases/download/v0.1.0/khiva-v0.1.0.sh -O installers/khiva-v0.1.0.sh
    chmod +x installers/khiva-v0.1.0.sh
fi

sudo ./installers/khiva-v0.1.0.sh --prefix=/usr/local --skip-license

ls -lah /usr/local/lib

sudo ldconfig

sudo ldconfig -p