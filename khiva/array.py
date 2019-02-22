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
import numpy as np
import ctypes
from collections import deque
from khiva.library import KhivaLibrary
from enum import Enum
import pandas as pd
import logging
import sys


########################################################################################################################

class dtype(Enum):
    """
    KHIVA array available types.
    """
    f32 = 0
    """
    Float. khiva.dtype
    """
    c32 = 1
    """
    32 bits Complex. khiva.dtype
    """
    f64 = 2
    """
    64 bits Double. khiva.dtype
    """
    c64 = 3
    """
    64 bits Complex. khiva.dtype
    """
    b8 = 4
    """
    Boolean. khiva.dtype
    """
    s32 = 5
    """
    32 bits Int. khiva.dtype
    """
    u32 = 6
    """
    32 bits Unsigned Int. khiva.dtype
    """
    u8 = 7
    """
    8 bits Unsigned Int. khiva.dtype
    """
    s64 = 8
    """
    64 bits Integer. khiva.dtype
    """
    u64 = 9
    """
    64 bits Unsigned Int. khiva.dtype
    """
    s16 = 10
    """
    16 bits Int. khiva.dtype
    """
    u16 = 11
    """
    16 bits Unsigned int. khiva.dtype
    """


def _get_array_type(khiva_type):
    """
    Transform the KHIVA type to its equivalent in ctypes.

    :param khiva_type: KHIVA type.

    :return: The ctypes equivalent.
    """
    return {
        dtype.f32.value: ctypes.c_float,
        dtype.c32.value: ctypes.c_float,
        dtype.f64.value: ctypes.c_double,
        dtype.c64.value: ctypes.c_double,
        dtype.b8.value: ctypes.c_bool,
        dtype.u8.value: ctypes.c_uint8,
        dtype.s16.value: ctypes.c_int16,
        dtype.u16.value: ctypes.c_uint16,
        dtype.s32.value: ctypes.c_int32,
        dtype.u32.value: ctypes.c_uint32,
        dtype.s64.value: ctypes.c_int64,
        dtype.u64.value: ctypes.c_uint64
    }[khiva_type]


def _get_numpy_type(khiva_type):
    """
     Transform the KHIVA type to its equivalent in Numpy.

    :param khiva_type: KHIVA type.

    :return: The Numpy type equivalent.
    """
    return {
        dtype.f32.value: np.float,
        dtype.c32.value: np.complex64,
        dtype.f64.value: np.double,
        dtype.c64.value: np.complex128,
        dtype.b8.value: np.bool,
        dtype.u8.value: np.uint8,
        dtype.s16.value: np.int8,
        dtype.u16.value: np.uint16,
        dtype.s32.value: np.int16,
        dtype.u32.value: np.uint32,
        dtype.s64.value: np.int64,
        dtype.u64.value: np.uint64,
    }[khiva_type]


class Array:
    __array_priority__ = 50

    def __init__(self, data=None, khiva_type=dtype.f32, array_reference=None, arrayfire_reference=False):
        """
        Creates a KHIVA array in one of the following ways: 1) using a previously created array; or 2) with data (in
        numpy, list, or pandas dataframe format)

        :param data: Numpy array, List of elements or a Pandas dataframe.
        :param khiva_type: KHIVA type.
        :param array_reference: Reference of the array.
        """
        if array_reference is None:
            self.khiva_type = khiva_type
            self.arr_reference = self._create_array(data)
            self.dims = self.get_dims()
            self.result_l = self._get_result_length()
        else:
            self.arr_reference = array_reference
            self.khiva_type = self.get_type()
            self.dims = self.get_dims()
            self.result_l = self._get_result_length()

        self.arrayfire_reference = arrayfire_reference

    @classmethod
    def from_arrayfire(cls, arrayfire):
        """
        Creates a KHIVA array from an array of ArrayFire.

        :param arrayfire: An ArrayFire array.
        :return: a KHIVA array.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.from_arrayfire(ctypes.pointer(arrayfire.arr), ctypes.pointer(result))
        return cls(array_reference=result, arrayfire_reference=True)

    def _create_array(self, data):
        """ Creates the KHIVA array in the device.

        :param data: The data used for creating the khiva array.

        :return An opaque pointer to the Array.
        """
        if isinstance(data, list):
            data = np.asarray(data)
        if isinstance(data, pd.DataFrame):
            data = data.values
        shape = np.array(data.shape)
        shape = shape[shape > 1]
        shape = deque(shape)
        shape.rotate(1)
        c_array_n = (ctypes.c_longlong * len(shape))(*(np.array(shape)).astype(np.longlong))
        c_ndims = ctypes.c_uint(len(shape))
        c_complex = np.iscomplexobj(data)

        if c_complex:
            data = np.array([data.real, data.imag])
            c = deque(range(1, len(data.shape)))
            c.rotate(1)
            c.append(0)
            array_joint = np.transpose(data, c).flatten()
        else:
            array_joint = data.flatten()

        c_array_joint = (_get_array_type(self.khiva_type.value) * len(array_joint))(
            *array_joint)
        opaque_pointer = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.create_array(ctypes.pointer(c_array_joint),
                                                    ctypes.pointer(c_ndims),
                                                    ctypes.pointer(c_array_n),
                                                    ctypes.pointer(opaque_pointer),
                                                    ctypes.pointer(ctypes.c_int(self.khiva_type.value)))
        return opaque_pointer

    def _get_data(self):
        """ Retrieves the data from the device to the host.

        :return A numpy array with the data.
        """
        initialized_result_array = np.zeros(self.result_l).astype(_get_array_type(self.khiva_type.value))
        c_result_array = (_get_array_type(self.khiva_type.value) * self.result_l)(*initialized_result_array)
        KhivaLibrary().c_khiva_library.get_data(ctypes.pointer(self.arr_reference), ctypes.pointer(c_result_array))

        dims = self.get_dims()
        dims = dims[dims > 1]
        a = np.array(c_result_array)

        if self._is_complex():
            a = np.array(np.split(a, self.result_l / 2))
            a = np.apply_along_axis(lambda args: [complex(*args)], 1, a)
            a = a.reshape(dims)
            c = deque(range(len(a.shape)))
            c.rotate(-1)
            a = np.transpose(a, c)
        else:
            dims = deque(dims)
            dims.rotate(1)
            a = a.reshape(dims)

        a = a.astype(_get_numpy_type(self.khiva_type.value))
        return a

    def _get_result_length(self):
        """ Gets the length of the result.

        :return: The length of the result, used in order to get the data to the host.
        """
        result = 1
        for value in self.dims:
            result *= value

        if self._is_complex():
            result *= 2

        return int(result)

    def get_dims(self):
        """ Gets the dimensions of the KHIVA array.

        :return: The dimensions of the KHIVA array.
        """
        c_array_n = (ctypes.c_longlong * 4)(*(np.zeros(4)).astype(np.longlong))
        KhivaLibrary().c_khiva_library.get_dims(ctypes.pointer(self.arr_reference), ctypes.pointer(c_array_n))
        return np.array(c_array_n)

    def get_type(self):
        """ Gets the type of the KHIVA array.

        :return: The type of the KHIVA array.
        """
        c_type = ctypes.c_int()
        KhivaLibrary().c_khiva_library.get_type(ctypes.pointer(self.arr_reference), ctypes.pointer(c_type))
        return dtype(c_type.value)

    def _is_complex(self):
        """ Returns True if the array contains complex numbers and False otherwise.

        :return: True if the array contains complex numbers and False otherwise.
        """
        return self.khiva_type.value == dtype.c32.value or self.khiva_type.value == dtype.c64.value

    def to_arrayfire(self):
        """ Creates an Arrayfire array from this KHIVA array. This need to be used carefully as the same array
        reference is oging to be used by both of them. Once the Arrayfire array is created, the destructor of
        the KHIVA array is not going to free the allocated array.

        :return: an Arrayfire Array
        """
        try:
            import arrayfire as af
        except ModuleNotFoundError:
            logging.error("In order to use `to_arrayfire()` function, you need to install the Arrayfire Python library")
            sys.exit(1)
        result = af.Array()
        result.arr = self.arr_reference
        self.arrayfire_reference = True
        return result

    def to_list(self):
        """ Converts the KHIVA array to a list.

        :return: KHIVA array converted to list.
        """
        return self._get_data().tolist()

    def to_numpy(self):
        """ Converts the KHIVA array to a numpy array.

        :return: KHIVA array converted to numpy.array.
        """
        return self._get_data()

    def to_pandas(self):
        """ Converts the KHIVA array to a pandas data frame.

        :return: KHIVA array converted to a pandas data frame.
        """
        return pd.DataFrame(data=self._get_data())

    def display(self):
        """
        Dispays the data stored in the KHIVA array.
        """
        KhivaLibrary().c_khiva_library.display(ctypes.pointer(self.arr_reference))

    def __len__(self):
        """
        Return the length.
        """
        if self._is_complex():
            return self.result_l / 2
        else:
            return self.result_l

    def __del__(self):
        """
        Class destructor.
        """
        if not self.arrayfire_reference:
            KhivaLibrary().c_khiva_library.delete_array(ctypes.pointer(self.arr_reference))

    def __add__(self, other):
        """
        Return self + other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_add(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __iadd__(self, other):
        """
        Perform self += other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_add(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __radd__(self, other):
        """
        Return other + self.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_add(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __sub__(self, other):
        """
        Return self - other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_sub(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __isub__(self, other):
        """
        Perform self -= other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_sub(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __rsub__(self, other):
        """
        Return other - self.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_sub(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __mul__(self, other):
        """
        Return self * other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_mul(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __imul__(self, other):
        """
        Perform self *= other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_mul(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __rmul__(self, other):
        """
        Return other * self.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_mul(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __truediv__(self, other):
        """
        Return self / other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_div(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __itruediv__(self, other):
        """
        Perform self /= other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_div(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __rtruediv__(self, other):
        """
        Return other / self.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_div(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __div__(self, other):
        """
        Return self / other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_div(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __idiv__(self, other):
        """
        Perform other / self.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_div(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __rdiv__(self, other):
        """
        Return other / self.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_div(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __mod__(self, other):
        """
        Return self % other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_mod(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __imod__(self, other):
        """
        Perform self %= other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_mod(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __rmod__(self, other):
        """
        Return other % self.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_mod(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __pow__(self, other):
        """
        Return self ** other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_pow(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __ipow__(self, other):
        """
        Perform self **= other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_pow(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __rpow__(self, other):
        """
        Return other ** self.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_pow(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(other.arr_reference),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def __lt__(self, other):
        """
        Return self < other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_lt(ctypes.pointer(self.arr_reference), ctypes.pointer(other.arr_reference),
                                                ctypes.pointer(result))
        return Array(array_reference=result)

    def __gt__(self, other):
        """
        Return self > other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_gt(ctypes.pointer(self.arr_reference), ctypes.pointer(other.arr_reference),
                                                ctypes.pointer(result))
        return Array(array_reference=result)

    def __le__(self, other):
        """
        Return self <= other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_le(ctypes.pointer(self.arr_reference), ctypes.pointer(other.arr_reference),
                                                ctypes.pointer(result))
        return Array(array_reference=result)

    def __ge__(self, other):
        """
        Return self >= other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_ge(ctypes.pointer(self.arr_reference), ctypes.pointer(other.arr_reference),
                                                ctypes.pointer(result))
        return Array(array_reference=result)

    def __eq__(self, other):
        """
        Return self == other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_eq(ctypes.pointer(self.arr_reference), ctypes.pointer(other.arr_reference),
                                                ctypes.pointer(result))
        return Array(array_reference=result)

    def __ne__(self, other):
        """
        Return self != other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_ne(ctypes.pointer(self.arr_reference), ctypes.pointer(other.arr_reference),
                                                ctypes.pointer(result))
        return Array(array_reference=result)

    def __and__(self, other):
        """
        Return self & other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_bitand(ctypes.pointer(self.arr_reference),
                                                    ctypes.pointer(other.arr_reference),
                                                    ctypes.pointer(result))
        return Array(array_reference=result)

    def __iand__(self, other):
        """
        Perform self &= other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_bitand(ctypes.pointer(self.arr_reference),
                                                    ctypes.pointer(other.arr_reference),
                                                    ctypes.pointer(result))
        return Array(array_reference=result)

    def __or__(self, other):
        """
        Return self | other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_bitor(ctypes.pointer(self.arr_reference),
                                                   ctypes.pointer(other.arr_reference),
                                                   ctypes.pointer(result))
        return Array(array_reference=result)

    def __ior__(self, other):
        """
        Perform self |= other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_bitor(ctypes.pointer(self.arr_reference),
                                                   ctypes.pointer(other.arr_reference),
                                                   ctypes.pointer(result))
        return Array(array_reference=result)

    def __xor__(self, other):
        """
        Return self ^ other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_bitxor(ctypes.pointer(self.arr_reference),
                                                    ctypes.pointer(other.arr_reference),
                                                    ctypes.pointer(result))
        return Array(array_reference=result)

    def __ixor__(self, other):
        """
        Perform self ^= other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_bitxor(ctypes.pointer(self.arr_reference),
                                                    ctypes.pointer(other.arr_reference),
                                                    ctypes.pointer(result))
        return Array(array_reference=result)

    def __lshift__(self, other):
        """
        Return self << other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_bitshiftl(ctypes.pointer(self.arr_reference),
                                                       ctypes.pointer(ctypes.c_int32(other)), ctypes.pointer(result))
        return Array(array_reference=result)

    def __ilshift__(self, other):
        """
        Perform self <<= other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_bitshiftl(ctypes.pointer(self.arr_reference),
                                                       ctypes.pointer(ctypes.c_int32(other)), ctypes.pointer(result))
        return Array(array_reference=result)

    def __rshift__(self, other):
        """
        Return self >> other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_bitshiftr(ctypes.pointer(self.arr_reference),
                                                       ctypes.pointer(ctypes.c_int32(other)), ctypes.pointer(result))
        return Array(array_reference=result)

    def __irshift__(self, other):
        """
        Perform self >>= other.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_bitshiftr(ctypes.pointer(self.arr_reference),
                                                       ctypes.pointer(ctypes.c_int32(other)), ctypes.pointer(result))
        return Array(array_reference=result)

    def __neg__(self):
        """
        Return -self
        """
        return Array(np.zeros(self.get_dims())) - self

    def __pos__(self):
        """
        Return +self
        """
        return self

    def __invert__(self):
        """
        Return ~self
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_not(ctypes.pointer(self.arr_reference), ctypes.pointer(result))
        return Array(array_reference=result)

    def _get_metadata_str(self, dims=True):
        return 'khiva.Array()\nType: {}\n{}' \
            .format(self.khiva_type, 'Dims: {}'.format(str(self.dims)) if dims else '')

    def __str__(self):
        """
        Converts the khiva array to string showing its meta data and contents.
        """

        return self._get_metadata_str()

    def __nonzero__(self):
        """
        Returns if the Array is non-zero.
        """
        ne = self != Array(np.zeros(self.get_dims()))
        ne_host = ne.to_numpy()
        return int(np.all(ne_host))

    def __repr__(self):
        """
        Displays the meta data of the arrayfire array.
        """

        return self._get_metadata_str()

    def transpose(self, conjugate=False):
        """
        Transpose the KHIVA Array.

        :param conjugate: Indicates if the transpose is conjugated or not.
        :return: The transposed KHIVA Array.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_transpose(ctypes.pointer(self.arr_reference),
                                                       ctypes.pointer(ctypes.c_bool(conjugate)), ctypes.pointer(result))

        return Array(array_reference=result)

    def get_col(self, index):
        """
        Gets a desired column.

        :param index: Index of the desired column.
        :return: The desired column.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_col(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(ctypes.c_int32(index)),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def get_cols(self, first, last):
        """
        Gets a sequence of columns using the first column index and the last column index, both columns included.

        :param first: First column of the subsequence of columns.
        :param last: Last column of the subsequence of columns.
        :return: A subsequence of columns between 'first' and 'last'.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_cols(ctypes.pointer(self.arr_reference),
                                                  ctypes.pointer(ctypes.c_int32(first)),
                                                  ctypes.pointer(ctypes.c_int32(last)),
                                                  ctypes.pointer(result))
        return Array(array_reference=result)

    def get_row(self, index):
        """
        Gets a desired row.

        :param index: Index of the desired row.
        :return: The desired row.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_row(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(ctypes.c_int32(index)),
                                                 ctypes.pointer(result))
        return Array(array_reference=result)

    def get_rows(self, first, last):
        """
        Gets a sequence of rows using the first row index and the last row index, both rows included.

        :param first: First row of the subsequence of rows.
        :param last: Last row of the subsequence of rows.
        :return: A subsequence of rows between 'first' and 'last'.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_rows(ctypes.pointer(self.arr_reference),
                                                  ctypes.pointer(ctypes.c_int32(first)),
                                                  ctypes.pointer(ctypes.c_int32(last)),
                                                  ctypes.pointer(result))
        return Array(array_reference=result)

    def matmul(self, other):
        """
        Matrix multiplication.

        :param other: KHIVA Array
        :return: The matrix multiplication between these two KHIVA Arrays.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_matmul(ctypes.pointer(self.arr_reference),
                                                    ctypes.pointer(other.arr_reference),
                                                    ctypes.pointer(result))
        return Array(array_reference=result)

    def copy(self):
        """
        Performs a deep copy of the array.

        return: An identical copy of self.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.copy(ctypes.pointer(self.arr_reference), ctypes.pointer(result))
        return Array(array_reference=result)

    def as_type(self, dtype):
        """
        Converts the array to a desired array with a desired type.

        :param dtype: The desired KHIVA data type.
        :return: An array with the desired data type.
        """
        result = ctypes.c_void_p(0)
        KhivaLibrary().c_khiva_library.khiva_as(ctypes.pointer(self.arr_reference),
                                                ctypes.pointer(ctypes.c_int32(dtype.value)), ctypes.pointer(result))
        self.khiva_type = self.get_type()
        return Array(array_reference=result)
