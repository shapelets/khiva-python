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
    DELTA = 1e-6

    def setUp(self):
        pass

    def test_cid_ce(self):
        cid_ce_result = cid_ce(np.array([[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]), False)
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

    def test_abs_energy(self):
        abs_energy_result = abs_energy([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
        self.assertAlmostEqual(abs_energy_result, 385, delta=self.DELTA)

    def test_abs_energy(self):
        abs_energy_result = abs_energy([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
        self.assertAlmostEqual(abs_energy_result, 385, delta=self.DELTA)

    def test_cross_correlation(self):
        cross_correlation_result = cross_correlation([[1, 2, 3, 4]], [[4, 6, 8, 10, 12]], False)

        self.assertAlmostEqual(cross_correlation_result[0], 0.790569415, delta=self.DELTA)
        self.assertAlmostEqual(cross_correlation_result[1], 0.790569415, delta=self.DELTA)
        self.assertAlmostEqual(cross_correlation_result[2], 0.079056941, delta=self.DELTA)
        self.assertAlmostEqual(cross_correlation_result[3], -0.395284707, delta=self.DELTA)
        self.assertAlmostEqual(cross_correlation_result[4], -0.474341649, delta=self.DELTA)

    def test_auto_covariance(self):
        auto_covariance_result = auto_covariance([[0, 1, 2, 3], [10, 11, 12, 13]], False)

        self.assertAlmostEqual(auto_covariance_result[0], 1.25, self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[1], 0.3125, self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[2], -0.375, self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[3], -0.5625, self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[4], 1.25, self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[5], 0.3125, self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[6], -0.375, self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[7], -0.5625, self.DELTA)

    def test_cross_covariance(self):
        cross_covariance_result = cross_covariance([[0, 1, 2, 3], [10, 11, 12, 13]],
                                                   [[4, 6, 8, 10, 12], [14, 16, 18, 20, 22]], False)

        for i in range(4):
            self.assertAlmostEqual(cross_covariance_result[(i * 5)], 2.5, delta=self.DELTA)
            self.assertAlmostEqual(cross_covariance_result[(i * 5) + 1], 2.5, delta=self.DELTA)
            self.assertAlmostEqual(cross_covariance_result[(i * 5) + 2], 0.25, delta=self.DELTA)
            self.assertAlmostEqual(cross_covariance_result[(i * 5) + 3], -1.25, delta=self.DELTA)
            self.assertAlmostEqual(cross_covariance_result[(i * 5) + 4], -1.5, delta=self.DELTA)

    def test_approximate_entropy(self):

        approximate_entropy_result = approximate_entropy(
            [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]], 4, 0.5)

        self.assertAlmostEqual(approximate_entropy_result[0], 0.13484281753639338, delta=self.DELTA)
        self.assertAlmostEqual(approximate_entropy_result[1], 0.13484281753639338, delta=self.DELTA)

    def test_cross_correlation(self):
        cross_correlation_result = cross_correlation([[1, 2, 3, 4]], [[4, 6, 8, 10, 12]], False)

        self.assertAlmostEqual(cross_correlation_result[0], 0.790569415, delta=self.DELTA)
        self.assertAlmostEqual(cross_correlation_result[1], 0.790569415, delta=self.DELTA)
        self.assertAlmostEqual(cross_correlation_result[2], 0.079056941, delta=self.DELTA)
        self.assertAlmostEqual(cross_correlation_result[3], -0.395284707, delta=self.DELTA)
        self.assertAlmostEqual(cross_correlation_result[4], -0.474341649, delta=self.DELTA)

    def test_auto_covariance(self):
        auto_covariance_result = auto_covariance([[0, 1, 2, 3], [10, 11, 12, 13]], False)

        self.assertAlmostEqual(auto_covariance_result[0], 1.25, delta=self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[1], 0.3125, delta=self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[2], -0.375, delta=self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[3], -0.5625, delta=self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[4], 1.25, delta=self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[5], 0.3125, delta=self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[6], -0.375, delta=self.DELTA)
        self.assertAlmostEqual(auto_covariance_result[7], -0.5625, delta=self.DELTA)

    def test_cross_covariance(self):
        cross_covariance_result = cross_covariance([[0, 1, 2, 3], [10, 11, 12, 13]],
                                                   [[4, 6, 8, 10, 12], [14, 16, 18, 20, 22]], False)

        for i in range(4):
            self.assertAlmostEqual(cross_covariance_result[(i * 5)], 2.5, delta=self.DELTA)
            self.assertAlmostEqual(cross_covariance_result[(i * 5) + 1], 2.5, delta=self.DELTA)
            self.assertAlmostEqual(cross_covariance_result[(i * 5) + 2], 0.25, delta=self.DELTA)
            self.assertAlmostEqual(cross_covariance_result[(i * 5) + 3], -1.25, delta=self.DELTA)
            self.assertAlmostEqual(cross_covariance_result[(i * 5) + 4], -1.5, delta=self.DELTA)

    def test_auto_correlation(self):
        auto_correlation_result = auto_correlation([[0, 1, 2, 3], [10, 11, 12, 13]], 4, False)
        self.assertAlmostEqual(auto_correlation_result[0], 1, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[1], 0.25, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[2], -0.3, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[3], -0.45, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[4], 1.0, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[5], 0.25, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[6], -0.3, delta=self.DELTA)
        self.assertAlmostEqual(auto_correlation_result[7], -0.45, delta=self.DELTA)

    def test_binned_entropy(self):
        binned_entropy_result = binned_entropy([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                                                 14, 15, 16, 17, 18, 19, 20],
                                                [1, 1, 3, 10, 5, 6, 1, 8, 9, 10, 11, 1, 13, 14, 10, 16, 17, 10, 19,
                                                 20]], 5)
        self.assertAlmostEqual(binned_entropy_result[0], 1.6094379124341005, delta=self.DELTA)
        self.assertAlmostEqual(binned_entropy_result[1], 1.5614694247763998, delta=self.DELTA)

    def test_count_above_mean(self):
        count_above_mean_result = count_above_mean([[0, 1, 2, 3, 4, 5],
                                                    [6, 7, 8, 9, 10, 11]])
        self.assertAlmostEqual(count_above_mean_result[0], 3, delta=self.DELTA)
        self.assertAlmostEqual(count_above_mean_result[1], 3, delta=self.DELTA)

    def test_count_below_mean(self):
        count_below_mean_result = count_below_mean([[0, 1, 2, 3, 4, 5],
                                                    [6, 7, 8, 9, 10, 11]])
        self.assertAlmostEqual(count_below_mean_result[0], 3, delta=self.DELTA)
        self.assertAlmostEqual(count_below_mean_result[1], 3, delta=self.DELTA)

    def test_energy_ratio_by_chunks(self):
        energy_ratio_by_chunks_result = energy_ratio_by_chunks([[0, 1, 2, 3, 4, 5],
                                                                [6, 7, 8, 9, 10, 11]], 2, 0)
        self.assertAlmostEqual(energy_ratio_by_chunks_result[0], 0.090909091, delta=self.DELTA)
        self.assertAlmostEqual(energy_ratio_by_chunks_result[1], 0.330376940, delta=self.DELTA)
        energy_ratio_by_chunks_result = energy_ratio_by_chunks([[0, 1, 2, 3, 4, 5],
                                                                [6, 7, 8, 9, 10, 11]], 2, 1)
        self.assertAlmostEqual(energy_ratio_by_chunks_result[0], 0.909090909, delta=self.DELTA)
        self.assertAlmostEqual(energy_ratio_by_chunks_result[1], 0.669623060, delta=self.DELTA)


if __name__ == '__main__':
    unittest.main()
