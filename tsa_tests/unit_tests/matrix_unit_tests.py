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
from tsa.algorithms.matrix import *


########################################################################################################################

class MatrixTest(unittest.TestCase):
    DELTA = 1e-6

    def setUp(self):
        pass

    def test_stomp_self_join(self):
        stomp_self_join_result = stomp_self_join([10, 10, 10, 11, 12, 11, 10, 10, 11, 12, 11, 10, 10, 10], 3)
        expected_index = [11, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 0]

        for i in range(12):
            self.assertAlmostEqual(stomp_self_join_result["matrix_profile"][i], 0.0, delta=self.DELTA)
            self.assertEqual(stomp_self_join_result["index_profile"][i], expected_index[i])

    def test_stomp(self):
        stomp_result = stomp([10, 10, 10, 11, 12, 11, 10, 10, 11, 12, 11, 10, 10, 10],
                             [10, 10, 10, 11, 12, 11, 10, 10, 11, 12, 11, 10, 10, 10], 3)
        expected_index = [11, 1, 2, 8, 9, 10, 1, 2, 8, 9, 10, 11]

        for i in range(12):
            self.assertAlmostEqual(stomp_result["matrix_profile"][i], 0.0, delta=self.DELTA)
            self.assertEqual(stomp_result["index_profile"][i], expected_index[i])

    def test_find_best_n_motifs(self):

        stomp_result = stomp([10, 11, 10, 10, 10, 10, 9, 10, 10, 10, 10, 10, 11, 10],
                             [10, 11, 10, 300, 20, 30, 40, 50, 60, 70, 80, 90, 80, 90],
                             3)

        find_best_n_motifs_result = find_best_n_motifs(stomp_result['matrix_profile'], stomp_result["index_profile"], 3)
        self.assertEqual(find_best_n_motifs_result["motif_index"][0], 0)
        self.assertEqual(find_best_n_motifs_result["motif_index"][1], 0)

        self.assertEqual(find_best_n_motifs_result["subsequence_index"][0], 0)
        self.assertEqual(find_best_n_motifs_result["subsequence_index"][1], 10)

    def test_find_best_n_discords(self):
        stomp_result = stomp(np.array([10, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 10]),
                             np.array([10, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 10]),
                             3)

        find_best_n_discords_result = find_best_n_discords(stomp_result['matrix_profile'],
                                                           stomp_result["index_profile"], 3)

        self.assertEqual(find_best_n_discords_result["subsequence_index"][0], 0)
        self.assertEqual(find_best_n_discords_result["subsequence_index"][1], 11)


if __name__ == '__main__':
    unittest.main()
