"""
Copyright (c) 2018 Grumpy Cat Software S.L.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

########################################################################################################################
# IMPORT
########################################################################################################################
import ctypes
import numpy as np
from tsa.tsa_libraries.library import tsaLibrary


########################################################################################################################

def abs_energy(list_of_time_series):
    """
    Primitive of the abs_energy function

    :param list_of_time_series: List with the time series.
    :return: Numpy array with the absEnergy.
    """
    list_of_time_series = list(list_of_time_series)
    n = len(list_of_time_series)
    time_series_length = len(list_of_time_series[0])
    c_number_of_time_series = ctypes.c_long(n)

    c_time_series_length = ctypes.c_long(time_series_length)

    initialized_result_array = np.zeros(n).astype(np.double)

    c_result_array = (ctypes.c_double * n)(*initialized_result_array)

    time_series_joint = []
    for time_series in list_of_time_series:
        time_series_joint += time_series

    c_time_series_joint = (ctypes.c_double * len(time_series_joint))(*time_series_joint)

    tsaLibrary().c_tsa_library.abs_energy(ctypes.pointer(c_time_series_joint),
                                          ctypes.pointer(c_time_series_length),
                                          ctypes.pointer(c_number_of_time_series),
                                          ctypes.pointer(c_result_array))

    np_result = np.array(c_result_array)

    return np_result


def absolute_sum_of_changes(list_of_time_series):
    """
    Primitive of the absolute_sum_of_changes function

    :param list_of_time_series: List with the time series.
    :return: Numpy array with the absolute sum of changes.
    """
    list_of_time_series = list(list_of_time_series)
    n = len(list_of_time_series)
    time_series_length = len(list_of_time_series[0])
    c_number_of_time_series = ctypes.c_long(n)

    c_time_series_length = ctypes.c_long(time_series_length)

    initialized_result_array = np.zeros(n).astype(np.double)

    c_result_array = (ctypes.c_double * n)(*initialized_result_array)

    time_series_joint = []
    for time_series in list_of_time_series:
        time_series_joint += time_series

    c_time_series_joint = (ctypes.c_double * len(time_series_joint))(*time_series_joint)

    tsaLibrary().c_tsa_library.absolute_sum_of_changes(ctypes.pointer(c_time_series_joint),
                                                       ctypes.pointer(c_time_series_length),
                                                       ctypes.pointer(c_number_of_time_series),
                                                       ctypes.pointer(c_result_array))

    np_result = np.array(c_result_array)

    return np_result


def c3(tss, lag):
    """
    c3 function.

    :param tss: List of lists with the time series.
    :param lag: The lag.
    :return: The non-linearity value for the given time series.
    """
    tss = list(tss)
    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = []

    for t_s in tss:
        tss_joint += t_s

    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_number_of_ts)(*result_initialized)
    lag_c = ctypes.c_long(lag)
    tsaLibrary().c_tsa_library.c3(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                  ctypes.pointer(tss_c_number_of_ts),
                                  ctypes.pointer(lag_c), ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def cid_ce(tss, z_normalize):
    """
    cid_ce function.

    :param tss: List of lists with the time series.
    :param z_normalize: Controls wheter the time series should be z-normalized or not.
    :return: The complexity value for the given time series.
    """
    tss = list(tss)
    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = []

    for t_s in tss:
        tss_joint += t_s

    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_number_of_ts)(*result_initialized)
    z_normalize_c = ctypes.c_bool(z_normalize)

    tsaLibrary().c_tsa_library.cidCe(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                     ctypes.pointer(tss_c_number_of_ts),
                                     ctypes.pointer(z_normalize_c), ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)
