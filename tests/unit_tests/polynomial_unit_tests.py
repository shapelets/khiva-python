# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
import numpy as np
from khiva.polynomial import *
from khiva.array import Array


########################################################################################################################

class PolynomialTest(unittest.TestCase):
    DELTA = 1e-6
    DECIMAL = 6

    def setUp(self):
        pass

    def test_polyfit1(self):
        polyfit_result = polyfit(Array([0, 1, 2, 3, 4, 5]), Array([0, 1, 2, 3, 4, 5]), 1).to_numpy()
        expected = np.array([1.0, 0.0])
        np.testing.assert_array_almost_equal(polyfit_result, expected, decimal=self.DECIMAL)

    def test_polyfit3(self):
        polyfit_result = polyfit(Array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0]), Array([0.0, 0.8, 0.9, 0.1, -0.8, -1.0]),
                                 3).to_numpy()
        expected = np.array([0.08703704, -0.81349206, 1.69312169, -0.03968254])
        np.testing.assert_array_almost_equal(polyfit_result, expected, decimal=self.DECIMAL - 1)

    def test_roots(self):
        roots_result = roots(Array([5, -20, 5, 50, -20, -40])).to_numpy()
        expected = np.array([2 + 0j, 2 + 0j, 2 + 0j, -1 + 0j, -1 + 0j])
        np.testing.assert_array_almost_equal(roots_result, expected, decimal=2)


if __name__ == '__main__':
    unittest.main()
