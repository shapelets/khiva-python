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

def _abs_energy(list_of_time_series, c_tsa_library):
    """
    Primitive of the abs_energy function

    :param list_of_time_series: List with the time series.
    :param c_tsa_library: TSA library.
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

    c_tsa_library.abs_energy(ctypes.pointer(c_time_series_joint),
                             ctypes.pointer(c_time_series_length),
                             ctypes.pointer(c_number_of_time_series),
                             ctypes.pointer(c_result_array))

    np_result = np.array(c_result_array)

    return np_result
