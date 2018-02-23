#
# title           :scrimp.py
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
def scrimp(time_series_list, subsequence_lenght,c_tsa_library):
    """

    :param time_series_list:
    :param subsequence_lenght:
    :param c_tsa_library:
    :return:
    """
    time_series_double_array = (ctypes.c_double * len(time_series_list))(*time_series_list)

    c_subsequence_length = ctypes.c_int(subsequence_lenght)

    initialized_mp_numpy_array = np.zeros(len(time_series_list) - subsequence_lenght)
    initializes_ip_numpy_array = np.zeros(len(time_series_list) - subsequence_lenght)

    initialized_c_mp_array = (ctypes.c_double * (len(time_series_list) - subsequence_lenght))\
        (*initialized_mp_numpy_array)

    initialized_c_ip_array = (ctypes.c_int * ((len(time_series_list)) - (subsequence_lenght)))\
        (*initializes_ip_numpy_array.astype(int))
    c_tsa_library.scrimp(time_series_double_array,  c_subsequence_length,ctypes.c_int(len(time_series_list)),
                         ctypes.pointer(initialized_c_mp_array), ctypes.pointer(initialized_c_ip_array))

    np_array_mp = np.array(initialized_c_mp_array)
    np_array_ip = np.array(initialized_c_ip_array).astype(int)

    return {'matrix_profile': np_array_mp, 'index_profile': np_array_ip}