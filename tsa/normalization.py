# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import ctypes
import numpy as np
from tsa.library import TsaLibrary
from tsa.array import array, dtype


########################################################################################################################

def znorm(tss, epsilon=0.00000001):
    """ Calculates a new set of timeseries with zero mean and standard deviation one.

    :param tss: TSA array with the time series.
    :param epsilon: Minimum standard deviation to consider.  It acts as a gatekeeper for those time series that
           may be constant or near constant.

    :return: TSA array with the same dimensions as tss where the time series have been adjusted for zero mean and
            one as standard deviation.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.znorm(ctypes.pointer(tss.arr_reference), ctypes.pointer(ctypes.c_double(epsilon)),
                                     ctypes.pointer(b))

    return array(array_reference=b, tsa_type=tss.tsa_type)


def znorm_in_place(tss, epsilon=0.00000001):
    """ Adjusts the time series in the given input and performs z-norm
    inplace (without allocating further memory).

    :param tss: TSA array with the time series.
    :param epsilon: epsilon Minimum standard deviation to consider.  It acts as a gatekeeper for
                    those time series that may be constant or near constant.
    """
    TsaLibrary().c_tsa_library.znorm_in_place(ctypes.pointer(tss.arr_reference),
                                              ctypes.pointer(ctypes.c_double(epsilon)))
