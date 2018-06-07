# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
from khiva.linalg import *
import numpy as np
from khiva.array import *


########################################################################################################################

class LinalgTest(unittest.TestCase):
    DELTA = 1e-6

    def setUp(self):
        pass

    def test_lls(self):
        lls_result = lls(Array(np.array([[4, 3], [-1, -2]])), Array([3, 1], dtype.f32))
        a = lls_result.to_numpy()
        self.assertAlmostEqual(a[0], 1, delta=self.DELTA)
        self.assertAlmostEqual(a[1], 1, delta=self.DELTA)


if __name__ == '__main__':
    unittest.main()
