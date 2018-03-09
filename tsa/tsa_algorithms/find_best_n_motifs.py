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

def _find_best_n_motifs(profile_list, index_list, n, c_tsa_library):
    """
    Primitive of the findBestNMotifs function

    :param profile_list: The matrix profile containing the minimum distance of each subsequence
    :param index_list: The matrix profile index containing where each minimum occurs
    :param n: Number of motifs to extract
    :param c_tsa_library: tsa Library
    :return: Dictionary with the motif distances, the motif indices and the subsequence indices.
    """
    profile_c_double_array = (ctypes.c_double * len(profile_list))(*profile_list)
    index_c_int_array = (ctypes.c_uint32 * len(index_list))(*index_list)

    initialized_motif_distance_array = np.zeros(n).astype(np.double)
    initialized_motif_index_array = np.zeros(n).astype(np.int)
    initialized_subsequence_index_array = np.zeros(n).astype(np.int)

    c_motif_distance = (ctypes.c_double * n)(*initialized_motif_distance_array)
    c_motif_index = (ctypes.c_int * n)(*initialized_motif_index_array)
    c_subsequence_index = (ctypes.c_int * n)(*initialized_subsequence_index_array)

    c_tsa_library.find_best_n_motifs(ctypes.pointer(profile_c_double_array),
                                     ctypes.pointer(index_c_int_array),
                                     ctypes.pointer(ctypes.c_long(len(profile_list))),
                                     ctypes.pointer(ctypes.c_long(n)),
                                     ctypes.pointer(c_motif_distance),
                                     ctypes.pointer(c_motif_index),
                                     ctypes.pointer(c_subsequence_index))

    np_motif_distance = np.array(c_motif_distance)
    np_motif_index = np.array(c_motif_index).astype(int)
    np_subsequence_index = np.array(c_subsequence_index).astype(int)

    return {'motif_distance': np_motif_distance, 'motif_index': np_motif_index,
            'subsequence_index': np_subsequence_index}
