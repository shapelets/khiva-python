#
# title           :stamp.py
# description     :
# author          :David Cuesta
# company         :Grumpy Cat Software
# date            :
# usage           :
# python_version  :3.6
# ==============================================================================
########################################################################################################################
# IMPORT
########################################################################################################################

import ctypes
import numpy as np
import os
import tsa.tsa_libraries

########################################################################################################################
def stamp(first_time_series_list, second_time_series_list, subsequence_length):
    """

    :param first_time_series_list: list of doubles
    :param second_time_series_list: list of doubles
    :param subsequence_length: int indicating the subsequence length
    :return: Dictionary with the profile and the index profile
    """
    first_time_series_double_array = (ctypes.c_double * len(first_time_series_list))(*first_time_series_list)

    second_time_series_double_array = (ctypes.c_double * len(second_time_series_list))(*second_time_series_list)

    c_subsequence_length = ctypes.c_int(len(first_time_series_list))

    initialized_mp_numpy_array = np.zeros(len(first_time_series_list) - 20)
    initializes_ip_numpy_array = np.zeros(len(first_time_series_list) - 20)

    initialized_c_mp_array = (ctypes.c_double * (len(first_time_series_list) - subsequence_length))\
        (*initialized_mp_numpy_array)

    initialized_c_ip_array = (ctypes.c_int * (int(len(first_time_series_list)) - int(subsequence_length)))\
        (*initializes_ip_numpy_array.astype(int))

    c_tsa_library = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libmylib-cpu.dylib'))

    c_tsa_library.stamp(first_time_series_double_array, second_time_series_double_array, subsequence_length,
                        c_subsequence_length, ctypes.pointer(initialized_c_mp_array),
                        ctypes.pointer(initialized_c_ip_array))

    np_array_mp = np.array(initialized_c_mp_array)
    np_array_ip = np.array(initialized_c_ip_array).astype(int)

    return {'matrix_profile': np_array_mp, 'index_profile' : np_array_ip}


