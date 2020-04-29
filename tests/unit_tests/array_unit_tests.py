#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v.  2.0.  If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import unittest

import arrayfire as af
import numpy as np
import pandas as pd

from khiva.array import Array, dtype
from khiva.library import set_backend, KHIVABackend


########################################################################################################################
class ArrayTest(unittest.TestCase):
    DELTA = 1e-6
    DECIMAL = 6

    def setUp(self):
        set_backend(KHIVABackend.KHIVA_BACKEND_CPU)

    def testFromArrayfire(self):
        a = af.Array([1, 2, 3, 4])
        b = Array.from_arrayfire(a)
        self.assertNotEqual(a.arr, 0)
        self.assertNotEqual(b.arr_reference, 0)
        self.assertNotEqual(a.arr, b.arr_reference)
        np.testing.assert_array_equal(
            np.asarray(a.to_list()), np.asarray(b.to_list()))

    def testFromList(self):
        test_input = [1, 2, 3, 4]
        array = Array.from_list(test_input, dtype.s32)
        np.testing.assert_array_equal(test_input, array.to_numpy())

    def testFromNumpy(self):
        test_input = [1, 2, 3, 4]
        array = Array.from_numpy(np.array(test_input), dtype.s32)
        np.testing.assert_array_equal(test_input, array.to_numpy())

    def testFromPandas(self):
        df = pd.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8]])
        df_array = Array.from_pandas(df, dtype.s32)
        np.testing.assert_array_equal(df.values, df_array.to_numpy())

    def test_real_1d(self):
        test_input = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        a = Array.from_list(test_input, dtype.f32)
        expected = np.array(test_input)
        np.testing.assert_array_equal(a.to_numpy(), expected)
        np.testing.assert_array_equal(a.dims, np.array([8, 1, 1, 1]))

    def test_real_2d(self):
        test_input = [[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]]
        a = Array.from_list(test_input, dtype.f32)
        expected = np.array(test_input)
        np.testing.assert_array_equal(a.to_numpy(), expected)
        np.testing.assert_array_equal(a.dims, np.array([4, 2, 1, 1]))

    def test_real_3d(self):
        test_input = [[[1.0, 5.0, 3.0, 1.0], [2.0, 6.0, 9.0, 8.0], [3.0, 4.0, 1.0, 3.0]],
                      [[3.0, 7.0, 4.0, 2.0], [4.0, 8.0, 1.0, 9.0], [1.0, 5.0, 9.0, 2.0]]]
        a = Array.from_list(test_input, dtype.f32)
        expected = np.array(test_input)
        np.testing.assert_array_equal(a.to_numpy(), expected)
        np.testing.assert_array_equal(a.dims, np.array([4, 3, 2, 1]))

    def test_int_4d(self):
        test_input = [[[[1, 9], [2, 10]], [[3, 11], [4, 12]]],
                      [[[5, 13], [6, 14]], [[7, 15], [8, 16]]]]
        a = Array.from_list(test_input, dtype.s64)
        expected = np.array(test_input)
        np.testing.assert_array_equal(a.to_numpy(), expected)
        np.testing.assert_array_equal(a.dims, np.array([2, 2, 2, 2]))

    def test_complex64_1d(self):
        test_input = np.array(
            [1 + 5j, 2 + 6j, 3 + 7j, 4 + 8j]).astype(np.complex64)
        a = Array.from_numpy(test_input, dtype.c32)
        expected = np.array(test_input).astype(np.complex64)
        np.testing.assert_array_equal(a.to_numpy(), expected)
        np.testing.assert_array_equal(a.dims, np.array([4, 1, 1, 1]))

    def test_complex64_2d(self):
        test_input = [[1 + 5j, 2 + 6j, 3 + 7j, 4 + 8j],
                      [9 + 13j, 10 + 14j, 11 + 15j, 12 + 16j]]
        a = Array.from_numpy(
            np.array(test_input).astype(np.complex64), dtype.c32)
        expected = np.array(test_input).astype(np.complex64)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex64_3d(self):
        test_input = [[[1 + 1j, 5 + 5j], [2 + 2j, 6 + 6j]],
                      [[3 + 3j, 7 + 7j], [4 + 4j, 8 + 8j]]]
        a = Array.from_numpy(
            np.array(test_input).astype(np.complex64), dtype.c32)
        expected = np.array(test_input).astype(np.complex64)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex64_4d(self):
        test_input = [[[[1 + 1j, 9 + 9j], [2 + 2j, 10 + 10j]], [[3 + 3j, 11 + 11j], [4 + 4j, 12 + 12j]]],
                      [[[5 + 5j, 13 + 13j], [6 + 6j, 14 + 14j]], [[7 + 7j, 15 + 15j], [8 + 8j, 16 + 16j]]]]
        a = Array.from_numpy(
            np.array(test_input).astype(np.complex64), dtype.c32)
        expected = np.array(test_input).astype(np.complex64)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex128_1d(self):
        test_input = [1 + 5j, 2 + 6j, 3 + 7j, 4 + 8j]
        a = Array.from_numpy(
            np.array(test_input).astype(np.complex128), dtype.c64)
        expected = np.array(test_input).astype(np.complex128)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex128_2d(self):
        test_input = [[1 + 5j, 2 + 6j, 3 + 7j, 4 + 8j],
                      [9 + 13j, 10 + 14j, 11 + 15j, 12 + 16j]]
        a = Array.from_numpy(
            np.array(test_input).astype(np.complex128), dtype.c32)
        expected = np.array(test_input).astype(np.complex128)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex128_3d(self):
        test_input = [[[1 + 1j, 5 + 5j], [2 + 2j, 6 + 6j]],
                      [[3 + 3j, 7 + 7j], [4 + 4j, 8 + 8j]]]
        a = Array.from_numpy(
            np.array(test_input).astype(np.complex128), dtype.c32)
        expected = np.array(test_input).astype(np.complex128)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_complex128_4d(self):
        test_input = [[[[1 + 1j, 9 + 9j], [2 + 2j, 10 + 10j]], [[3 + 3j, 11 + 11j], [4 + 4j, 12 + 12j]]],
                      [[[5 + 5j, 13 + 13j], [6 + 6j, 14 + 14j]], [[7 + 7j, 15 + 15j], [8 + 8j, 16 + 16j]]]]
        a = Array.from_numpy(np.array(test_input).astype(
            np.complex128), khiva_type=dtype.c32)
        expected = np.array(test_input).astype(np.complex128)
        np.testing.assert_array_equal(a.to_numpy(), expected)

    def test_get_type(self):
        a = Array.from_list([[1, 2, 3, 4], [5, 6, 7, 8]], dtype.s64)
        self.assertEqual(a.get_type(), dtype.s64)

    def test_join(self):
        a = Array.from_list([1, 2, 3, 4], dtype.f64)
        b = Array.from_list([5, 6, 7, 8], dtype.f64)
        c = a.join(0, b)
        np.testing.assert_array_equal(
            c.to_numpy(), np.array([1, 2, 3, 4, 5, 6, 7, 8]))

    def testPlus(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([1, 2, 3, 4], dtype.s32)
        c = a + b
        np.testing.assert_array_equal(c.to_numpy(), np.array([2, 4, 6, 8]))

    def testTimes(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([1, 2, 3, 4], dtype.s32)
        c = a * b
        np.testing.assert_array_equal(c.to_numpy(), np.array([1, 4, 9, 16]))

    def testTimesException(self):
        a = Array.from_list([1, 2, 3, 4, 5], dtype.s32)
        b = Array.from_list([1, 2, 3, 4], dtype.s32)
        with self.assertRaises(Exception) as context:
            a * b

    def testMinus(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([1, 2, 3, 4], dtype.s32)
        c = a - b
        np.testing.assert_array_equal(c.to_numpy(), np.array([0, 0, 0, 0]))

    def testRDivide(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([1, 2, 3, 4], dtype.s32)
        c = a / b
        expected = np.array([1., 1., 1., 1.])
        for d, e in zip(expected, c.to_numpy()):
            self.assertAlmostEqual(d, e, delta=1e-5)

    def testMod(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([2, 2, 2, 2], dtype.s32)
        c = a % b
        np.testing.assert_array_equal(c.to_numpy(), np.array([1, 0, 1, 0]))

    def testModInPlace(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([1, 2, 3, 4], dtype.s32)
        a %= b
        np.testing.assert_array_equal(a.to_numpy(), np.array([0, 0, 0, 0]))

    def testPower(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([2, 2, 2, 2], dtype.s32)
        c = a ** b
        np.testing.assert_array_equal(c.to_numpy(), np.array([1, 4, 9, 16]))

    def testLt(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([2, 2, 2, 2], dtype.s32)
        c = a < b
        np.testing.assert_array_equal(
            c.to_numpy(), np.array([True, False, False, False]))

    def testGt(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([2, 2, 2, 2], dtype.s32)
        c = a > b
        np.testing.assert_array_equal(
            c.to_numpy(), np.array([False, False, True, True]))

    def testLe(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([2, 2, 2, 2], dtype.s32)
        c = a <= b
        np.testing.assert_array_equal(
            c.to_numpy(), np.array([True, True, False, False]))

    def testGe(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([2, 2, 2, 2], dtype.s32)
        c = a >= b
        np.testing.assert_array_equal(
            c.to_numpy(), np.array([False, True, True, True]))

    def testEq(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([1, 2, 3, 5], dtype.s32)
        c = a == b
        np.testing.assert_array_equal(
            c.to_numpy(), np.array([True, True, True, False]))

    def testNeq(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([1, 2, 3, 5], dtype.s32)
        c = a != b
        np.testing.assert_array_equal(
            c.to_numpy(), np.array([False, False, False, True]))

    def testAnd(self):
        a = Array.from_list([True, True, True, True], dtype.b8)
        b = Array.from_list([True, False, True, False], dtype.b8)
        c = a & b
        np.testing.assert_array_equal(
            c.to_numpy(), np.array([True, False, True, False]))

    def testOr(self):
        a = Array.from_list([True, True, True, True], dtype.b8)
        b = Array.from_list([True, False, True, False], dtype.b8)
        c = a | b
        np.testing.assert_array_equal(
            c.to_numpy(), np.array([True, True, True, True]))

    def testXor(self):
        a = Array.from_list([True, True, True, True], dtype.b8)
        b = Array.from_list([True, False, True, False], dtype.b8)
        c = a ^ b
        np.testing.assert_array_equal(
            c.to_numpy(), np.array([False, True, False, True]))

    def testXorInPlace(self):
        a = Array.from_list([True, True, True, True], dtype.b8)
        b = Array.from_list([True, False, True, False], dtype.b8)
        a ^= b
        np.testing.assert_array_equal(
            a.to_numpy(), np.array([False, True, False, True]))

    def testBitshift(self):
        a = Array.from_list([2, 4, 6, 8], dtype.s32)
        c = a >> 1
        np.testing.assert_array_equal(c.to_numpy(), np.array([1, 2, 3, 4]))

    def testBitshiftInPlace(self):
        a = Array.from_list([2, 4, 6, 8], dtype.s32)
        a >>= 1
        np.testing.assert_array_equal(a.to_numpy(), np.array([1, 2, 3, 4]))

    def testBitsra(self):
        a = Array.from_list([2, 4, 6, 8], dtype.s32)
        c = a << 1
        np.testing.assert_array_equal(c.to_numpy(), np.array([4, 8, 12, 16]))

    def testBitsra(self):
        a = Array.from_list([2, 4, 6, 8], dtype.s32)
        a <<= 1
        np.testing.assert_array_equal(a.to_numpy(), np.array([4, 8, 12, 16]))

    def testCtranspose(self):
        a = Array.from_list(
            [[0 - 1j, 4 + 2j], [2 + 1j, 0 - 2j]], khiva_type=dtype.c32)
        b = a.transpose(True)
        expected = [[0 + 1j, 2 - 1j], [4 - 2j, 0 + 2j]]
        np.testing.assert_array_equal(b.to_numpy(), expected)

    def testTranspose(self):
        a = Array.from_list([[1, 3], [2, 4]], dtype.s32)
        c = a.transpose()
        np.testing.assert_array_equal(c.to_numpy(), np.array([[1, 2], [3, 4]]))

    def testCol(self):
        a = Array.from_list([[1, 3], [2, 4]], dtype.s32)
        c = a.get_col(0)
        np.testing.assert_array_equal(c.to_numpy(), np.array([1, 3]))

    def testCols(self):
        a = Array.from_numpy(np.transpose([[1, 2, 3], [4, 5, 6]]), dtype.s32)
        c = a.get_cols(0, 1)
        np.testing.assert_array_equal(
            c.to_numpy(), np.transpose(np.array([[1, 2], [4, 5]])))

    def testRow(self):
        a = Array.from_numpy(np.transpose([[1, 2], [3, 4]]), dtype.s32)
        c = a.get_row(0)
        np.testing.assert_array_equal(
            c.to_numpy(), np.transpose(np.array([[1, 2]])))

    def testRows(self):
        a = Array.from_numpy(np.transpose([[1, 2], [3, 4], [5, 6]]), dtype.s32)
        c = a.get_rows(0, 1)
        np.testing.assert_array_equal(
            c.to_numpy(), np.transpose(np.array([[1, 2], [3, 4]])))

    def testMatmul(self):
        a = Array.from_list([1, 2, 3, 4], dtype.f32)
        b = a.transpose()
        c = a.matmul(b)
        expected = np.transpose(
            [[1, 2, 3, 4], [2, 4, 6, 8], [3, 6, 9, 12], [4, 8, 12, 16]])
        np.testing.assert_array_equal(c.to_numpy(), expected)

    def testAs(self):
        a = Array.from_list([1.0, 2.0, 3.0, 4.0], dtype.f32)
        b = a.as_type(dtype.u32)
        expected_data = [1, 2, 3, 4]
        np.testing.assert_array_equal(b.to_numpy(), expected_data)
        self.assertEqual(b.khiva_type, dtype.u32)

    def testCopy(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = a.copy()
        np.testing.assert_array_equal(a.to_numpy(), b.to_numpy())
        self.assertEqual(b.khiva_type, b.khiva_type)
        self.assertNotEqual(a.arr_reference, b.arr_reference)

    def testLength(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        self.assertEqual(len(a), 4)

    def testIaddException(self):
        with self.assertRaises(Exception) as cm:
            a = Array.from_list([1, 2, 3, 4, 5], dtype.s32)
            b = Array.from_list([1, 2, 3, 4], dtype.s32)
            a += b

    def testIadd(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([1, 2, 3, 4], dtype.s32)
        a += b
        np.testing.assert_array_equal(a.to_numpy(), np.array([2, 4, 6, 8]))

    def testIaddSelfArray(self):
        a = Array.from_list([1, 2, 3, 4, 5], dtype.s32)
        a += a
        np.testing.assert_array_equal(a.to_numpy(), np.array([2, 4, 6, 8, 10]))

    def testISub(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([1, 2, 3, 4], dtype.s32)
        a -= b
        np.testing.assert_array_equal(a.to_numpy(), np.array([0, 0, 0, 0]))

    def testIMul(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([1, 2, 3, 4], dtype.s32)
        a *= b
        np.testing.assert_array_equal(a.to_numpy(), np.array([1, 4, 9, 16]))

    def testITrueDiv(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([1, 2, 3, 4], dtype.s32)
        a /= b
        np.testing.assert_array_equal(a.to_numpy(), np.array([1, 1, 1, 1]))

    def testDiv(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([1, 2, 3, 4], dtype.s32)
        c = a / b
        np.testing.assert_array_equal(c.to_numpy(), np.array([1, 1, 1, 1]))

    def testIPow(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        b = Array.from_list([2, 2, 2, 2], dtype.s32)
        a **= b
        np.testing.assert_array_equal(a.to_numpy(), np.array([1, 4, 9, 16]))

    def testIAnd(self):
        a = Array.from_list([1, 1, 1, 1], dtype.b8)
        b = Array.from_list([1, 0, 1, 0], dtype.b8)
        a &= b
        np.testing.assert_array_equal(a.to_numpy(), np.array([1, 0, 1, 0]))

    def testIOr(self):
        a = Array.from_list([1, 1, 1, 1], dtype.b8)
        b = Array.from_list([1, 0, 1, 0], dtype.b8)
        a |= b
        np.testing.assert_array_equal(a.to_numpy(), np.array([1, 1, 1, 1]))

    def testNeg(self):
        a = Array.from_list([[1, 2], [3, 4]], dtype.s32)
        b = -a
        np.testing.assert_array_equal(
            b.to_numpy(), np.array([[-1, -2], [-3, -4]]))

    def testNot(self):
        a = Array.from_list([True, True, True, False], khiva_type=dtype.b8)
        b = ~a
        np.testing.assert_array_equal(
            b.to_numpy(), np.array([False, False, False, True]))

    def testStr(self):
        a = Array.from_list([2, 4, 6, 8], dtype.s32)
        self.assertEqual(
            "khiva.Array()\nType: dtype.s32\nDims: [4 1 1 1]", str(a))

    def testRepre(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s64)
        self.assertEqual(
            "khiva.Array()\nType: dtype.s64\nDims: [4 1 1 1]", str(repr(a)))

    def testNonZero(self):
        a = Array.from_list([1, 2, 3, 4], dtype.s32)
        self.assertTrue(a)
    
    def testZero(self):
        a = Array.from_list([0, 0, 0, 0], dtype.s32)
        self.assertFalse(a)

    def testGetData1(self):
        a = Array.from_list([1], dtype.s32)
        np.testing.assert_array_equal(a._get_data(), np.array([1]))

    def testToList1(self):
        a = Array.from_list([1], dtype.s32)
        a_list = a.to_list()
        self.assertIs(type(a_list), list)
        self.assertEqual(a_list[0], 1)
    
    def testToArrayfire(self):
        a = Array.from_list([1], dtype.s32)
        af = a.to_arrayfire()
        self.assertNotEqual(af.arr, a.arr_reference)
        self.assertNotEqual(af.arr, 0)
        self.assertNotEqual(a.arr_reference, 0)        


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ArrayTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
