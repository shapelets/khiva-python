# Khiva-Python

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://github.com/shapelets/khiva-python/blob/master/LICENSE.txt)  

| Build Documentation                                                                                                                                           | Build Linux and Mac OS                                                                                                                   |  Build Windows                                                                                                                                                                | Code Coverage                                                                                                                                                |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| [![Documentation Status](https://readthedocs.org/projects/khiva-python/badge/?version=latest)](https://khiva-python.readthedocs.io/en/master/?badge=master)   | [![Build Status](https://travis-ci.org/shapelets/khiva-python.svg?branch=master)](https://travis-ci.org/shapelets/khiva-python/branches) | [![Build status](https://ci.appveyor.com/api/projects/status/7f4n5n0iydicfd9p/branch/master?svg=true)](https://ci.appveyor.com/project/shapelets/khiva-python/branch/master)  |[![Coverage Status](https://codecov.io/gh/shapelets/khiva-python/branch/master/graph/badge.svg)](https://codecov.io/gh/shapelets/khiva-python/branch/master)  |

# README #
This is the Khiva Python binding, it allows the usage of Khiva library from Python.

## License
This project is licensed under [MPL-v2](https://www.mozilla.org/en-US/MPL/2.0/). 

## Quick Summary
This Python library called 'khiva' provides all the functionalities of the KHIVA library for time series analytics.

## Set up
It is just needed to execute the next command in the root directory of the project:
```bash
python3 setup.py install
```
> Note: By now, only 64-bit Python versions are supported. 

## Executing the tests:
The tests can be executed and they are located in <project-root-dir>/tests/unit_tests.
 
## Documentation
This Python library follows the standard way of writing documentation of Python by using Sphinx.

In order to generate the documentation (in html format), run the following command under the <project-root-dir>/docs folder:
```bash
make html
```

## Contributing
The rules to contribute to this project are described [here](CONTRIBUTING.md)

[![Powered by Shapelets](https://img.shields.io/badge/powered%20by-Shapelets-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://shapelets.io)
