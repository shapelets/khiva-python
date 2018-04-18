# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
from tsa.linalg import *
import numpy as np


########################################################################################################################

class LinalgTest(unittest.TestCase):
    DELTA = 1e-6

    def setUp(self):
        pass

    def test_lls(self):
        lls_result = lls(array(np.array([[4, 3], [-1, -2]])), array([3, 1], dtype.f32))
        a = lls_result.to_numpy()[0]
        self.assertAlmostEqual(a[0], 1, delta=self.DELTA)
        self.assertAlmostEqual(a[1], 1, delta=self.DELTA)


if __name__ == '__main__':
    unittest.main()
