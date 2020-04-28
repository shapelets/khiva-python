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
import os
from khiva.matrix import *
from khiva.array import *
from khiva.library import set_backend, KHIVABackend


########################################################################################################################

class MatrixTest(unittest.TestCase):
    DELTA = 1e-6
    DECIMAL = 6

    def setUp(self):
        set_backend(KHIVABackend.KHIVA_BACKEND_CPU)

    def test_matrix_profile(self):
        ta = Array.from_list(
            [[-0.9247, 0.1808, 2.5441, 0.3516, -0.3452, 0.2191, -0.7687, 0.2413],
             [-1.1948, 0.8927, -0.5378, 0.227, 0.9354, -0.7613, 0.5787, -0.6174],
             [0.5889, 0.7897, -0.0645, 0.952, -1.1411, 0.8281, -0.7363, -0.7446]], dtype.f32)
        tb = Array.from_list(
            [[0.2512, 0.6436, -2.3651, -0.7734, -0.0511, 1.6693, 1.9453, -1.9047], [0.8149, -0.1831, -0.1542, -1.3490,
                                                                                    1.2285, -1.0472, 0.3911, -0.0637]], dtype.f32)

        res = matrix_profile(ta, tb, 3)
        distances = res[0].to_numpy()
        indexes = res[1].to_numpy()
        np.testing.assert_array_equal([2, 3, 6], distances.shape)
        np.testing.assert_array_equal([2, 3, 6], indexes.shape)

        distances = distances.flatten()
        indexes = indexes.flatten()
        self.assertAlmostEqual(0.0112, distances[7], delta=1e-3)
        self.assertEqual(1, indexes[7])
        self.assertAlmostEqual(0.2810, distances[17], delta=1e-3)
        self.assertEqual(0, indexes[17])
        self.assertAlmostEqual(0.4467, distances[18], delta=1e-3)
        self.assertEqual(2, indexes[18])
        self.assertAlmostEqual(0.0162, distances[27], delta=1e-3)
        self.assertEqual(5, indexes[27])
        self.assertAlmostEqual(0.9187, distances[35], delta=1e-3)
        self.assertEqual(4, indexes[35])

    def test_matrix_profile_self_join(self):
        ta = Array.from_list(
            [[0.6010, 0.0278, 0.9806, 0.2126, 0.0655, 0.5497, 0.2864, 0.3410, 0.7509, 0.4105, 0.1583, 0.3712,
              0.3543, 0.6450, 0.9675, 0.3636],
             [0.4165, 0.5814, 0.8962, 0.3712, 0.6755, 0.6105, 0.5232, 0.5567,
              0.7896, 0.8966, 0.0536, 0.5775, 0.2908, 0.9941, 0.5143, 0.3670],
             [0.3336, 0.0363, 0.5349, 0.0123,
              0.3988, 0.9787, 0.2308, 0.6244, 0.7917, 0.1654, 0.8657, 0.3766, 0.7331, 0.2522, 0.9644, 0.4711]], dtype.f32)

        res = matrix_profile_self_join(ta, 6)
        distances = res[0].to_numpy()
        indexes = res[1].to_numpy()
        np.testing.assert_array_equal([3, 11], distances.shape)
        np.testing.assert_array_equal([3, 11], indexes.shape)

        distances = distances.flatten()
        indexes = indexes.flatten()
        self.assertAlmostEqual(1.2237, distances[7], delta=1e-3)
        self.assertEqual(1, indexes[7])
        self.assertAlmostEqual(2.5324, distances[21], delta=1e-3)
        self.assertEqual(1, indexes[21])
        self.assertAlmostEqual(1.979, distances[25], delta=1e-3)
        self.assertEqual(6, indexes[25])

    def test_stomp_self_join(self):
        stomp_self_join_result = stomp_self_join(
            Array.from_list([[10, 10, 11, 11, 10, 11, 10, 10, 11, 11, 10, 11, 10, 10], [
                11, 10, 10, 11, 10, 11, 11, 10, 11, 11, 10, 10, 11, 10]], dtype.f32), 3)
        expected_index = [6, 7, 8, 9, 10, 11, 0, 1, 2, 3,
                          4, 5, 9, 10, 11, 6, 7, 8, 3, 4, 5, 0, 1, 2]

        for i in range(6):
            self.assertAlmostEqual(stomp_self_join_result[0].to_numpy()[0][i], 0.0, delta=1e-2)
            self.assertEqual(stomp_self_join_result[1].to_numpy()[0][i], expected_index[i])

    def test_stomp(self):
        stomp_result = stomp(Array.from_list([[10, 11, 10, 11], [10, 11, 10, 11]], dtype.f32),
                             Array.from_list([[10, 11, 10, 11, 10, 11, 10, 11], [10, 11, 10, 11, 10, 11, 10, 11]], dtype.f32),
                             3)
        expected_index = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        a = stomp_result[0].to_numpy().flatten()
        b = stomp_result[1].to_numpy().flatten()

        for i in range(24):
            self.assertAlmostEqual(a[i], 0, delta=1e-2)
            self.assertAlmostEqual(b[i], expected_index[i])

    def test_stomp_different_queries(self):
        stomp_result = stomp(Array.from_list([[10, 11, 10, 8, 14], [10, 14, 10, 10, 3]], dtype.f32),
                             Array.from_list([[10, 11, 10, 11, 10, 11, 10, 7], [10, 13, 10, 10, 10, 14, 8, 7]], dtype.f32), 3)

        a = stomp_result[0].to_numpy()
        b = stomp_result[1].to_numpy()

        self.assertAlmostEqual(a[1, 0, 2], 1.73205077, delta=1e-3)
        self.assertAlmostEqual(a[0, 0, 0], 0.00954336, delta=1e-3)

        self.assertEqual(b[0, 1, 5], 2)
        self.assertEqual(b[1, 1, 1], 1)

    def test_find_best_n_motifs(self):
        stomp_result = stomp(Array.from_list([10, 10, 10, 10, 10, 10, 9, 10, 10, 10, 10, 10, 11, 10, 9], dtype.f32),
                             Array.from_list([10, 11, 10, 9], dtype.f32),
                             3)

        find_best_n_motifs_result = find_best_n_motifs(
            stomp_result[0], stomp_result[1], 3, 1)
        a = find_best_n_motifs_result[1].to_numpy()
        b = find_best_n_motifs_result[2].to_numpy()
        self.assertAlmostEqual(a, 12, delta=self.DELTA)
        self.assertAlmostEqual(b, 1, delta=self.DELTA)

    def test_find_best_n_motifs_multiple_profiles(self):
        stomp_result = stomp(Array.from_list([[10, 10, 10, 10, 10, 10, 9, 10, 10, 10, 10, 10, 11, 10, 9],
                                    [10, 10, 10, 10, 10, 10, 9, 10, 10, 10, 10, 10, 11, 10, 9]], dtype.f32),
                             Array.from_list([[10, 11, 10, 9], [10, 11, 10, 9]], dtype.f32),
                             3)

        find_best_n_motifs_result = find_best_n_motifs(
            stomp_result[0], stomp_result[1], 3, 1)
        a = find_best_n_motifs_result[1].to_numpy()
        b = find_best_n_motifs_result[2].to_numpy()
        np.testing.assert_array_almost_equal(a, np.array(
            [[[12], [12]], [[12], [12]]]), decimal=self.DECIMAL)
        np.testing.assert_array_almost_equal(b, np.array(
            [[[1], [1]], [[1], [1]]]), decimal=self.DECIMAL)

    def test_find_best_n_motifs_mirror(self):
        stomp_result = stomp_self_join(
            Array.from_list([10.1, 11, 10.2, 10.15, 10.775, 10.1, 11, 10.2], dtype.f32), 3)

        find_best_n_motifs_result = find_best_n_motifs(
            stomp_result[0], stomp_result[1], 3, 2, True)
        a = find_best_n_motifs_result[1].to_numpy()
        b = find_best_n_motifs_result[2].to_numpy()
        self.assertAlmostEqual(a[0], 0, delta=self.DELTA)
        self.assertAlmostEqual(a[1], 0, delta=self.DELTA)
        self.assertAlmostEqual(b[0], 5, delta=self.DELTA)
        self.assertAlmostEqual(b[1], 3, delta=self.DELTA)

    def test_find_best_n_motifs_consecutive(self):
        stomp_result = stomp_self_join(
            Array.from_list([10.1, 11, 10.1, 10.15, 10.075, 10.1, 11, 10.1, 10.15], dtype.f32), 3)

        find_best_n_motifs_result = find_best_n_motifs(
            stomp_result[0], stomp_result[1], 3, 2, True)
        a = find_best_n_motifs_result[1].to_numpy()
        b = find_best_n_motifs_result[2].to_numpy()
        self.assertAlmostEqual(a[1], 6, delta=self.DELTA)
        self.assertAlmostEqual(b[1], 3, delta=self.DELTA)

    def test_find_best_n_discords(self):
        stomp_result = stomp(Array.from_numpy(np.array([11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11]), dtype.f32),
                             Array.from_numpy(np.array(
                                 [9, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 9]), dtype.f32),
                             3)
        find_best_n_discords_result = find_best_n_discords(stomp_result[0],
                                                           stomp_result[1], 3, 2)
        a = find_best_n_discords_result[2].to_numpy()

        self.assertEqual(a[0], 0)
        self.assertEqual(a[1], 10)

    def test_find_best_n_discords_multiple_profiles(self):
        stomp_result = stomp(Array.from_numpy(np.array([[11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11],
                                             [11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11]]), dtype.f32),
                             Array.from_numpy(np.array([[9, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 9],
                                             [9, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 9]]), dtype.f32),
                             3)
        find_best_n_discords_result = find_best_n_discords(stomp_result[0],
                                                           stomp_result[1], 3, 2)
        a = find_best_n_discords_result[2].to_numpy()
        np.testing.assert_array_almost_equal(a, np.array([[[0, 10], [0, 10]], [[0, 10], [0, 10]]]),
                                                 decimal=self.DECIMAL)

    def test_find_best_n_discords_mirror(self):
        stomp_result = stomp_self_join(
            Array.from_numpy(np.array([10, 11, 10, 10, 11, 10]), dtype.s32), 3)
        find_best_n_discords_result = find_best_n_discords(stomp_result[0],
                                                           stomp_result[1], 3, 1, True)
        a = find_best_n_discords_result[1].to_numpy()
        b = find_best_n_discords_result[2].to_numpy()

        self.assertEqual(a, 3)
        self.assertEqual(b, 1)

    def test_find_best_n_discords_consecutive(self):
        stomp_result = stomp_self_join(
            Array.from_numpy(np.array([10.0, 11.0, 14.0, 11.0, -2.0, 11.0, 18.0, 11.0, 1.0, 25.0, 10.0, 11.0, 1.0, 0.0, 19.0]), dtype.f32), 3)
        find_best_n_discords_result = find_best_n_discords(stomp_result[0],
                                                           stomp_result[1], 3, 2, True)
        a = find_best_n_discords_result.subsequence_indexes.to_numpy()

        self.assertEqual(a[0], 9)
        self.assertEqual(a[1], 3)

    def test_mass(self):
        mass_result = mass(Array.from_numpy(np.array([4, 3, 8]), dtype.f32),
                           Array.from_numpy(np.array([10, 10, 10, 11, 12, 11, 10, 10, 11, 12, 11, 14, 10, 10]), dtype.f32))

        distances = mass_result.to_numpy()
        distances_expected = np.array([1.732051, 0.328954, 1.210135, 3.150851, 3.245858, 2.822044,
                                       0.328954, 1.210135, 3.150851, 0.248097, 3.30187, 2.82205])

        np.testing.assert_array_almost_equal(
            distances, distances_expected, decimal=self.DECIMAL)

    def test_mass_multiple(self):
        mass_result = mass(Array.from_numpy(np.array([[10, 10, 11, 11], [10, 11, 10, 10]]), dtype.f32),
                           Array.from_numpy(np.array([[10, 10, 10, 11, 12, 11, 10], [10, 11, 12, 11, 14, 10, 10]]), dtype.f32))

        distances = mass_result.to_numpy()

        distances_expected = np.array([[[1.83880341, 0.87391543, 1.5307337, 3.69551826],
                                        [3.26598597, 3.48967957, 2.82842779, 1.21162188]],
                                       [[1.5307337, 2.17577887, 2.57832384, 3.75498915],
                                        [2.82842779, 2.82842731, 3.21592307, 0.50202721]]])

        np.testing.assert_array_almost_equal(
            distances, distances_expected, decimal=self.DECIMAL)

    def test_find_best_n_occurrences(self):
        find_result = find_best_n_occurrences(
            Array.from_numpy(np.array([10, 11, 12]), dtype.f32),
            Array.from_numpy(np.array([[10, 10, 11, 11, 12, 11, 10, 10, 11, 12, 11, 10, 10, 11],
                            [10, 10, 11, 11, 12, 11, 10, 10, 11, 12, 11, 10, 10, 11]]), dtype.f32),
            1)

        distances = find_result[0].to_numpy()
        indexes = find_result[1].to_numpy()

        self.assertAlmostEqual(distances[0], 0.00069053, delta=self.DELTA)
        self.assertEqual(indexes[0], 7)

    def test_find_best_n_occurrences_multiple_queries(self):
        find_result = find_best_n_occurrences(
            Array.from_numpy(np.array([[11, 11, 10, 11], [10, 11, 11, 12]]), dtype.f32),
            Array.from_numpy(np.array([[10, 10, 11, 11, 10, 11, 10, 10, 11, 11, 10, 11, 10, 10],
                            [11, 10, 10, 11, 10, 11, 11, 10, 11, 11, 14, 10, 11, 10]]), dtype.f32),
            4)

        distances = find_result[0].to_numpy()
        indexes = find_result[1].to_numpy()

        np.testing.assert_array_equal(
            find_result[0].get_dims(), np.array([4, 2, 2, 1]))

        # Subsequence index of the third best distance for the second query over the first time series
        self.assertEqual(indexes[0, 1, 3], 2)

        # Second best distance for the first query over the second time series
        self.assertAlmostEqual(
            distances[1, 0, 2], 1.83880329, delta=self.DELTA)

    def test_get_chains(self):
        tss = Array.from_list([
            -92.4662, 18.0826, 254.4097, 35.1582, -
            34.5167, 21.9123, -76.8666, 24.1255, -119.4840, 89.2692,
            -53.7780, 22.6983, 93.5360, -76.1285, 57.8707, -
            61.7367, 58.8945, 78.9682, -6.4519, 95.2034,
            -114.1063, 82.8133, -73.6341, -74.4575, -
            84.1459, 129.9067, 8.8310, 65.8802, -27.8835, 141.4345,
            -116.4987, -66.2915, -58.0665, -16.9934, -72.6471, -
            15.0601, -27.8524, -0.6336, 40.2054, 139.2524,
            -24.1727, 11.3927, -162.7895, 14.8781, 25.1250, 64.3562, -
            236.5118, -77.3420, -5.1106, 166.9285,
            194.5296, -190.4659, 81.4878, -18.3076, -15.4175, -
            134.8966, 122.8539, -104.7209, 39.1123, -6.3669,
            -125.9402, -226.7495, 71.6115, -255.7238, 73.6051, 14.0193, -
            9.0993, 32.4544, -109.1953, 87.6599,
            121.1325, -8.6135, -49.1869, -134.8533, -
            139.3240, 118.1974, 22.9832, 63.0970, -93.4303, -193.2919,
            -43.6712, -4.2870, -93.5555, -86.3817, -
            26.6190, 94.3234, -100.8066, 70.5622, 75.9013, 36.3536,
            -138.5388, 72.8221, -145.1508, 73.7886, -
            1.6499, 24.0054, 113.4099, 7.9198, 77.7093, 33.7550,
            -68.3262, -126.4960, 120.4121, -181.5796, -
            110.4838, 88.8343, -256.1250, 3.1551, 125.7766, -76.7836,
            0.5753, -25.1363, 49.2497, -74.0528, -100.8634, -
            56.5037, -75.5141, -7.2044, -51.6655, -116.6414,
            182.3497, -152.1112, 150.9720, 77.0329, 58.4420, 50.0252, -36.1718, -55.2495
        ], dtype.f32)

        chain_values = [
            [18, 28, 76, 111], [27, 75, 110], [16, 53, 82], [
                26, 74, 109], [6, 59, 88], [7, 60, 89], [8, 61, 90],
            [9, 62, 105], [15, 46, 92], [29, 77, 112], [31, 79, 114], [
                38, 64, 70], [17, 48], [19, 50], [23, 106],
            [24, 107], [25, 108], [0, 47], [2, 49], [5, 10], [14, 91], [
                51, 80], [52, 81], [54, 83], [55, 84], [56, 85],
            [57, 86], [58, 87], [65, 71], [67, 73], [78, 113], [93, 96], [94, 97], [95, 98]]

        chain_indexes = np.array([
            1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10,
            10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19,
            19, 20, 20, 21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29,
            30, 30, 31, 31, 32, 32, 33, 33, 34, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ])

        chains_result = get_chains(tss, 12).to_numpy()
        chain_values_result = set(chains_result[0, :].tolist())
        for chain in chain_values:
            self.assertTrue(set(chain) <= chain_values_result)

        np.testing.assert_array_equal(chain_indexes, chains_result[1, :])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MatrixTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
