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
from khiva.regularization import *
from khiva.array import Array


########################################################################################################################

class RegularizationTest(unittest.TestCase):
    DELTA = 1e-6
    DECIMAL = 6

    def setUp(self):
        pass

    def test_group_by_single_column(self):
        group_by_result = group_by(Array([[0, 1, 1, 2, 2, 3], [0, 3, 3, 1, 1, 2]]), 0).to_numpy()
        expected = [0, 3, 1, 2]
        np.testing.assert_array_almost_equal(group_by_result, expected, decimal=self.DECIMAL)

    def test_group_by_double_key_column(self):
        group_by_result = group_by(Array([[0, 1, 1, 2, 2, 3], [1, 2, 2, 3, 3, 4], [0, 3, 3, 1, 1, 2]]),
                                   0, 2, 1).to_numpy()
        expected = [0, 3, 1, 2]
        np.testing.assert_array_almost_equal(group_by_result, expected, decimal=self.DECIMAL)

    def test_group_by_double_key_column_2(self):
        group_by_result = group_by(Array([[0, 0, 1, 1, 1], [0, 1, 0, 0, 1], [1, 2, 3, 4, 5]]),
                                   0, 2, 1).to_numpy()
        expected = [1, 2, 3.5, 5]
        np.testing.assert_array_almost_equal(group_by_result, expected, decimal=self.DECIMAL)

    def test_group_by_double_key_double_value_column(self):
        group_by_result = group_by(Array([[0, 0, 0, 2, 2], [2, 2, 2, 4, 4], [0, 1, 2, 3, 4], [1, 1, 1, 1, 1]]),
                                   0, 2, 2).to_numpy()
        expected = [[1, 3.5], [1, 1]]
        np.testing.assert_array_almost_equal(group_by_result, expected, decimal=self.DECIMAL)


if __name__ == '__main__':
    unittest.main()
