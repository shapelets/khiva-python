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
########################################################################################################################

def _stomp(first_time_series_list, second_time_series_list, subsequence_length, c_tsa_library):
    """
    STOMP algorithm to calculate the matrix profile between 'ta' and 'tb' using a subsequence length
          of 'm'.
    :param first_time_series_list: List with the first time series.
    :param second_time_series_list: List with the second time series.
    :param subsequence_length: Length of the subsequence.
    :param c_tsa_library: Dynamic library of TSA.
    :return: Matrix profile in dictionary format.
    """
    first_time_series_double_array = (ctypes.c_double * len(first_time_series_list))(*first_time_series_list)

    second_time_series_double_array = (ctypes.c_double * len(second_time_series_list))(*second_time_series_list)

    initialized_mp_numpy_array = np.zeros(len(second_time_series_list) - subsequence_length + 1).astype(np.double)
    initialized_ip_numpy_array = np.zeros(len(second_time_series_list) - subsequence_length + 1).astype(np.uint32)

    initialized_c_mp_array = (ctypes.c_double * (len(second_time_series_list) - subsequence_length + 1)) \
        (*initialized_mp_numpy_array)

    initialized_c_ip_array = (ctypes.c_uint32 * ((len(second_time_series_list)) - subsequence_length + 1)) \
        (*initialized_ip_numpy_array)

    c_tsa_library.stomp(ctypes.pointer(first_time_series_double_array),
                        ctypes.pointer(second_time_series_double_array),
                        ctypes.pointer(ctypes.c_int(len(first_time_series_list))),
                        ctypes.pointer(ctypes.c_int(len(second_time_series_list))),
                        ctypes.pointer(ctypes.c_long(subsequence_length)),
                        ctypes.pointer(initialized_c_mp_array),
                        ctypes.pointer(initialized_c_ip_array))

    np_array_mp = np.array(initialized_c_mp_array)
    np_array_ip = np.array(initialized_c_ip_array).astype(int)

    return {'matrix_profile': np_array_mp, 'index_profile': np_array_ip}
