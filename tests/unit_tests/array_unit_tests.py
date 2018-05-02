# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest
import numpy as np
from tsa.array import array, dtype


########################################################################################################################

class ArrayTest(unittest.TestCase):
    DELTA = 1e-6
    DECIMAL = 6

    def setUp(self):
        pass

    def test_real_1d(self):
        a = array([1, 2, 3, 4, 5, 6, 7, 8])
        expected = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_real_2d(self):
        a = array([[1, 2, 3, 4], [5, 6, 7, 8]])
        expected = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_real_3d(self):
        a = array([[[1, 5], [2, 6]], [[3, 7], [4, 8]]])
        expected = np.array([[[1, 5], [2, 6]], [[3, 7], [4, 8]]])
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_real_4d(self):
        a = array([[[[1, 9], [2, 10]], [[3, 11], [4, 12]]], [[[5, 13], [6, 14]], [[7, 15], [8, 16]]]])
        expected = np.array([[[[1, 9], [2, 10]], [[3, 11], [4, 12]]], [[[5, 13], [6, 14]], [[7, 15], [8, 16]]]])
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex64_1d(self):
        a = array(np.array([1 + 5j, 2 + 6j, 3 + 7j, 4 + 8j]).astype(np.complex64), tsa_type=dtype.c32)
        expected = np.array([1 + 5j, 2 + 6j, 3 + 7j, 4 + 8j]).astype(np.complex64)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex64_2d(self):
        a = array(
            np.array([[1 + 5j, 2 + 6j, 3 + 7j, 4 + 8j], [9 + 13j, 10 + 14j, 11 + 15j, 12 + 16j]]).astype(np.complex64),
            tsa_type=dtype.c32)
        expected = np.array([[1 + 5j, 2 + 6j, 3 + 7j, 4 + 8j], [9 + 13j, 10 + 14j, 11 + 15j, 12 + 16j]]).astype(
            np.complex64)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex64_3d(self):
        a = array(
            np.array([[[1 + 1j, 5 + 5j], [2 + 2j, 6 + 6j]], [[3 + 3j, 7 + 7j], [4 + 4j, 8 + 8j]]]).astype(np.complex64),
            tsa_type=dtype.c32)
        expected = np.array([[[1 + 1j, 5 + 5j], [2 + 2j, 6 + 6j]], [[3 + 3j, 7 + 7j], [4 + 4j, 8 + 8j]]]).astype(
            np.complex64)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex64_4d(self):
        a = array(
            np.array([[[[1 + 1j, 9 + 9j], [2 + 2j, 10 + 10j]], [[3 + 3j, 11 + 11j], [4 + 4j, 12 + 12j]]],
                      [[[5 + 5j, 13 + 13j], [6 + 6j, 14 + 14j]], [[7 + 7j, 15 + 15j], [8 + 8j, 16 + 16j]]]])
                .astype(np.complex64),
            tsa_type=dtype.c32)
        expected = np.array([[[[1 + 1j, 9 + 9j], [2 + 2j, 10 + 10j]], [[3 + 3j, 11 + 11j], [4 + 4j, 12 + 12j]]],
                             [[[5 + 5j, 13 + 13j], [6 + 6j, 14 + 14j]],
                              [[7 + 7j, 15 + 15j], [8 + 8j, 16 + 16j]]]]).astype(
            np.complex64)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex128_1d(self):
        a = array(np.array([1 + 5j, 2 + 6j, 3 + 7j, 4 + 8j]).astype(np.complex128), tsa_type=dtype.c64)
        expected = np.array([1 + 5j, 2 + 6j, 3 + 7j, 4 + 8j]).astype(np.complex128)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex128_2d(self):
        a = array(
            np.array([[1 + 5j, 2 + 6j, 3 + 7j, 4 + 8j], [9 + 13j, 10 + 14j, 11 + 15j, 12 + 16j]]).astype(np.complex128),
            tsa_type=dtype.c32)
        expected = np.array([[1 + 5j, 2 + 6j, 3 + 7j, 4 + 8j], [9 + 13j, 10 + 14j, 11 + 15j, 12 + 16j]]).astype(
            np.complex128)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex128_3d(self):
        a = array(
            np.array([[[1 + 1j, 5 + 5j], [2 + 2j, 6 + 6j]], [[3 + 3j, 7 + 7j], [4 + 4j, 8 + 8j]]]).astype(
                np.complex128),
            tsa_type=dtype.c32)
        expected = np.array([[[1 + 1j, 5 + 5j], [2 + 2j, 6 + 6j]], [[3 + 3j, 7 + 7j], [4 + 4j, 8 + 8j]]]).astype(
            np.complex128)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex128_4d(self):
        a = array(
            np.array([[[[1 + 1j, 9 + 9j], [2 + 2j, 10 + 10j]], [[3 + 3j, 11 + 11j], [4 + 4j, 12 + 12j]]],
                      [[[5 + 5j, 13 + 13j], [6 + 6j, 14 + 14j]], [[7 + 7j, 15 + 15j], [8 + 8j, 16 + 16j]]]])
                .astype(np.complex128),
            tsa_type=dtype.c32)
        expected = np.array([[[[1 + 1j, 9 + 9j], [2 + 2j, 10 + 10j]], [[3 + 3j, 11 + 11j], [4 + 4j, 12 + 12j]]],
                             [[[5 + 5j, 13 + 13j], [6 + 6j, 14 + 14j]],
                              [[7 + 7j, 15 + 15j], [8 + 8j, 16 + 16j]]]]).astype(
            np.complex128)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_get_type(self):
        a = array([[1, 2, 3, 4], [5, 6, 7, 8]], tsa_type=dtype.s64)
        expected = dtype.s64
        self.assertEqual(a.get_type(), expected)


if __name__ == '__main__':
    unittest.main()
