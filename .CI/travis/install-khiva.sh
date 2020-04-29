#!/bin/bash
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

function check-error() {
  KHIVA_ERROR=$?
  if [ $KHIVA_ERROR -ne 0 ]; then
      echo "$1: $KHIVA_ERROR"
      exit $KHIVA_ERROR
  fi
}

cmake --version
#Installing conan and dependencies
if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    pip install conan
else
    pip${PYTHON_VERSION} install conan
fi

# Cloning Github repo into khiva-library folder
git clone --depth 1 --recurse-submodules -q https://github.com/shapelets/khiva.git khiva-library
cd khiva-library
mkdir -p build && cd build
conan profile new --detect --force default
if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    conan profile update settings.compiler.libcxx=libc++ default
    conan profile update settings.compiler=apple-clang default
    conan profile update settings.compiler.version=9.1 default
    conan install .. --build missing
    cmake .. -DKHIVA_ONLY_CPU_BACKEND=ON -DKHIVA_BUILD_DOCUMENTATION=OFF -DKHIVA_BUILD_EXAMPLES=OFF -DKHIVA_BUILD_BENCHMARKS=OFF
    check-error "Error generating CMake configuration"
    make install -j8
    check-error "Error building Khiva"
else
    conan profile update settings.compiler.libcxx=libstdc++11 default
    conan profile update settings.compiler.version=7 default
    conan install .. --build missing
    cmake .. -DKHIVA_ENABLE_COVERAGE=ON -DKHIVA_BUILD_DOCUMENTATION=OFF -DKHIVA_BUILD_EXAMPLES=OFF -DKHIVA_BUILD_BENCHMARKS=OFF
    check-error "Error generating CMake configuration"
    sudo make install -j8
    check-error "Error building Khiva"
    sudo ldconfig
fi
# Switching back to the khiva-python folder
cd ../..