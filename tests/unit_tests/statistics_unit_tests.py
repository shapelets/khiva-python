#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
from khiva.statistics import *
from khiva.array import Array
import numpy as np
from khiva.library import set_backend, KHIVABackend


########################################################################################################################


class StatisticsTest(unittest.TestCase):

    def setUp(self):
        set_backend(KHIVABackend.KHIVA_BACKEND_CPU)

    def test_covariance_unbiased(self):
        result = covariance(Array(data=[[-2.1, -1, 4.3], [3, 1.1, 0.12], [3, 1.1, 0.12]]), True).to_numpy().flatten()
        expected = np.array([11.70999999, -4.286, -4.286, -4.286, 2.14413333,
                             2.14413333, -4.286, 2.14413333, 2.14413333])

        np.testing.assert_array_almost_equal(result, expected, decimal=6)

    def test_covariance_biased(self):
        result = covariance(Array(data=[[-2.1, -1, 4.3], [3, 1.1, 0.12], [3, 1.1, 0.12]]), False).to_numpy().flatten()
        expected = np.array([7.80666667, -2.85733333, -2.85733333, -2.85733333, 1.42942222,
                             1.42942222, -2.85733333, 1.42942222, 1.42942222])
        np.testing.assert_array_almost_equal(result, expected, decimal=6)

    def test_kurtosis(self):
        result = kurtosis(Array(data=[[0, 1, 2, 3, 4, 5], [2, 2, 2, 20, 30, 25]])).to_numpy().flatten()
        expected = np.array([-1.2, -2.66226722])
        np.testing.assert_array_almost_equal(result, expected, decimal=2)

    def test_ljung_box(self):
        result = ljung_box(Array(data=[[0, 1, 2, 3], [4, 5, 6, 7]]), 3).to_numpy().flatten()
        expected = np.array([6.4400, 6.4400])
        np.testing.assert_array_almost_equal(result, expected, decimal=6)

    def test_moment(self):
        result = moment(Array(data=[[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]]), 2).to_numpy().flatten()
        expected = np.array([9.166666666, 9.166666666])
        np.testing.assert_array_almost_equal(result, expected, decimal=6)
        result = moment(Array(data=[[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]]), 4).to_numpy().flatten()
        expected = np.array([163.1666666666, 163.1666666666])
        np.testing.assert_array_almost_equal(result, expected, decimal=2)

    def test_quantile(self):
        result = quantile(Array([[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]), Array([0.1, 0.2])).to_numpy().flatten()
        expected = np.array([0.5, 1.0, 6.5, 7.0])
        np.testing.assert_array_almost_equal(result, expected, decimal=2)

    def test_quantile_cut_2(self):
        result = quantiles_cut(Array([[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]), 2)
        a = result.transpose()
        expected = np.array([-0.00000001, 2.5, -0.00000001, 2.5, -0.00000001, 2.5, 2.5, 5.0, 2.5, 5.0, 2.5, 5.0,
                             6.0, 8.5, 6.0, 8.5, 6.0, 8.5, 8.5, 11.0, 8.5, 11.0, 8.5, 11.0])
        np.testing.assert_array_almost_equal(a.to_numpy().flatten(), expected, decimal=6)

    def test_quantile_cut_3(self):
        result = quantiles_cut(Array([[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]), 3)
        a = result.transpose()
        expected = np.array(
            [-0.00000001, 1.66666667, -0.00000001, 1.6666667, 1.6666667, 3.3333333, 1.6666667, 3.3333333,
             3.3333333, 5.0, 3.3333333, 5.0, 5.9999999, 7.66666667, 5.9999999, 7.6666667,
             7.6666667, 9.3333333, 7.6666667, 9.3333333, 9.3333333, 11.0, 9.3333333, 11.0])
        np.testing.assert_array_almost_equal(a.to_numpy().flatten(), expected, decimal=6)

    def test_quantile_cut_7(self):
        result = quantiles_cut(Array([[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]), 7)
        a = result.transpose()
        expected = np.array([0, 0.7142857, 0.7142857, 1.4285715, 1.4285715, 2.1428573, 2.8571429, 3.5714288,
                             3.5714288, 4.2857146, 4.2857146, 5, 5.9999999, 6.7142857, 6.7142857, 7.4285715,
                             7.4285715, 8.1428573, 8.8571429, 9.5714288, 9.5714288, 10.2857146, 10.2857146, 11])
        np.testing.assert_array_almost_equal(a.to_numpy().flatten(), expected, decimal=6)

    def test_sample_stdev(self):
        result = sample_stdev(Array(data=[[0, 1, 2, 3, 4, 5], [2, 2, 2, 20, 30, 25]])).to_numpy().flatten()
        expected = np.array([1.870828693, 12.988456413])
        np.testing.assert_array_almost_equal(result, expected, decimal=2)

    def test_skewness(self):
        result = skewness(Array(data=[[0, 1, 2, 3, 4, 5], [2, 2, 2, 20, 30, 25]])).to_numpy().flatten()
        expected = np.array([0.0, 0.236177069879499])
        np.testing.assert_array_almost_equal(result, expected, decimal=2)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(StatisticsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
