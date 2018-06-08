# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import ctypes
from khiva.library import KhivaLibrary
from khiva.array import Array


########################################################################################################################

def find_best_n_discords(profile, index, n):
    """ This function extracts the best N motifs from a previously calculated matrix profile.

    :param profile: KHIVA array with the matrix profile containing the minimum distance of each subsequence.
    :param index: KHIVA array with the matrix profile index containing where each minimum occurs.
    :param n: Number of discords to extract.
    :return: KHIVA arrays with the discord distances, the discord indices and the subsequence indices.
    """
    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)
    d = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.find_best_n_discords(ctypes.pointer(profile.arr_reference),
                                                        ctypes.pointer(index.arr_reference),
                                                        ctypes.pointer(ctypes.c_long(n)),
                                                        ctypes.pointer(b),
                                                        ctypes.pointer(c),
                                                        ctypes.pointer(d))

    return Array(array_reference=b), Array(array_reference=c), Array(
        array_reference=d)


def find_best_n_motifs(profile, index, n):
    """ This function extracts the best N discords from a previously calculated matrix profile.

    :param profile: KHIVA array with the matrix profile containing the minimum distance of each subsequence.
    :param index: KHIVA array with the matrix profile index containing where each minimum occurs.
    :param n: Number of motifs to extract.
    :return: KHIVA arrays with the motif distances, the motif indices and the subsequence indices.
    """
    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)
    d = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.find_best_n_motifs(ctypes.pointer(profile.arr_reference),
                                                      ctypes.pointer(index.arr_reference),
                                                      ctypes.pointer(ctypes.c_long(n)),
                                                      ctypes.pointer(b),
                                                      ctypes.pointer(c),
                                                      ctypes.pointer(d))

    return Array(array_reference=b), Array(array_reference=c), Array(
        array_reference=d)


def stomp(first_time_series, second_time_series, subsequence_length):
    """ Stomp algorithm to calculate the matrix profile between `ta` and `tb` using a subsequence length of `m`.

    :param first_time_series: KHIVA array with the first time series.
    :param second_time_series: KHIVA array with the second time series.
    :param subsequence_length: Length of the subsequence.
    :return: KHIVA arrays with the profile and index.
    """

    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.stomp(ctypes.pointer(first_time_series.arr_reference),
                                         ctypes.pointer(second_time_series.arr_reference),
                                         ctypes.pointer(ctypes.c_long(subsequence_length)),
                                         ctypes.pointer(b),
                                         ctypes.pointer(c))

    return Array(array_reference=b), Array(array_reference=c)


def stomp_self_join(time_series, subsequence_length):
    """ Stomp algorithm to calculate the matrix profile between `t` and itself using a subsequence length of `m`.
    This method filters the trivial matches.

    :param time_series: The query and reference time series in KHIVA array format.
    :param subsequence_length: Lenght of the subsequence
    :return: KHIVA arrays with the profile and index.
    """
    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.stomp_self_join(ctypes.pointer(time_series.arr_reference),
                                                   ctypes.pointer(ctypes.c_long(subsequence_length)),
                                                   ctypes.pointer(b),
                                                   ctypes.pointer(c))

    return Array(array_reference=b), Array(array_reference=c)
