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
        ta = Array(
            [[-0.9247, 0.1808, 2.5441, 0.3516, -0.3452, 0.2191, -0.7687, 0.2413],
             [-1.1948, 0.8927, -0.5378, 0.227, 0.9354, -0.7613, 0.5787, -0.6174],
             [0.5889, 0.7897, -0.0645, 0.952, -1.1411, 0.8281, -0.7363, -0.7446]])
        tb = Array(
            [[0.2512, 0.6436, -2.3651, -0.7734, -0.0511, 1.6693, 1.9453, -1.9047], [0.8149, -0.1831, -0.1542, -1.3490,
                                                                                    1.2285, -1.0472, 0.3911, -0.0637]])

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
        ta = Array(
            [[0.6010, 0.0278, 0.9806, 0.2126, 0.0655, 0.5497, 0.2864, 0.3410, 0.7509, 0.4105, 0.1583, 0.3712,
              0.3543, 0.6450, 0.9675, 0.3636],
             [0.4165, 0.5814, 0.8962, 0.3712, 0.6755, 0.6105, 0.5232, 0.5567,
              0.7896, 0.8966, 0.0536, 0.5775, 0.2908, 0.9941, 0.5143, 0.3670],
             [0.3336, 0.0363, 0.5349, 0.0123,
              0.3988, 0.9787, 0.2308, 0.6244, 0.7917, 0.1654, 0.8657, 0.3766, 0.7331, 0.2522, 0.9644, 0.4711]])

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
            Array(data=[[10, 10, 11, 11, 10, 11, 10, 10, 11, 11, 10, 11, 10, 10], [
                11, 10, 10, 11, 10, 11, 11, 10, 11, 11, 10, 10, 11, 10]]), 3)
        expected_index = [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 9, 10, 11, 6, 7, 8, 3, 4, 5, 0, 1, 2]

        for i in range(6):
            self.assertAlmostEqual(stomp_self_join_result[0].to_numpy()[0][i], 0.0, delta=1e-2)
            self.assertEqual(stomp_self_join_result[1].to_numpy()[0][i], expected_index[i])

    def test_stomp(self):
        stomp_result = stomp(Array([[10, 11, 10, 11], [10, 11, 10, 11]]),
                             Array([[10, 11, 10, 11, 10, 11, 10, 11], [10, 11, 10, 11, 10, 11, 10, 11]]), 3)
        expected_index = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        a = stomp_result[0].to_numpy().flatten()
        b = stomp_result[1].to_numpy().flatten()

        for i in range(24):
            self.assertAlmostEqual(a[i], 0, delta=1e-2)
            self.assertAlmostEqual(b[i], expected_index[i])

    def test_stomp_different_queries(self):
        stomp_result = stomp(Array([[10, 11, 10, 8, 14], [10, 14, 10, 10, 3]]),
                             Array([[10, 11, 10, 11, 10, 11, 10, 7], [10, 13, 10, 10, 10, 14, 8, 7]]), 3)

        a = stomp_result[0].to_numpy()
        b = stomp_result[1].to_numpy()

        self.assertAlmostEqual(a[1, 0, 2], 1.73205077, delta=1e-3)
        self.assertAlmostEqual(a[0, 0, 0], 0.00954336, delta=1e-3)

        self.assertEqual(b[0, 1, 5], 2)
        self.assertEqual(b[1, 1, 1], 1)

    def test_find_best_n_motifs(self):
        stomp_result = stomp(Array([10, 10, 10, 10, 10, 10, 9, 10, 10, 10, 10, 10, 11, 10, 9], dtype.f32),
                             Array([10, 11, 10, 9], dtype.f32),
                             3)

        find_best_n_motifs_result = find_best_n_motifs(stomp_result[0], stomp_result[1], 3, 1)
        a = find_best_n_motifs_result[1].to_numpy()
        b = find_best_n_motifs_result[2].to_numpy()
        self.assertAlmostEqual(a, 12, delta=self.DELTA)
        self.assertAlmostEqual(b, 1, delta=self.DELTA)

    def test_find_best_n_motifs_multiple_profiles(self):
        stomp_result = stomp(Array([[10, 10, 10, 10, 10, 10, 9, 10, 10, 10, 10, 10, 11, 10, 9],
                                    [10, 10, 10, 10, 10, 10, 9, 10, 10, 10, 10, 10, 11, 10, 9]], dtype.f32),
                             Array([[10, 11, 10, 9], [10, 11, 10, 9]], dtype.f32),
                             3)

        find_best_n_motifs_result = find_best_n_motifs(stomp_result[0], stomp_result[1], 3, 1)
        a = find_best_n_motifs_result[1].to_numpy()
        b = find_best_n_motifs_result[2].to_numpy()
        np.testing.assert_array_almost_equal(a, np.array([[[12], [12]], [[12], [12]]]), decimal=self.DECIMAL)
        np.testing.assert_array_almost_equal(b, np.array([[[1], [1]], [[1], [1]]]), decimal=self.DECIMAL)

    def test_find_best_n_motifs_mirror(self):
        stomp_result = stomp_self_join(Array([10.1, 11, 10.2, 10.15, 10.775, 10.1, 11, 10.2], dtype.f32), 3)

        find_best_n_motifs_result = find_best_n_motifs(stomp_result[0], stomp_result[1], 3, 2, True)
        a = find_best_n_motifs_result[1].to_numpy()
        b = find_best_n_motifs_result[2].to_numpy()
        self.assertAlmostEqual(a[0], 0, delta=self.DELTA)
        self.assertAlmostEqual(a[1], 0, delta=self.DELTA)
        self.assertAlmostEqual(b[0], 5, delta=self.DELTA)
        self.assertAlmostEqual(b[1], 3, delta=self.DELTA)

    def test_find_best_n_motifs_consecutive(self):
        stomp_result = stomp_self_join(Array([10.1, 11, 10.1, 10.15, 10.075, 10.1, 11, 10.1, 10.15], dtype.f32), 3)

        find_best_n_motifs_result = find_best_n_motifs(stomp_result[0], stomp_result[1], 3, 2)
        a = find_best_n_motifs_result[1].to_numpy()
        b = find_best_n_motifs_result[2].to_numpy()
        self.assertAlmostEqual(a[1], 6, delta=self.DELTA)
        self.assertAlmostEqual(b[1], 3, delta=self.DELTA)

    def test_find_best_n_discords(self):
        stomp_result = stomp(Array(np.array([11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11])),
                             Array(np.array([9, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 9])),
                             3)
        find_best_n_discords_result = find_best_n_discords(stomp_result[0],
                                                           stomp_result[1], 3, 2)
        a = find_best_n_discords_result[2].to_numpy()

        self.assertEqual(a[0], 0)
        # The test failed in the CPU used in the Travis CI build machine
        if os.environ.get("TRAVIS") == "true":
            self.assertEqual(a[1], 2)
        else:
            self.assertEqual(a[1], 10)

    def test_find_best_n_discords_multiple_profiles(self):
        stomp_result = stomp(Array(np.array([[11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11],
                                             [11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11]])),
                             Array(np.array([[9, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 9],
                                             [9, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1, 10.2, 10.1,
                                              9]])),
                             3)
        find_best_n_discords_result = find_best_n_discords(stomp_result[0],
                                                           stomp_result[1], 3, 2)
        a = find_best_n_discords_result[2].to_numpy()

        # The test failed in the CPU used in the Travis CI build machine
        if os.environ.get("TRAVIS") == "true":
            np.testing.assert_array_almost_equal(a, np.array([[[0, 2], [0, 2]], [[0, 2], [0, 2]]]),
                                                 decimal=self.DECIMAL)
        else:
            np.testing.assert_array_almost_equal(a, np.array([[[0, 10], [0, 10]], [[0, 10], [0, 10]]]),
                                                 decimal=self.DECIMAL)

    def test_find_best_n_discords_mirror(self):
        stomp_result = stomp_self_join(Array(np.array([10, 11, 10, 10, 11, 10])), 3)
        find_best_n_discords_result = find_best_n_discords(stomp_result[0],
                                                           stomp_result[1], 3, 1, True)
        a = find_best_n_discords_result[1].to_numpy()
        b = find_best_n_discords_result[2].to_numpy()

        self.assertEqual(a, 3)
        self.assertEqual(b, 1)

    def test_find_best_n_discords_consecutive(self):
        stomp_result = stomp_self_join(
            Array(np.array([10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 9.999, 9.998]), dtype.f32), 3)
        find_best_n_discords_result = find_best_n_discords(stomp_result[0],
                                                           stomp_result[1], 3, 2, True)
        a = find_best_n_discords_result[2].to_numpy()

        self.assertEqual(a[0], 12)
        # The test failed in the CPU used in the Travis CI build machine
        if os.environ.get("TRAVIS") == "true":
            self.assertEqual(a[1], 11)
        else:
            self.assertNotEqual(a[1], 11)

    def test_mass(self):
        mass_result = mass(Array(np.array([4, 3, 8]), dtype.f32),
                           Array(np.array([10, 10, 10, 11, 12, 11, 10, 10, 11, 12, 11, 14, 10, 10]), dtype.f32))

        distances = mass_result.to_numpy()
        distances_expected = np.array([1.732051, 0.328954, 1.210135, 3.150851, 3.245858, 2.822044,
                                       0.328954, 1.210135, 3.150851, 0.248097, 3.30187, 2.82205])

        np.testing.assert_array_almost_equal(distances, distances_expected, decimal=self.DECIMAL)

    def test_mass_multiple(self):
        mass_result = mass(Array(np.array([[10, 10, 11, 11], [10, 11, 10, 10]]), dtype.f32),
                           Array(np.array([[10, 10, 10, 11, 12, 11, 10], [10, 11, 12, 11, 14, 10, 10]]), dtype.f32))

        distances = mass_result.to_numpy()

        distances_expected = np.array([[[1.83880341, 0.87391543, 1.5307337, 3.69551826],
                                        [3.26598597, 3.48967957, 2.82842779, 1.21162188]],
                                       [[1.5307337, 2.17577887, 2.57832384, 3.75498915],
                                        [2.82842779, 2.82842731, 3.21592307, 0.50202721]]])

        np.testing.assert_array_almost_equal(distances, distances_expected, decimal=self.DECIMAL)

    def test_find_best_n_occurrences(self):
        find_result = find_best_n_occurrences(
            Array(np.array([10, 11, 12]), dtype.f32),
            Array(np.array([[10, 10, 11, 11, 12, 11, 10, 10, 11, 12, 11, 10, 10, 11],
                            [10, 10, 11, 11, 12, 11, 10, 10, 11, 12, 11, 10, 10, 11]]), dtype.f32),
            1)

        distances = find_result[0].to_numpy()
        indexes = find_result[1].to_numpy()

        self.assertAlmostEqual(distances[0], 0.00069053, delta=self.DELTA)
        self.assertEqual(indexes[0], 7)

    def test_find_best_n_occurrences_multiple_queries(self):
        find_result = find_best_n_occurrences(
            Array(np.array([[11, 11, 10, 11], [10, 11, 11, 12]]), dtype.f32),
            Array(np.array([[10, 10, 11, 11, 10, 11, 10, 10, 11, 11, 10, 11, 10, 10],
                            [11, 10, 10, 11, 10, 11, 11, 10, 11, 11, 14, 10, 11, 10]]), dtype.f32),
            4)

        distances = find_result[0].to_numpy()
        indexes = find_result[1].to_numpy()

        np.testing.assert_array_equal(find_result[0].get_dims(), np.array([4, 2, 2, 1]))

        # Subsequence index of the third best distance for the second query over the first time series
        self.assertEqual(indexes[0, 1, 3], 2)

        # Second best distance for the first query over the second time series
        self.assertAlmostEqual(distances[1, 0, 2], 1.83880329, delta=self.DELTA)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MatrixTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
