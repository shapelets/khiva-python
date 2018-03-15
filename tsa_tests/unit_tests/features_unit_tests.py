"""
Copyright (c) 2018 Grumpy Cat Software S.L.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
from tsa.algorithms.features import *


########################################################################################################################

class FeatureTest(unittest.TestCase):
    DELTA = 1e-9

    def setUp(self):
        pass

    def test_cid_ce(self):
        cid_ce_result = cid_ce([[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]], False)
        self.assertAlmostEqual(cid_ce_result[0], 2.23606797749979, delta=self.DELTA)
        self.assertAlmostEqual(cid_ce_result[1], 2.23606797749979, delta=self.DELTA)

        cid_ce_result = cid_ce([[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]], True)
        self.assertAlmostEqual(cid_ce_result[0], 1.30930734141595, delta=self.DELTA)
        self.assertAlmostEqual(cid_ce_result[1], 1.30930734141595, delta=self.DELTA)

    def test_c3(self):
        c3_result = c3([[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]], 2)
        self.assertEqual(c3_result[0], 7.5)
        self.assertEqual(c3_result[1], 586.5)

    def test_abs_sum_of_changes(self):
        abs_sum_of_changes_result = absolute_sum_of_changes([[0, 1, 2, 3], [4, 6, 8, 10], [11, 14, 17, 20]])
        self.assertEqual(abs_sum_of_changes_result[0], 3)
        self.assertEqual(abs_sum_of_changes_result[1], 6)
        self.assertEqual(abs_sum_of_changes_result[2], 9)

    def test_absolute_sum_of_changes(self):
        abs_energy_result = abs_energy([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
        self.assertAlmostEqual(abs_energy_result, 385, delta=0.00000001)


if __name__ == '__main__':
    unittest.main()
