# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

########################################################################################################################
# IMPORT
########################################################################################################################
import numpy as np
import ctypes
from tsa.library import TsaLibrary
from enum import Enum
import pandas as pd
import logging
import sys


########################################################################################################################

class dtype(Enum):
    """
    TSA array available types.
    """
    f32 = 0
    """
    Float. tsa.dtype
    """
    c32 = 1
    """
    32 bits Complex. tsa.dtype
    """
    f64 = 2
    """
    64 bits Double. tsa.dtype
    """
    c64 = 3
    """
    64 bits Complex. tsa.dtype
    """
    b8 = 4
    """
    Boolean. tsa.dtype
    """
    s32 = 5
    """
    32 bits Int. tsa.dtype
    """
    u32 = 6
    """
    32 bits Unsigned Int. tsa.dtype
    """
    u8 = 7
    """
    8 bits Unsigned Int. tsa.dtype
    """
    s64 = 8
    """
    64 bits Integer. tsa.dtype
    """
    u64 = 9
    """
    64 bits Unsigned Int. tsa.dtype
    """
    s16 = 10
    """
    16 bits Int. tsa.dtype
    """
    u16 = 11
    """
    16 bits Unsigned int. tsa.dtype
    """


def _get_array_type(tsa_type):
    """
    Transform the TSA type to its equivalent in ctypes.

    :param tsa_type: TSA type.

    :return: The ctypes equivalent.
    """
    return {
        dtype.f32.value: ctypes.c_float,
        dtype.f64.value: ctypes.c_double,
        dtype.b8.value: ctypes.c_bool,
        dtype.u8.value: ctypes.c_uint8,
        dtype.s16.value: ctypes.c_int16,
        dtype.u16.value: ctypes.c_uint16,
        dtype.s32.value: ctypes.c_int32,
        dtype.u32.value: ctypes.c_uint32,
        dtype.s64.value: ctypes.c_int64,
        dtype.u64.value: ctypes.c_uint64,
        dtype.c32.value: (2 * ctypes.c_float),
        dtype.c64.value: (2 * ctypes.c_double)

    }[tsa_type]


def _get_numpy_type(tsa_type):
    """
     Transform the TSA type to its equivalent in Numpy.

    :param tsa_type: TSA type.

    :return: The Numpy type equivalent.
    """
    return {
        dtype.f32.value: np.float,
        dtype.f64.value: np.double,
        dtype.b8.value: np.bool,
        dtype.u8.value: np.uint8,
        dtype.s16.value: np.int8,
        dtype.u16.value: np.uint16,
        dtype.s32.value: np.int16,
        dtype.u32.value: np.uint32,
        dtype.s64.value: np.int64,
        dtype.u64.value: np.uint64,
    }[tsa_type]


class array:
    __array_priority__ = 50

    def __init__(self, data=None, tsa_type=dtype.f32, array_reference=None):
        """
        Creates a TSA array in one of the following ways: 1) using a previously created array; or 2) with data (in
        numpy, list, or pandas dataframe format)

        :param data: Numpy array, List of elements or a Pandas dataframe.
        :param tsa_type: TSA type.
        :param array_reference: Reference of the array.
        """
        if array_reference is None:
            self.tsa_type = tsa_type
            self.arr_reference = self._create_array(data)
            self.dims = self.get_dims()
            self.result_l = self._get_result_length()

        else:
            self.tsa_type = tsa_type
            self.arr_reference = array_reference
            self.dims = self.get_dims()
            self.result_l = self._get_result_length()

        self.arrayfire_reference = False

    def get_dims(self):
        """ Gets the dimensions of the TSA array.

        :return: The dimensions of the TSA array.
        """
        c_array_n = (ctypes.c_long * 4)(*(np.zeros(4)).astype(np.long))
        TsaLibrary().c_tsa_library.get_dims(ctypes.pointer(self.arr_reference), ctypes.pointer(c_array_n))
        return np.array(c_array_n)

    def _get_result_length(self):
        """ Gets the length of the result.

        :return: The length of the result, used in order to get the data to the host.
        """
        result = 1
        for value in self.dims:
            result *= value

        return result

    def _create_array(self, data):
        """ Creates the TSA array in the device.

        :param data: The data used for creating the tsa array.
        :return An opaque pointer to the Array.
        """
        if isinstance(data, list):
            data = np.array(data)
        if isinstance(data, pd.DataFrame):
            data = data.as_matrix(data)
        shape = np.shape(data)[::-1]
        c_array_n = (ctypes.c_long * len(shape))(*(np.array(shape)).astype(np.long))
        c_ndims = ctypes.c_uint(len(shape))
        try:
            array_joint = np.concatenate(data, axis=0)
            c_array_joint = (_get_array_type(self.tsa_type.value) * len(array_joint))(*array_joint)
        except:
            c_array_joint = (_get_array_type(self.tsa_type.value) * len(data))(*data)
        opaque_pointer = ctypes.c_void_p(0)
        TsaLibrary().c_tsa_library.create_array(ctypes.pointer(c_array_joint),
                                                ctypes.pointer(c_ndims),
                                                ctypes.pointer(c_array_n),
                                                ctypes.pointer(opaque_pointer),
                                                ctypes.pointer(ctypes.c_int(self.tsa_type.value)))
        return opaque_pointer

    def _get_data(self):
        """ Retrieves the data from the device to the host.

        :return A numpy array with the data.
        """
        initialized_result_array = np.zeros(self.result_l).astype(_get_array_type(self.tsa_type.value))
        c_result_array = (_get_array_type(self.tsa_type.value) * self.result_l)(*initialized_result_array)
        TsaLibrary().c_tsa_library.get_data(ctypes.pointer(self.arr_reference), ctypes.pointer(c_result_array))
        return np.array(c_result_array)

    def to_numpy(self):
        """ Converts the TSA array to a numpy array.

        :return: TSA array converted to numpy.array.
        """
        return np.array(np.split(self._get_data(), self.dims[1]))

    def to_list(self):
        """ Converts the TSA array to a list.

        :return: TSA array converted to list.
        """
        return np.split(self._get_data(), self.dims[1])

    def to_pandas(self):
        """ Converts the TSA array to a pandas dataframe.

        :return: TSA array converted to a pandas dataframe.
        """
        return pd.DataFrame(data=np.split(self._get_data(), self.dims[1]))

    def to_arrayfire(self):
        """ Creates an Arrayfire array from this TSA array. This need to be used carefully as the same array
        reference is oging to be used by both of them. Once the Arrayfire array is created, the destructor of
        the TSA array is not going to free the allocated array.

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

    def print(self):
        """
        Prints the data stored in the TSA array.
        """
        TsaLibrary().c_tsa_library.print(ctypes.pointer(self.arr_reference))

    def __len__(self):
        return self.result_l

    def __del__(self):
        if not self.arrayfire_reference:
            TsaLibrary().c_tsa_library.delete_array(ctypes.pointer(self.arr_reference))
