#
# title           :stomp_self_join.py
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
import time
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

########################################################################################################################
def stomp_self_join(time_series_list, subsequence_length, c_tsa_library):
    """
    STAMP algorithm to calculate the matrix profile between 't' and itself using a subsequence length
          of 'm'. This method filters the trivial matches.
    :param time_series_list: List with the query and reference time series.
    :param subsequence_length: Lenght of the subsequence
    :param c_tsa_library: Dynamic library of TSA
    :return: Matrix profile in dictionary format.
    """

    start= time.time()

    first_time_series_double_array = (ctypes.c_double * len(time_series_list))(*time_series_list)

    initialized_mp_numpy_array = np.zeros(len(time_series_list) - subsequence_length +1).astype(np.double)
    initializes_ip_numpy_array = np.zeros(len(time_series_list) - subsequence_length +1).astype(np.uint32)

    initialized_c_mp_array = (ctypes.c_double * (len(time_series_list) - subsequence_length + 1))\
        (*initialized_mp_numpy_array)

    initialized_c_ip_array = (ctypes.c_uint32 * ((len(time_series_list)) - subsequence_length + 1))\
        (*initializes_ip_numpy_array)

    logging.info("Time conversioning to C types:" + str(time.time() - start))

    c_tsa_library.stomp_self_join(ctypes.pointer(first_time_series_double_array),
                                  ctypes.pointer(ctypes.c_int(len(time_series_list))),
                                  ctypes.pointer(ctypes.c_long(subsequence_length)),
                                  ctypes.pointer(initialized_c_mp_array),
                                  ctypes.pointer(initialized_c_ip_array))

    np_array_mp = np.array(initialized_c_mp_array)
    np_array_ip = np.array(initialized_c_ip_array).astype(int)

    return {'matrix_profile': np_array_mp, 'index_profile': np_array_ip}