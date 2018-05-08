# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

########################################################################################################################
# IMPORT
########################################################################################################################
import ctypes
from tsa.library import TsaLibrary
from tsa.array import array


########################################################################################################################


def euclidean(tss):
    """ Calculates euclidean distances between time series.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and
                dimension one indicates the number of time series.
    :return: Array with an upper triangular matrix where each position corresponds to the distance between two
            time series. Diagonal elements will be zero. For example: Position row 0 column 1 records the distance
            between time series 0 and time series 1.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.euclidean(ctypes.pointer(tss.arr_reference),
                                         ctypes.pointer(b))
    return array(array_reference=b)


def dtw(tss):
    """ Calculates the Dynamic Time Warping Distance.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and
                dimension one indicates the number of time series.
    :return: Array with an upper triangular matrix where each position corresponds to the distance between
            two time series. Diagonal elements will be zero. For example: Position row 0 column 1 records the
            distance between time series 0 and time series 1.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.dtw(ctypes.pointer(tss.arr_reference),
                                   ctypes.pointer(b))
    return array(array_reference=b)


def hamming(tss):
    """ Calculates hamming distances between time series.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and
                dimension one indicates the number of time series.
    :return: Array with an upper triangular matrix where each position corresponds to the distance between two
            time series. Diagonal elements will be zero. For example: Position row 0 column 1 records the distance
            between time series 0 and time series 1.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.hamming(ctypes.pointer(tss.arr_reference),
                                       ctypes.pointer(b))
    return array(array_reference=b)


def manhattan(tss):
    """ Calculates manhattan distances between time series.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and
                dimension one indicates the number of time series.
    :return: Array with an upper triangular matrix where each position corresponds to the distance between two
            time series. Diagonal elements will be zero. For example: Position row 0 column 1 records the distance
            between time series 0 and time series 1.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.manhattan(ctypes.pointer(tss.arr_reference),
                                         ctypes.pointer(b))
    return array(array_reference=b)


def squared_euclidean(tss):
    """ Calculates non squared version of the euclidean distance.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and
                dimension one indicates the number of time series.
    :return: Array with an upper triangular matrix where each position corresponds to the distance between two time series.
            Diagonal elements will be zero. For example: Position row 0 column 1 records the distance between time series 0
            and time series 1.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.squared_euclidean(ctypes.pointer(tss.arr_reference),
                                                 ctypes.pointer(b))
    return array(array_reference=b)

