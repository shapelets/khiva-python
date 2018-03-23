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
from tsa.tsa_libraries.library import TsaLibrary


########################################################################################################################

def find_best_n_discords(profile, index, n):
    """
    This function extracts the best N motifs from a previously calculated matrix profile

    :param profile: The matrix profile containing the minimum distance of each subsequence
    :param index: The matrix profile index containing where each minimum occurs
    :param n: Number of discords to extract
    :return: Dictionary with the discord distances, the discord indices and the subsequence indices
    """
    if isinstance(profile, list):
        profile = np.array(profile)
    if isinstance(index, list):
        profile = np.array(index)
    profile_c_double_array = (ctypes.c_double * len(profile))(*profile)
    index_c_double_array = (ctypes.c_uint32 * len(index))(*index)

    initialized_discord_distance_array = np.zeros(n).astype(np.double)
    initialized_discord_index_array = np.zeros(n).astype(np.int)
    initialized_subsequence_index_array = np.zeros(n).astype(np.int)

    c_discord_distance = (ctypes.c_double * n)(*initialized_discord_distance_array)
    c_discord_index = (ctypes.c_int * n)(*initialized_discord_index_array)
    c_subsequence_index = (ctypes.c_int * n)(*initialized_subsequence_index_array)

    TsaLibrary().c_tsa_library.find_best_n_discords(ctypes.pointer(profile_c_double_array),
                                                    ctypes.pointer(index_c_double_array),
                                                    ctypes.pointer(ctypes.c_long(len(profile))),
                                                    ctypes.pointer(ctypes.c_long(n)),
                                                    ctypes.pointer(c_discord_distance),
                                                    ctypes.pointer(c_discord_index),
                                                    ctypes.pointer(c_subsequence_index))

    np_discord_distance = np.array(c_discord_distance)
    np_discord_index = np.array(c_discord_index).astype(int)
    np_subsequence_index = np.array(c_subsequence_index).astype(int)

    return {'discord_distance': np_discord_distance, 'discord_index': np_discord_index,
            'subsequence_index': np_subsequence_index}


def find_best_n_motifs(profile, index, n):
    """
    This function extracts the best N discords from a previously calculated matrix profile.

    :param profile: The matrix profile containing the minimum distance of each subsequence
    :param index: The matrix profile index containing where each minimum occurs
    :param n: Number of motifs to extract
    :return: Dictionary with the motif distances, the motif indices and the subsequence indices.
    """
    if isinstance(profile, list):
        profile = np.array(profile)
    if isinstance(index, list):
        profile = np.array(index)
    profile_c_double_array = (ctypes.c_double * len(profile))(*profile)
    index_c_int_array = (ctypes.c_uint32 * len(index))(*index)

    initialized_motif_distance_array = np.zeros(n).astype(np.double)
    initialized_motif_index_array = np.zeros(n).astype(np.int)
    initialized_subsequence_index_array = np.zeros(n).astype(np.int)

    c_motif_distance = (ctypes.c_double * n)(*initialized_motif_distance_array)
    c_motif_index = (ctypes.c_int * n)(*initialized_motif_index_array)
    c_subsequence_index = (ctypes.c_int * n)(*initialized_subsequence_index_array)

    TsaLibrary().c_tsa_library.find_best_n_motifs(ctypes.pointer(profile_c_double_array),
                                                  ctypes.pointer(index_c_int_array),
                                                  ctypes.pointer(ctypes.c_long(len(profile))),
                                                  ctypes.pointer(ctypes.c_long(n)),
                                                  ctypes.pointer(c_motif_distance),
                                                  ctypes.pointer(c_motif_index),
                                                  ctypes.pointer(c_subsequence_index))

    np_motif_distance = np.array(c_motif_distance)
    np_motif_index = np.array(c_motif_index).astype(int)
    np_subsequence_index = np.array(c_subsequence_index).astype(int)

    return {'motif_distance': np_motif_distance, 'motif_index': np_motif_index,
            'subsequence_index': np_subsequence_index}


def stomp(first_time_series, second_time_series, subsequence_length):
    """
    STOMP algorithm to calculate the matrix profile between 'ta' and 'tb' using a subsequence length
          of 'm'.

    :param first_time_series: First time series. It accepts a list of lists or a numpy array with one or
    several time series.
    :param second_time_series: Second time series. It accepts a list of lists or a numpy array with one or
    several time series.
    or a numpy array with the several time series in ndarray format.
    :param subsequence_length: Length of the subsequence.
    :return: Matrix profile in dictionary format.
    """
    if isinstance(first_time_series, list):
        first_time_series = np.array(first_time_series)
    if isinstance(second_time_series, list):
        second_time_series = np.array(second_time_series)
    first_time_series_double_array = (ctypes.c_double * len(first_time_series))(*first_time_series)

    second_time_series_double_array = (ctypes.c_double * len(second_time_series))(*second_time_series)

    initialized_mp_numpy_array = np.zeros(len(second_time_series) - subsequence_length + 1).astype(np.double)
    initialized_ip_numpy_array = np.zeros(len(second_time_series) - subsequence_length + 1).astype(np.uint32)

    initialized_c_mp_array = (ctypes.c_double * (len(second_time_series) - subsequence_length + 1)) \
        (*initialized_mp_numpy_array)

    initialized_c_ip_array = (ctypes.c_uint32 * ((len(second_time_series)) - subsequence_length + 1)) \
        (*initialized_ip_numpy_array)

    TsaLibrary().c_tsa_library.stomp(ctypes.pointer(first_time_series_double_array),
                                     ctypes.pointer(second_time_series_double_array),
                                     ctypes.pointer(ctypes.c_long(len(first_time_series))),
                                     ctypes.pointer(ctypes.c_long(len(second_time_series))),
                                     ctypes.pointer(ctypes.c_long(subsequence_length)),
                                     ctypes.pointer(initialized_c_mp_array),
                                     ctypes.pointer(initialized_c_ip_array))

    np_array_mp = np.array(initialized_c_mp_array)
    np_array_ip = np.array(initialized_c_ip_array).astype(np.uint32)

    return {'matrix_profile': np_array_mp, 'index_profile': np_array_ip}


def stomp_self_join(time_series, subsequence_length):
    """
    STOMP algorithm to calculate the matrix profile between 't' and itself using a subsequence length
          of 'm'. This method filters the trivial matches.

    :param time_series: The query and reference time series. It accepts a list of lists or a numpy array with
    one or several time series.
    :param subsequence_length: Lenght of the subsequence
    :return: Matrix profile in dictionary format.
    """
    if isinstance(time_series, list):
        time_series = np.array(time_series)
    first_time_series_double_array = (ctypes.c_double * len(time_series))(*time_series)

    initialized_mp_numpy_array = np.zeros(len(time_series) - subsequence_length + 1).astype(np.double)
    initializes_ip_numpy_array = np.zeros(len(time_series) - subsequence_length + 1).astype(np.uint32)

    initialized_c_mp_array = (ctypes.c_double * (len(time_series) - subsequence_length + 1)) \
        (*initialized_mp_numpy_array)

    initialized_c_ip_array = (ctypes.c_uint32 * ((len(time_series)) - subsequence_length + 1)) \
        (*initializes_ip_numpy_array)

    TsaLibrary().c_tsa_library.stomp_self_join(ctypes.pointer(first_time_series_double_array),
                                               ctypes.pointer(ctypes.c_long(len(time_series))),
                                               ctypes.pointer(ctypes.c_long(subsequence_length)),
                                               ctypes.pointer(initialized_c_mp_array),
                                               ctypes.pointer(initialized_c_ip_array))

    np_array_mp = np.array(initialized_c_mp_array)
    np_array_ip = np.array(initialized_c_ip_array).astype(int)

    return {'matrix_profile': np_array_mp, 'index_profile': np_array_ip}
