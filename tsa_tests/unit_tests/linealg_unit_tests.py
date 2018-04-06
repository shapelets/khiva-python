# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
from tsa.algorithms.linalg import *


########################################################################################################################

class LinealgTest(unittest.TestCase):
    DELTA = 1e-6

    def setUp(self):
        pass

    def test_lls(self):
        lls_result = lls(np.array([[4, 3], [-1, -2]]), [3, 1])
        self.assertAlmostEqual(lls_result[0], 1, delta=self.DELTA)
        self.assertAlmostEqual(lls_result[1], 1, delta=self.DELTA)


if __name__ == '__main__':
    unittest.main()
