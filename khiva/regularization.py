# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import ctypes
from khiva.library import KhivaLibrary
from khiva.array import Array


########################################################################################################################

def group_by(tss, aggregation_function, n_columns_key=1, n_columns_value=1):
    """ Group by operation in the input array using n_columns_key columns as group keys and n_columns_value columns as
    values. The data is expected to be sorted. The aggregation function determines the operation to aggregate the
    values.

    :param tss: KHIVA array with the time series.
    :param aggregation_function: Function to be used in the aggregation. It receives an integer which indicates
                                the function to be applied.
                                0 : mean,
                                1 : median
                                2 : min,
                                3 : max,
                                4 : stdev,
                                5 : var,
                                default : mean
    :param n_columns_key: Number of columns conforming the key.
    :param n_columns_value: Number of columns conforming the value (they are expected to be consecutive to the column
                            keys).

    :return: KHIVA array with the values of the group keys aggregated using the aggregation_function.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.group_by(ctypes.pointer(tss.arr_reference),
                                            ctypes.pointer(ctypes.c_int(aggregation_function)),
                                            ctypes.pointer(ctypes.c_int(n_columns_key)),
                                            ctypes.pointer(ctypes.c_int(n_columns_value)),
                                            ctypes.pointer(b))

    return Array(array_reference=b)
