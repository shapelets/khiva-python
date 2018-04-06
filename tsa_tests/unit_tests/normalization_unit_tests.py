# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
from tsa.algorithms.normalization import *


########################################################################################################################

class NormalizationTest(unittest.TestCase):
    DELTA = 1e-6

    def setUp(self):
        pass

    def test_normz(self):
        znorm_result = znorm([[0, 1, 2, 3], [4, 5, 6, 7]], 0.00000001)
        expected = [-1.341640786499870, -0.447213595499958, 0.447213595499958, 1.341640786499870]
        for i in range(len(expected)):
            self.assertAlmostEqual(znorm_result[i], expected[i])
            self.assertAlmostEqual(znorm_result[i + 4], expected[i])


if __name__ == '__main__':
    unittest.main()
