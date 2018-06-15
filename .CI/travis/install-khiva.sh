#!/bin/bash

# Installing khiva

wget https://github.com/shapelets/khiva/releases/download/v0.1.0/khiva-v0.1.0.sh
chmod +x khiva-v0.1.0.sh
sudo ./khiva-v0.1.0.sh --prefix=/usr/local --skip-license
rm khiva-v0.1.0.sh
