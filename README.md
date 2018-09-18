# Khiva-Python

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://github.com/shapelets/khiva-python/blob/master/LICENSE.txt)
[![Gitter chat](https://badges.gitter.im/shapelets-io/Lobby.svg)](https://gitter.im/shapelets-io/khiva-python?utm_source=share-link&utm_medium=link&utm_campaign=share-link)

| Build Documentation                                                                                                                                           | Build Linux and Mac OS                                                                                                                   |  Build Windows                                                                                                                                                                | Code Coverage                                                                                                                                                |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| [![Documentation Status](https://readthedocs.org/projects/khiva-python/badge/?version=latest)](https://khiva-python.readthedocs.io/en/master/?badge=master)   | [![Build Status](https://travis-ci.org/shapelets/khiva-python.svg?branch=master)](https://travis-ci.org/shapelets/khiva-python/branches) | [![Build status](https://ci.appveyor.com/api/projects/status/7f4n5n0iydicfd9p/branch/master?svg=true)](https://ci.appveyor.com/project/shapelets/khiva-python/branch/master)  |[![Coverage Status](https://codecov.io/gh/shapelets/khiva-python/branch/master/graph/badge.svg)](https://codecov.io/gh/shapelets/khiva-python/branch/master)  |

# README #
This is the Khiva Python binding, it allows the usage of Khiva library from Python.

## License
This project is licensed under [MPL-v2](https://www.mozilla.org/en-US/MPL/2.0/). 

## Quick Summary
This Python binding called 'khiva' provides all the functionalities of the KHIVA library for time series analytics.

## Set up
In order to use this binding, you need to install Khiva library.

### Prerequisites
- [Python 64-bits](https://www.python.org/downloads/)

> Note: By now, only 64-bit Python versions are supported.

> Note **Windows' users**: Search your 64-bits version [here](https://www.python.org/downloads/windows/)

### Install latest version
Install latest stable version of Khiva library. Follow the steps in the "Installation" section of the [Khiva repository](https://github.com/shapelets/khiva)

To install the Khiva Python binding, we just need to execute the following command:
```bash
python setup.py install
```

### Install any release
Install the prerequisites listed in the "Installation" section of the [Khiva library repository](https://github.com/shapelets/khiva). Download and install your selected Khiva release from [Khiva repository](https://github.com/shapelets/khiva/releases).

Install the Khiva python binding compatible with the Khiva library installed previously. Follow the steps to install the Khiva python binding explained in [pypi](https://pypi.org/project/khiva/).


## Executing the tests:
All tests can be executed separately, please find them in <project-root-dir>/tests/unit_tests.
 
## Documentation
This Khiva Python binding follows the standard way of writing documentation of Python by using Sphinx.

In order to generate the documentation (in html format), run the following command under the <project-root-dir>/docs folder:
```bash
make html
```

## Contributing
The rules to contribute to this project are described [here](CONTRIBUTING.md)

[![Powered by Shapelets](https://img.shields.io/badge/powered%20by-Shapelets-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://shapelets.io)
