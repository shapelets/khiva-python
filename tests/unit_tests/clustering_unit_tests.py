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
from khiva.clustering import *
from khiva.array import Array
import numpy as np
from khiva.library import set_backend, KHIVABackend


########################################################################################################################

class ClusteringTest(unittest.TestCase):
    DELTA = 1e-3
    DECIMAL = 3

    def setUp(self):
        set_backend(KHIVABackend.KHIVA_BACKEND_CPU)

    def test_kmeans(self):
        tss = Array([[0.0,   1.0,  2.0,  3.0],
                     [6.0,   7.0,  8.0,  9.0],
                     [2.0,  -2.0,  4.0, -4.0],
                     [8.0,   5.0,  3.0,  1.0],
                     [15.0, 10.0,  5.0,  0.0],
                     [7.0,  -7.0,  1.0, -1.0]])

        expected_c = np.array([[0.0, 0.1667, 0.3333, 0.5],
                               [1.5, -1.5, 0.8333, -0.8333],
                               [4.8333, 3.6667, 2.6667, 1.6667]])

        result = k_means(tss, 3)
        result_c = result[0].to_numpy()

        for i in range(0, 4):
            self.assertAlmostEqual(result_c[0, i] + result_c[1, i] +
                                   result_c[2, i],
                                   expected_c[0, i] +
                                   expected_c[1, i] +
                                   expected_c[2, i], delta=self.DELTA)

    def test_k_shape(self):
        tss = Array([[1.0,   2.0,   3.0,  4.0,  5.0,  6.0, 7.0],
                     [0.0,  10.0,   4.0,  5.0,  7.0, -3.0, 0.0],
                     [-1.0, 15.0, -12.0,  8.0,  9.0,  4.0, 5.0],
                     [2.0,   8.0,   7.0, -6.0, -1.0,  2.0, 9.0],
                     [-5.0, -5.0,  -6.0,  7.0,  9.0,  9.0, 0.0]])

        expected_c = np.array([[-0.5234, 0.1560, -0.3627, -1.2764, -0.7781,  0.9135,  1.8711],
                               [-0.7825, 1.5990,  0.1701,  0.4082,  0.8845, -1.4969, -0.7825],
                               [-0.6278, 1.3812, -2.0090,  0.5022,  0.6278,  0.0000,  0.1256]])
        expected_l = np.array([0, 1, 2, 0, 0])

        (centroids, labels) = k_shape(tss, 3)
        centr = centroids.to_numpy()
        lab = labels.to_numpy()
        np.testing.assert_array_almost_equal(centr, expected_c, decimal=self.DECIMAL)
        np.testing.assert_array_almost_equal(lab, expected_l, decimal=self.DECIMAL)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ClusteringTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
