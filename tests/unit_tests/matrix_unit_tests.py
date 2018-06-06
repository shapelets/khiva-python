# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
from khiva.matrix import *
from khiva.array import *


########################################################################################################################

class MatrixTest(unittest.TestCase):
    DELTA = 1e-6

    def setUp(self):
        pass

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

    def test_find_best_n_motifs(self):

        stomp_result = stomp(Array([10, 10, 10, 10, 10, 10, 9, 10, 10, 10, 10, 10, 11, 10, 9], dtype.f32),
                             Array([10, 11, 10, 9], dtype.f32),
                             3)

        find_best_n_motifs_result = find_best_n_motifs(stomp_result[0], stomp_result[1], 2)
        a = find_best_n_motifs_result[1].to_numpy()
        b = find_best_n_motifs_result[2].to_numpy()
        self.assertAlmostEqual(a[0], 12, delta=self.DELTA)
        self.assertAlmostEqual(a[1], 11, delta=self.DELTA)
        self.assertAlmostEqual(b[0], 1, delta=self.DELTA)
        self.assertAlmostEqual(b[1], 0, delta=self.DELTA)

    def test_find_best_n_discords(self):
        stomp_result = stomp(Array(np.array([11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11])),
                             Array(np.array([9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9])),
                             3)

        find_best_n_discords_result = find_best_n_discords(stomp_result[0],
                                                           stomp_result[1], 2)
        a = find_best_n_discords_result[2].to_numpy()
        self.assertEqual(a[0], 0)
        self.assertEqual(a[1], 9)


if __name__ == '__main__':
    unittest.main()
