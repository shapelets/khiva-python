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
from khiva.dimensionality import *
from khiva.array import Array
import numpy as np
from khiva.library import set_backend, KHIVABackend


########################################################################################################################


class DimensionalityTest(unittest.TestCase):
    DELTA = 1e-6
    DECIMAL = 6

    def setUp(self):
        set_backend(KHIVABackend.KHIVA_BACKEND_CPU)

    def test_ramer_douglas_peucker(self):
        a = Array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 0.1, -0.1, 5.0, 6.0, 7.0, 8.1, 9.0, 9.0, 9.0]])
        ramer_douglas_peucker_result = ramer_douglas_peucker(a, 1.0).to_numpy()
        expected = np.array([[0, 2, 3, 6, 9], [0, -0.1, 5.0, 8.1, 9.0]])
        np.testing.assert_array_almost_equal(ramer_douglas_peucker_result, expected, decimal=self.DECIMAL)

    def test_visvalingam(self):
        a = Array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 0.1, -0.1, 5.0, 6.0, 7.0, 8.1, 9.0, 9.0, 9.0]])
        visvalingam_result = visvalingam(a, 5).to_numpy()
        expected = np.array([[0, 2, 5, 7, 9], [0, -0.1, 7.0, 9.0, 9.0]])
        np.testing.assert_array_almost_equal(visvalingam_result, expected, decimal=self.DECIMAL)

    def test_paa(self):
        a = Array(
            [[0.0, 0.1, -0.1, 5.0, 6.0, 7.0, 8.1, 9.0, 9.0, 9.0],
             [0.0, 0.1, -0.1, 5.0, 6.0, 7.0, 8.1, 9.0, 9.0, 9.0]])
        paa_result = paa(a, 5).to_numpy()
        expected = np.array([[0.05, 2.45, 6.5, 8.55, 9.0], [0.05, 2.45, 6.5, 8.55, 9.0]])
        np.testing.assert_array_almost_equal(paa_result, expected, decimal=self.DECIMAL)

    def test_sax(self):
        a = Array([[0.05, 2.45, 6.5, 8.55, 9.0], [0.05, 2.45, 6.5, 8.55, 9.0]])
        sax_result = sax(a, 3).to_numpy()

        expected = np.array([[0, 0, 1, 2, 2], [0, 0, 1, 2, 2]], dtype=np.int32)
        np.testing.assert_array_almost_equal(sax_result, expected, decimal=self.DECIMAL)

    def test_pip(self):
        a = Array(
            [[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0], [0.0, 0.1, -0.1, 5.0, 6.0, 7.0, 8.1, 9.0, 9.0, 9.0]])
        pip_result = pip(a, 6).to_numpy()

        expected = np.array([[0.0, 2.0, 3.0, 6.0, 7.0, 9.0], [0.0, -0.1, 5.0, 8.1, 9.0, 9.0]])
        np.testing.assert_array_almost_equal(pip_result, expected, decimal=self.DECIMAL)

    def test_pla_bottom_up(self):
        tss = Array([[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
                     [0.0, 0.1, -0.1, 5.0, 6.0, 7.0, 8.1, 9.0, 9.0, 9.0]])
        expected = [[0, 1, 2, 3, 4, 7, 8, 9], [0, 0.1, -0.1, 5, 6, 9, 9, 9]]
        result = pla_bottom_up(tss, 1).to_numpy()
        np.testing.assert_array_almost_equal(result, expected, decimal=self.DECIMAL)

    def test_pla_sliding_window(self):
        tss = Array([[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
                     [0.0, 0.1, -0.1, 5.0, 6.0, 7.0, 8.1, 9.0, 9.0, 9.0]])
        expected = [[0, 2, 3, 7, 8, 9], [0, -0.1, 5, 9, 9, 9]]
        result = pla_sliding_window(tss, 1).to_numpy()
        np.testing.assert_array_almost_equal(result, expected, decimal=self.DECIMAL)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DimensionalityTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
