# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
########################################################################################################################

testmodules = [
    'array_unit_tests',
    'dimensionality_unit_tests',
    'distances_unit_tests',
    'features_unit_tests',
    'linalg_unit_tests',
    'matrix_unit_tests',
    'normalization_unit_tests',
    'polynomial_unit_tests',
    'regression_unit_tests',
    'regularization_unit_tests',
    'statistics_unit_tests',
    'library_unit_tests'
    ]

suite = unittest.TestSuite()

for t in testmodules:
    try:
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)