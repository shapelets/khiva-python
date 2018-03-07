"""
Copyright (c) 2018 Grumpy Cat Software S.L.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import ctypes
import numpy as np


########################################################################################################################
def binding_test(time_series_list, c_tsa_library):

    first_time_series_double_array = (ctypes.c_double * len(time_series_list))(*time_series_list)

    initialized_mp_numpy_array = np.zeros(len(time_series_list)).astype(np.double)

    initialized_c_mp_array = (ctypes.c_double * (len(time_series_list)))\
        (*initialized_mp_numpy_array)

    c_tsa_library.binding_test(ctypes.pointer(first_time_series_double_array),
                                  ctypes.pointer(ctypes.c_int(len(time_series_list))),
                                  ctypes.pointer(initialized_c_mp_array))

    np_array_mp = np.array(initialized_c_mp_array)

    return np_array_mp