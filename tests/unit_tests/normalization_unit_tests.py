# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
import numpy as np
from tsa.normalization import *
from tsa.array import array, dtype


########################################################################################################################

class NormalizationTest(unittest.TestCase):
    DELTA = 1e-6

    def setUp(self):
        pass

    def test_znorm(self):
        znorm_result = znorm(array([[0, 1, 2, 3], [4, 5, 6, 7]]), 0.00000001).to_numpy().flatten()
        expected = [-1.341640786499870, -0.447213595499958, 0.447213595499958, 1.341640786499870]
        for i in range(len(expected)):
            self.assertAlmostEqual(znorm_result[i], expected[i], delta=self.DELTA)
            self.assertAlmostEqual(znorm_result[i + 4], expected[i], delta=self.DELTA)

    def test_znorm_in_place(self):
        tss = array(data=[[0, 1, 2, 3], [4, 5, 6, 7]])
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
        max_min_norm_result = max_min_norm(array([[0, 1, 2, 3], [4, 5, 6, 7]]), 2.0, 1.0).to_numpy()
        expected = np.array([[1.0, 1.3333333333333, 1.66666667, 2.0], [1.0, 1.3333333333333, 1.66666667, 2.0]])
        self.assertAlmostEqual(max_min_norm_result.all(), expected.all(), delta=self.DELTA)

    def test_max_min_norm_in_place(self):
        tss = array([[0, 1, 2, 3], [4, 5, 6, 7]])
        max_min_norm_in_place(tss, 2.0, 1.0)
        tss = tss.to_numpy()
        expected = np.array([[1.0, 1.3333333333333, 1.66666667, 2.0], [1.0, 1.3333333333333, 1.66666667, 2.0]])
        self.assertAlmostEqual(tss.all(), expected.all(), delta=self.DELTA)

    def test_decimal_scaling_norm(self):
        decimal_scaling_norm_result = decimal_scaling_norm(array([[0, 1, -2, 3], [40, 50, 60, -70]])).to_numpy()
        expected = np.array([[0.0, 0.1, -0.2, 0.3], [0.4, 0.5, 0.6, -0.7]])
        self.assertAlmostEqual(decimal_scaling_norm_result.all(), expected.all(), delta=self.DELTA)

    def test_decimal_scaling_norm_in_place(self):
        tss = array([[0, 1, -2, 3], [40, 50, 60, -70]])
        decimal_scaling_norm_in_place(tss)
        tss = tss.to_numpy()
        expected = np.array([[0.0, 0.1, -0.2, 0.3], [0.4, 0.5, 0.6, -0.7]])
        self.assertAlmostEqual(tss.all(), expected.all(), delta=self.DELTA)


if __name__ == '__main__':
    unittest.main()
