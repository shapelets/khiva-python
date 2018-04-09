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
from tsa.tsa_libraries.library import TsaLibrary


########################################################################################################################

def znorm(tss, epsilon=0.00000001):
    """ Calculates a new set of timeseries with zero mean and standard deviation one.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param epsilon: Minimum standard deviation to consider.  It acts as a gatekeeper for those time series that
           may be constant or near constant.

    :return: Numpy array with the same dimensions as tss where the time series have been adjusted for zero mean and
            one as standard deviation.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_n = len(tss)
    tss_l = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_n)
    tss_c_length = ctypes.c_long(tss_l)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)

    result_initialized = np.zeros(tss_n * tss_l).astype(np.double)
    result_c_initialized = (ctypes.c_double * (tss_n * tss_l))(*result_initialized)
    TsaLibrary().c_tsa_library.znorm(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                     ctypes.pointer(tss_c_number_of_ts), ctypes.pointer(ctypes.c_double(epsilon)),
                                     ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def znorm_in_place(tss, epsilon=0.00000001):
    """ Adjusts the time series in the given input and performs z-norm
    inplace (without allocating further memory).

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param epsilon: epsilon Minimum standard deviation to consider.  It acts as a gatekeeper for
    those time series that may be constant or near constant.
    """
    if isinstance(tss, list):
        tss = np.array(tss).astype(np.double)
    tss_n = len(tss)
    tss_l = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_n)
    tss_c_length = ctypes.c_long(tss_l)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)

    TsaLibrary().c_tsa_library.znorm_in_place(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                              ctypes.pointer(tss_c_number_of_ts),
                                              ctypes.pointer(ctypes.c_double(epsilon)))
    tss_result = np.array(tss_c_joint)
    for i in range(tss_n):
        tss[i] = tss_result[(i * tss_l):((i + 1) * tss_l)]

    return tss
