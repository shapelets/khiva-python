=========
Changelog
=========

KHIVA uses `Semantic Versioning <http://semver.org/>`_

Version 0.2.0
=============

Added
 - KMeans algorithm.
 - KShape Algorithm.
 - Added Ljung-Box test.
 - Installation script for Windows.
 - SBD distance function.
 - Header checks in all header files from core library and bindings.

Changed
 - Implementation improvement of stomp function and find motifs and discords functions.
 - Readme and installation Guide have been improved.

Fixed
 - PAA method.
 - Crosscorrelation function to work with several time series.
 - Conan script to work with new conan version.
 - Documentation generator to work with new PIP version.
 - Cmake path for windows in installation guide.

Version 0.1.0
=============

Added
- Binding for Matlab.
- Statistics namespace.
- Features namespace.
- Dimensionality namespace.
- Polynomial namespace.
- LinAlg namespace.
- Normalization namespace.
- Regression namespace.
- Regularization namespace.
- Support for Windows and Linux (Ubuntu 16.04 LTS).
- Documentation using breathe.
- Async. memory management.
- Operators for Khiva Arrays class for all bindings (Java, Python, C++, R)

Removed
- Simplification namespace.

Version 0.0.1
=============

Added
- We have set Arrayfire as an abstraction layer to run on top of accelerators that are able to run OpenCL.
- Implementation of STOMP method.
- (Mueen's Algorithm for Similarity Search) MASS algorithm implementation.
- Implementation of Simplification algorithms (Visvalingam and PIP).
- Benchmarks Suite (based on Google Benchmark).
- Test Suite (Google Test).
- New Features Algorithms.
- Binding for Python, R, Java.
- Matrix namespace.
- Distances namespace.
- Simplification namespace.
