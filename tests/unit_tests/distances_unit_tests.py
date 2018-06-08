# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
from khiva.distances import *
from khiva.array import Array
import numpy as np


########################################################################################################################


class DistancesTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_euclidean(self):
        euclidean_result = euclidean(Array(data=[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])).to_numpy().flatten()
        expected = np.array([0, 0, 0, 8, 0, 0, 16, 8, 0])
        np.testing.assert_array_almost_equal(euclidean_result, expected, decimal=1)

    def test_squared_euclidean(self):
        squared_euclidean_result = squared_euclidean(
            Array(data=[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])).to_numpy().flatten()
        expected = np.array([0, 0, 0, 64, 0, 0, 256, 64, 0])
        np.testing.assert_array_almost_equal(squared_euclidean_result, expected, decimal=1)

    def test_dtw(self):
        euclidean_result = dtw(Array(
            data=[[1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3], [4, 4, 4, 4, 4], [5, 5, 5, 5, 5]])).to_numpy()
        expected = np.array([[0, 0, 0, 0, 0], [5, 0, 0, 0, 0], [10, 5, 0, 0, 0], [15, 10, 5, 0, 0], [20, 15, 10, 5, 0]])
        np.testing.assert_array_almost_equal(euclidean_result, expected, decimal=1)

    def test_hamming(self):
        result = hamming(Array(
            data=[[1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3], [4, 4, 4, 4, 4], [5, 5, 5, 5, 5]])).to_numpy()
        expected = np.array([[0, 0, 0, 0, 0], [5, 0, 0, 0, 0], [5, 5, 0, 0, 0], [5, 5, 5, 0, 0], [5, 5, 5, 5, 0]])
        np.testing.assert_array_almost_equal(result, expected, decimal=1)

    def test_manhattan(self):
        result = manhattan(Array(
            data=[[1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3], [4, 4, 4, 4, 4], [5, 5, 5, 5, 5]])).to_numpy()
        expected = np.array([[0, 0, 0, 0, 0], [5, 0, 0, 0, 0], [10, 5, 0, 0, 0], [15, 10, 5, 0, 0], [20, 15, 10, 5, 0]])
        np.testing.assert_array_almost_equal(result, expected, decimal=2)


if __name__ == '__main__':
    unittest.main()
