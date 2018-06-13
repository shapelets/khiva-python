# README #
This is the KHIVA binding for connecting the Python programming language and the KHIVA library.

## License
This project is licensed under [MPL-v2](https://www.mozilla.org/en-US/MPL/2.0/).
 
## Quick Summary
This Python library called 'khiva' provides all the functionalities of the KHIVA library for time series analytics.

## Set up
It is just needed to execute the next command in the root directory of the project:
```bash
python3 setup.py install
```
  
## Executing the tests:
The tests can be executed and they are located in <project-root-dir>/tests/unit_tests.
 
## Documentation
This Python library follows the standard way of writing documentation of Python by using Sphinx.

In order to generate the documentation (in html format), run the following command under the <project-root-dir>/docs folder:
```bash
make html
```

### Contributing
The rules to contribute to this project are described [here](CONTRIBUTING.md)
 
 ### Builds
We have a first approach to generate a build and execute the set of tests on every pull request to the **develop** 
branch. This process uses **travis** and **appveyor** and is currently under setup.