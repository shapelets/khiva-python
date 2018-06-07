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
from khiva.normalization import *
from khiva.array import Array, dtype


########################################################################################################################

class NormalizationTest(unittest.TestCase):
    DELTA = 1e-6
    DECIMAL = 6

    def setUp(self):
        pass

    def test_znorm(self):
        znorm_result = znorm(Array([[0, 1, 2, 3], [4, 5, 6, 7]]), 0.00000001).to_numpy().flatten()
        expected = [-1.341640786499870, -0.447213595499958, 0.447213595499958, 1.341640786499870]
        for i in range(len(expected)):
            self.assertAlmostEqual(znorm_result[i], expected[i], delta=self.DELTA)
            self.assertAlmostEqual(znorm_result[i + 4], expected[i], delta=self.DELTA)

    def test_znorm_in_place(self):
        tss = Array(data=[[0, 1, 2, 3], [4, 5, 6, 7]])
        znorm_in_place(tss)
        tss = tss.to_numpy()
        self.assertAlmostEqual(tss[0][0], -1.341640786499870, delta=self.DELTA)
        self.assertAlmostEqual(tss[0][1], -0.447213595499958, delta=self.DELTA)
        self.assertAlmostEqual(tss[0][2], 0.447213595499958, delta=self.DELTA)
        self.assertAlmostEqual(tss[0][3], 1.341640786499870, delta=self.DELTA)

        self.assertAlmostEqual(tss[1][0], -1.341640786499870, delta=self.DELTA)
        self.assertAlmostEqual(tss[1][1], -0.447213595499958, delta=self.DELTA)
        self.assertAlmostEqual(tss[1][2], 0.447213595499958, delta=self.DELTA)
        self.assertAlmostEqual(tss[1][3], 1.341640786499870, delta=self.DELTA)

    def test_max_min_norm(self):
        max_min_norm_result = max_min_norm(Array([[0, 1, 2, 3], [4, 5, 6, 7]]), 2.0, 1.0).to_numpy()
        expected = np.array([[1.0, 1.3333333333333, 1.66666667, 2.0], [1.0, 1.3333333333333, 1.66666667, 2.0]])
        np.testing.assert_array_almost_equal(max_min_norm_result, expected, decimal=self.DECIMAL)

    def test_max_min_norm_in_place(self):
        tss = Array([[0, 1, 2, 3], [4, 5, 6, 7]])
        max_min_norm_in_place(tss, 2.0, 1.0)
        tss = tss.to_numpy()
        expected = np.array([[1.0, 1.3333333333333, 1.66666667, 2.0], [1.0, 1.3333333333333, 1.66666667, 2.0]])
        np.testing.assert_array_almost_equal(tss, expected, decimal=self.DECIMAL)

    def test_decimal_scaling_norm(self):
        decimal_scaling_norm_result = decimal_scaling_norm(Array([[0, 1, -2, 3], [40, 50, 60, -70]])).to_numpy()
        expected = np.array([[0.0, 0.1, -0.2, 0.3], [0.4, 0.5, 0.6, -0.7]])
        np.testing.assert_array_almost_equal(decimal_scaling_norm_result, expected, decimal=self.DECIMAL)

    def test_decimal_scaling_norm_in_place(self):
        tss = Array([[0, 1, -2, 3], [40, 50, 60, -70]])
        decimal_scaling_norm_in_place(tss)
        tss = tss.to_numpy()
        expected = np.array([[0.0, 0.1, -0.2, 0.3], [0.4, 0.5, 0.6, -0.7]])
        np.testing.assert_array_almost_equal(tss, expected, decimal=self.DECIMAL)

    def test_mean_norm(self):
        result = mean_norm(Array([[0, 1, 2, 3], [4, 5, 6, 7]])).to_numpy()
        expected = np.array([[-0.5, -0.166666667, 0.166666667, 0.5], [-0.5, -0.166666667, 0.166666667, 0.5]])
        np.testing.assert_array_almost_equal(result, expected, decimal=self.DECIMAL)

    def test_mean_norm_in_place(self):
        a = Array([[0, 1, 2, 3], [4, 5, 6, 7]])
        mean_norm_in_place(a)
        expected = np.array([[-0.5, -0.166666667, 0.166666667, 0.5], [-0.5, -0.166666667, 0.166666667, 0.5]])
        np.testing.assert_array_almost_equal(a.to_numpy(), expected, decimal=self.DECIMAL)


if __name__ == '__main__':
    unittest.main()
