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
import ctypes
import logging
import sys
from enum import Enum

import numpy as np
import pandas as pd

from khiva.library import KhivaLibrary, KHIVA_ERROR_LENGTH


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


_KHIVATYPE_TO_CTYPE = {
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
}

_KHIVATYPE_TO_NUMPY_TYPE = {
    dtype.f32.value: np.float,
    dtype.c32.value: np.complex64,
    dtype.f64.value: np.double,
    dtype.c64.value: np.complex128,
    dtype.b8.value: np.bool,
    dtype.u8.value: np.uint8,
    dtype.s16.value: np.int16,
    dtype.u16.value: np.uint16,
    dtype.s32.value: np.int32,
    dtype.u32.value: np.uint32,
    dtype.s64.value: np.int64,
    dtype.u64.value: np.uint64,
}


def _get_array_type(khiva_type):
    """
    Transform the KHIVA type to its equivalent in ctypes.

    :param khiva_type: KHIVA type.

    :return: The ctypes equivalent.
    """
    return _KHIVATYPE_TO_CTYPE[khiva_type]


def _get_numpy_type(khiva_type):
    """
     Transform the KHIVA type to its equivalent in Numpy.

    :param khiva_type: KHIVA type.

    :return: The Numpy type equivalent.
    """
    return _KHIVATYPE_TO_NUMPY_TYPE[khiva_type]


class Array:
    __array_priority__ = 50

    def __init__(self, array_reference):
        """
        Creates a KHIVA array from a ctypes.c_void_p.
        This constructor is not meant to be used directly. Use methods Array.from_list, Array.from_pandas, Array.from_numpy or Array.from_arrayfire.

        :param array_reference: Reference to an Arrayfire array.
        """
        self.arr_reference = array_reference
        self.khiva_type = self.get_type()
        self.dims = self.get_dims()
        self.result_l = self._get_result_length()

    @staticmethod
    def from_arrayfire(arrayfire):
        """
        Creates a KHIVA array from an array of ArrayFire.
        This method increments the reference count of the ArrayFire's array passed.

        :param arrayfire: An ArrayFire array.
        :return: a KHIVA array.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.from_arrayfire(ctypes.pointer(arrayfire.arr),
                                                      ctypes.pointer(result),
                                                      ctypes.pointer(
                                                          error_code),
                                                      error_message)
        return Array(array_reference=result)

    @staticmethod
    def from_list(input_list, khiva_type):
        """
        Creates a KHIVA array from a Python list.

        :param input_list: A Python list.
        :param khiva_type: The KHIVA type of the elements of the list.
        :return: a KHIVA array.
        """
        if not isinstance(input_list, list):
            raise TypeError("input_list parameter must be a list")
        if not isinstance(khiva_type, dtype):
            raise TypeError("khiva_type parameter must be a khiva.array.dtype")
        data = np.asarray(input_list)
        result = Array._create_array(data, khiva_type)
        return Array(array_reference=result)

    @staticmethod
    def from_pandas(dataframe, khiva_type):
        """
        Creates a KHIVA array from a Pandas dataframe.

        :param input_list: A Pandas dataframe.
        :param khiva_type: The KHIVA type of the elements of the Pandas dataframe.
        :return: a KHIVA array.
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("Input parameter must be a pandas datadrame")
        if not isinstance(khiva_type, dtype):
            raise TypeError("khiva_type parameter must be a khiva.array.dtype")
        data = np.asarray(dataframe.values)
        result = Array._create_array(data, khiva_type)
        return Array(array_reference=result)

    @staticmethod
    def from_numpy(array, khiva_type):
        """
        Creates a KHIVA array from a Pandas dataframe.

        :param input_list: A Numpy multidimensional array.
        :param khiva_type: The KHIVA type of the elements of the Pandas dataframe.
        :return: a KHIVA array.
        """
        if not isinstance(array, np.ndarray):
            raise TypeError("Input parameter must be a numpy array")
        if not isinstance(khiva_type, dtype):
            raise TypeError("khiva_type parameter must be a khiva.array.dtype")

        result = Array._create_array(array, khiva_type)
        return Array(array_reference=result)

    @staticmethod
    def _create_array(data, khiva_type):
        """ Creates the KHIVA array in the device.

        :param data: The numpy array used for creating the khiva array.
        :param khiva_type: KHIVA type of the data elements .

        :return An opaque pointer to the Array.
        """

        shape = np.array(data.shape)

        if data.size > 1:
            trimmed_dims = shape
            for _ in range(0, 3):
                if trimmed_dims[-1] == 1:
                    trimmed_dims = trimmed_dims[:-1]
            shape = trimmed_dims[::-1]
        else:
            shape = np.array([1])

        c_array_n = (ctypes.c_longlong * len(shape))(*
                                                     (np.array(shape)).astype(np.longlong))
        c_ndims = ctypes.c_uint(len(shape))
        c_complex = np.iscomplexobj(data)

        if c_complex:
            data = np.dstack((data.real.flatten(), data.imag.flatten()))

        array_joint = data.flatten()

        c_array_joint = (_get_array_type(khiva_type.value)
                         * len(array_joint))(*array_joint)
        opaque_pointer = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.create_array(ctypes.pointer(c_array_joint),
                                                    c_ndims,
                                                    ctypes.pointer(c_array_n),
                                                    ctypes.pointer(
                                                        opaque_pointer),
                                                    ctypes.c_int(
                                                        khiva_type.value),
                                                    ctypes.pointer(error_code),
                                                    error_message)
        return opaque_pointer

    def _get_data(self):
        """ Retrieves the data from the device to the host.

        :return A numpy array with the data.
        """
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        initialized_result_array = np.zeros(self.result_l).astype(
            _get_array_type(self.khiva_type.value))
        c_result_array = (_get_array_type(self.khiva_type.value)
                          * self.result_l)(*initialized_result_array)
        KhivaLibrary().c_khiva_library.get_data(ctypes.pointer(self.arr_reference),
                                                ctypes.pointer(c_result_array),
                                                ctypes.pointer(error_code),
                                                error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        a = np.array(c_result_array)

        if self._is_complex():
            a = np.array(np.split(a, self.result_l / 2))
            a = np.apply_along_axis(lambda args: [complex(*args)], 1, a)

        # Clean up the last n dimensions if these are equal to 1
        if a.size > 1:
            trimmed_dims = self.get_dims()
            for _ in range(0, 3):
                if trimmed_dims[-1] == 1:
                    trimmed_dims = trimmed_dims[:-1]
        else:
            trimmed_dims = np.array([1])

        a = a.reshape(trimmed_dims[::-1])

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
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.get_dims(ctypes.pointer(self.arr_reference),
                                                ctypes.pointer(c_array_n),
                                                ctypes.pointer(error_code),
                                                error_message)
        return np.array(c_array_n)

    def get_type(self):
        """ Gets the type of the KHIVA array.

        :return: The type of the KHIVA array.
        """
        c_type = ctypes.c_int()
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.get_type(ctypes.pointer(self.arr_reference),
                                                ctypes.pointer(c_type),
                                                ctypes.pointer(error_code),
                                                error_message)
        return dtype(c_type.value)

    def _is_complex(self):
        """ Returns True if the array contains complex numbers and False otherwise.

        :return: True if the array contains complex numbers and False otherwise.
        """
        return self.khiva_type.value == dtype.c32.value or self.khiva_type.value == dtype.c64.value

    def to_arrayfire(self):
        """ Creates an Arrayfire array from this KHIVA array. This need to be used carefully as the same array
        reference is going to be used by both of them. Once the Arrayfire array is created, the destructor of
        the KHIVA array is not going to free the allocated array.

        :return: an Arrayfire Array
        """
        try:
            import arrayfire as af
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(
                "{}. In order to use `to_arrayfire()` function, you need to install the Arrayfire Python library.".format(e))

        local = af.Array()
        local.arr = self.arr_reference
        result = af.Array(local)  # increments Arrayfire's reference count.
        # set to zero to avoid deleting our own reference.
        local.arr = ctypes.c_void_p(0)
        return result

    def to_list(self):
        """ Converts the KHIVA array to a list.

        :return: KHIVA array converted to list.
        """
        return self._get_data().tolist()

    def to_numpy(self):
        """ Converts the KHIVA array to a numpy array.

        The returned numpy array shape matches the Array dimensions as follows:
          - For an Array with dims equal to [4, 2, 1, 1] the numpy shape will be (2, 4).
          - For an Array with dims equal to [4, 3, 2, 1] the numpy shape will be (2, 3, 4).
          - For an Array with dims equal to [4, 1, 2, 3] the numpy shape will be (3, 2, 1, 4).

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
        Displays the data stored in the KHIVA array.
        """
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.display(ctypes.pointer(self.arr_reference),
                                               ctypes.pointer(error_code),
                                               error_message)

    def join(self, dim, other):
        """
        Joins the first and second KHIVA arrays along the specified dimension.
        :param dim: The dimension along which the join occurs.
        :param other: The second input array.
        :return: KHIVA Array with the result of this operation.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.join(ctypes.c_int(dim),
                                            ctypes.pointer(self.arr_reference),
                                            ctypes.pointer(
                                                other.arr_reference),
                                            ctypes.pointer(result),
                                            ctypes.pointer(error_code),
                                            error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

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
        if self.arr_reference:
            error_code = ctypes.c_int(0)
            error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
            KhivaLibrary().c_khiva_library.delete_array(ctypes.pointer(self.arr_reference), ctypes.pointer(error_code),
                                                        error_message)
            if error_code.value != 0:
                raise Exception(str(error_message.value.decode()))

    def __add__(self, other):
        """
        Return self + other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_add(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __iadd__(self, other):
        """
        Perform self += other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_add(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __radd__(self, other):
        """
        Return other + self.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_add(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __sub__(self, other):
        """
        Return self - other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_sub(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __isub__(self, other):
        """
        Perform self -= other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_sub(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __rsub__(self, other):
        """
        Return other - self.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_sub(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __mul__(self, other):
        """
        Return self * other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_mul(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __imul__(self, other):
        """
        Perform self *= other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_mul(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __rmul__(self, other):
        """
        Return other * self.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_mul(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __truediv__(self, other):
        """
        Return self / other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_div(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __itruediv__(self, other):
        """
        Perform self /= other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_div(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __rtruediv__(self, other):
        """
        Return other / self.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_div(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __div__(self, other):
        """
        Return self / other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_div(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __idiv__(self, other):
        """
        Perform other / self.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_div(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __rdiv__(self, other):
        """
        Return other / self.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_div(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __mod__(self, other):
        """
        Return self % other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_mod(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __imod__(self, other):
        """
        Perform self %= other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_mod(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __rmod__(self, other):
        """
        Return other % self.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_mod(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __pow__(self, other):
        """
        Return self ** other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_pow(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __ipow__(self, other):
        """
        Perform self **= other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_pow(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __rpow__(self, other):
        """
        Return other ** self.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_pow(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(
                                                     other.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __lt__(self, other):
        """
        Return self < other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_lt(ctypes.pointer(self.arr_reference),
                                                ctypes.pointer(
                                                    other.arr_reference),
                                                ctypes.pointer(result),
                                                ctypes.pointer(error_code),
                                                error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __gt__(self, other):
        """
        Return self > other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_gt(ctypes.pointer(self.arr_reference),
                                                ctypes.pointer(
                                                    other.arr_reference),
                                                ctypes.pointer(result),
                                                ctypes.pointer(error_code),
                                                error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __le__(self, other):
        """
        Return self <= other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_le(ctypes.pointer(self.arr_reference),
                                                ctypes.pointer(
                                                    other.arr_reference),
                                                ctypes.pointer(result),
                                                ctypes.pointer(error_code),
                                                error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __ge__(self, other):
        """
        Return self >= other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_ge(ctypes.pointer(self.arr_reference),
                                                ctypes.pointer(
                                                    other.arr_reference),
                                                ctypes.pointer(result),
                                                ctypes.pointer(error_code),
                                                error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __eq__(self, other):
        """
        Return self == other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_eq(ctypes.pointer(self.arr_reference),
                                                ctypes.pointer(
                                                    other.arr_reference),
                                                ctypes.pointer(result),
                                                ctypes.pointer(error_code),
                                                error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __ne__(self, other):
        """
        Return self != other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_ne(ctypes.pointer(self.arr_reference),
                                                ctypes.pointer(
                                                    other.arr_reference),
                                                ctypes.pointer(result),
                                                ctypes.pointer(error_code),
                                                error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __and__(self, other):
        """
        Return self & other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_bitand(ctypes.pointer(self.arr_reference),
                                                    ctypes.pointer(
                                                        other.arr_reference),
                                                    ctypes.pointer(result),
                                                    ctypes.pointer(error_code),
                                                    error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __iand__(self, other):
        """
        Perform self &= other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_bitand(ctypes.pointer(self.arr_reference),
                                                    ctypes.pointer(
                                                        other.arr_reference),
                                                    ctypes.pointer(result),
                                                    ctypes.pointer(error_code),
                                                    error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __or__(self, other):
        """
        Return self | other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_bitor(ctypes.pointer(self.arr_reference),
                                                   ctypes.pointer(
                                                       other.arr_reference),
                                                   ctypes.pointer(result),
                                                   ctypes.pointer(error_code),
                                                   error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __ior__(self, other):
        """
        Perform self |= other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_bitor(ctypes.pointer(self.arr_reference),
                                                   ctypes.pointer(
                                                       other.arr_reference),
                                                   ctypes.pointer(result),
                                                   ctypes.pointer(error_code),
                                                   error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __xor__(self, other):
        """
        Return self ^ other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_bitxor(ctypes.pointer(self.arr_reference),
                                                    ctypes.pointer(
                                                        other.arr_reference),
                                                    ctypes.pointer(result),
                                                    ctypes.pointer(error_code),
                                                    error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __ixor__(self, other):
        """
        Perform self ^= other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_bitxor(ctypes.pointer(self.arr_reference),
                                                    ctypes.pointer(
                                                        other.arr_reference),
                                                    ctypes.pointer(result),
                                                    ctypes.pointer(error_code),
                                                    error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __lshift__(self, other):
        """
        Return self << other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_bitshiftl(ctypes.pointer(self.arr_reference),
                                                       ctypes.c_int32(other),
                                                       ctypes.pointer(result),
                                                       ctypes.pointer(
                                                           error_code),
                                                       error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __ilshift__(self, other):
        """
        Perform self <<= other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_bitshiftl(ctypes.pointer(self.arr_reference),
                                                       ctypes.c_int32(other),
                                                       ctypes.pointer(result),
                                                       ctypes.pointer(
                                                           error_code),
                                                       error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __rshift__(self, other):
        """
        Return self >> other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_bitshiftr(ctypes.pointer(self.arr_reference),
                                                       ctypes.c_int32(other),
                                                       ctypes.pointer(result),
                                                       ctypes.pointer(
                                                           error_code),
                                                       error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __irshift__(self, other):
        """
        Perform self >>= other.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_bitshiftr(ctypes.pointer(self.arr_reference),
                                                       ctypes.c_int32(other),
                                                       ctypes.pointer(result),
                                                       ctypes.pointer(
                                                           error_code),
                                                       error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def __neg__(self):
        """
        Return -self
        """
        type_ = self.get_type()
        return Array.from_numpy(
            np.zeros(self.get_dims(), dtype=_get_numpy_type(type_.value)), type_) - self

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
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_not(ctypes.pointer(self.arr_reference),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)

        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def _get_metadata_str(self, dims=True):
        return 'khiva.Array()\nType: {}\n{}' \
            .format(self.khiva_type, 'Dims: {}'.format(str(self.dims)) if dims else '')

    def __str__(self):
        """
        Converts the khiva array to string showing its meta data and contents.
        """

        return self._get_metadata_str()

    def __bool__(self):
        """
        Returns if the Array is non-zero.
        """
        type_ = self.get_type()
        ne = self != Array.from_numpy(
            np.zeros(self.get_dims(), dtype=_get_numpy_type(type_.value)), type_)
        ne_host = ne.to_numpy()
        return bool(np.all(ne_host))

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
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_transpose(ctypes.pointer(self.arr_reference),
                                                       ctypes.c_bool(
                                                           conjugate),
                                                       ctypes.pointer(result),
                                                       ctypes.pointer(
                                                           error_code),
                                                       error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def get_col(self, index):
        """
        Gets a desired column.

        :param index: Index of the desired column.
        :return: The desired column.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_col(ctypes.pointer(self.arr_reference),
                                                 ctypes.c_int32(index),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def get_cols(self, first, last):
        """
        Gets a sequence of columns using the first column index and the last column index, both columns included.

        :param first: First column of the subsequence of columns.
        :param last: Last column of the subsequence of columns.
        :return: A subsequence of columns between 'first' and 'last'.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_cols(ctypes.pointer(self.arr_reference),
                                                  ctypes.c_int32(first),
                                                  ctypes.c_int32(last),
                                                  ctypes.pointer(result),
                                                  ctypes.pointer(error_code),
                                                  error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def get_row(self, index):
        """
        Gets a desired row.

        :param index: Index of the desired row.
        :return: The desired row.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_row(ctypes.pointer(self.arr_reference),
                                                 ctypes.c_int32(index),
                                                 ctypes.pointer(result),
                                                 ctypes.pointer(error_code),
                                                 error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def get_rows(self, first, last):
        """
        Gets a sequence of rows using the first row index and the last row index, both rows included.

        :param first: First row of the subsequence of rows.
        :param last: Last row of the subsequence of rows.
        :return: A subsequence of rows between 'first' and 'last'.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_rows(ctypes.pointer(self.arr_reference),
                                                  ctypes.c_int32(first),
                                                  ctypes.c_int32(last),
                                                  ctypes.pointer(result),
                                                  ctypes.pointer(error_code),
                                                  error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def matmul(self, other):
        """
        Matrix multiplication.

        :param other: KHIVA Array
        :return: The matrix multiplication between these two KHIVA Arrays.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_matmul(ctypes.pointer(self.arr_reference),
                                                    ctypes.pointer(
                                                        other.arr_reference),
                                                    ctypes.pointer(result),
                                                    ctypes.pointer(error_code),
                                                    error_message)
        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def copy(self):
        """
        Performs a deep copy of the array.

        return: An identical copy of self.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.copy(ctypes.pointer(self.arr_reference),
                                            ctypes.pointer(result),
                                            ctypes.pointer(error_code),
                                            error_message)

        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        return Array(array_reference=result)

    def as_type(self, dtype):
        """
        Converts the array to a desired array with a desired type.

        :param dtype: The desired KHIVA data type.
        :return: An array with the desired data type.
        """
        result = ctypes.c_void_p(0)
        error_code = ctypes.c_int(0)
        error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
        KhivaLibrary().c_khiva_library.khiva_as(ctypes.pointer(self.arr_reference),
                                                ctypes.c_int32(dtype.value),
                                                ctypes.pointer(result),
                                                ctypes.pointer(error_code),
                                                error_message)

        if error_code.value != 0:
            raise Exception(str(error_message.value.decode()))

        self.khiva_type = self.get_type()

        return Array(array_reference=result)
