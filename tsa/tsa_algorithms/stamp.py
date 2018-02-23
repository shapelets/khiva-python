#
# title           :test_stamp.py
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
def stamp(first_time_series_list, second_time_series_list, subsequence_length,c_tsa_library):
    """

    :param first_time_series_list:
    :param second_time_series_list:
    :param subsequence_length:
    :param c_tsa_library:
    :return:
    """
    first_time_series_double_array = (ctypes.c_double * len(first_time_series_list))(*first_time_series_list)

    second_time_series_double_array = (ctypes.c_double * len(second_time_series_list))(*second_time_series_list)

    c_subsequence_length = ctypes.c_int(len(first_time_series_list))

    initialized_mp_numpy_array = np.zeros(len(first_time_series_list) - subsequence_length)
    initializes_ip_numpy_array = np.zeros(len(first_time_series_list) - subsequence_length)

    initialized_c_mp_array = (ctypes.c_double * (len(first_time_series_list) - subsequence_length))\
        (*initialized_mp_numpy_array)

    initialized_c_ip_array = (ctypes.c_int * ((len(first_time_series_list)) - (subsequence_length)))\
        (*initializes_ip_numpy_array.astype(int))

    c_tsa_library.stamp(first_time_series_double_array, second_time_series_double_array, subsequence_length,
                        c_subsequence_length, ctypes.pointer(initialized_c_mp_array),
                        ctypes.pointer(initialized_c_ip_array))
    np_array_mp = np.array(initialized_c_mp_array)
    np_array_ip = np.array(initialized_c_ip_array).astype(int)



    return {'matrix_profile': np_array_mp, 'index_profile': np_array_ip}



