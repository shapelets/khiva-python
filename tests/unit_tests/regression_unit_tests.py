# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
from khiva.regression import *
from khiva.array import Array
import numpy as np


########################################################################################################################


class RegressionTest(unittest.TestCase):
    DELTA = 1e-6

    def setUp(self):
        pass

    def test_linear(self):
        euclidean_result = linear(Array([0.24580423, 0.59642861, 0.35879163, 0.37891011, 0.02445137,
                                         0.23830957, 0.38793433, 0.68054104, 0.83934083, 0.76073689]),
                                  Array([0.2217416, 0.06344161, 0.77944375, 0.72174137, 0.19413884,
                                         0.51146167, 0.06880307, 0.39414268, 0.98172767, 0.30490851]))
        self.assertAlmostEqual(euclidean_result[0].to_numpy(), 0.344864266, delta=self.DELTA)
        self.assertAlmostEqual(euclidean_result[1].to_numpy(), 0.268578232, delta=self.DELTA)
        self.assertAlmostEqual(euclidean_result[2].to_numpy(), 0.283552942, delta=self.DELTA)
        self.assertAlmostEqual(euclidean_result[3].to_numpy(), 0.427239418, delta=self.DELTA)
        self.assertAlmostEqual(euclidean_result[4].to_numpy(), 0.412351891, delta=self.DELTA)

    def test_linear_multiple_time_series(self):
        euclidean_result = linear(Array([[0.24580423, 0.59642861, 0.35879163, 0.37891011, 0.02445137,
                                          0.23830957, 0.38793433, 0.68054104, 0.83934083, 0.76073689],
                                         [0.24580423, 0.59642861, 0.35879163, 0.37891011, 0.02445137,
                                          0.23830957, 0.38793433, 0.68054104, 0.83934083, 0.76073689]]),
                                  Array([[0.2217416, 0.06344161, 0.77944375, 0.72174137, 0.19413884,
                                          0.51146167, 0.06880307, 0.39414268, 0.98172767, 0.30490851],
                                         [0.2217416, 0.06344161, 0.77944375, 0.72174137, 0.19413884,
                                          0.51146167, 0.06880307, 0.39414268, 0.98172767, 0.30490851]]))
        slope = euclidean_result[0].to_numpy()
        intercept = euclidean_result[1].to_numpy()
        rvalue = euclidean_result[2].to_numpy()
        pvalue = euclidean_result[3].to_numpy()
        stderrest = euclidean_result[4].to_numpy()

        self.assertAlmostEqual(slope[0], 0.344864266, delta=self.DELTA)
        self.assertAlmostEqual(intercept[0], 0.268578232, delta=self.DELTA)
        self.assertAlmostEqual(rvalue[0], 0.283552942, delta=self.DELTA)
        self.assertAlmostEqual(pvalue[0], 0.427239418, delta=self.DELTA)
        self.assertAlmostEqual(stderrest[0], 0.412351891, delta=self.DELTA)

        self.assertAlmostEqual(slope[1], 0.344864266, delta=self.DELTA)
        self.assertAlmostEqual(intercept[1], 0.268578232, delta=self.DELTA)
        self.assertAlmostEqual(rvalue[1], 0.283552942, delta=self.DELTA)
        self.assertAlmostEqual(pvalue[1], 0.427239418, delta=self.DELTA)
        self.assertAlmostEqual(stderrest[1], 0.412351891, delta=self.DELTA)


if __name__ == '__main__':
    unittest.main()
