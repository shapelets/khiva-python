#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
import ctypes
from khiva.library import KhivaLibrary, KHIVA_ERROR_LENGTH
from khiva.array import Array
from collections import namedtuple


########################################################################################################################
MatrixProfileResult = namedtuple("MatrixProfileResult", ["profile", "index"])
BestNResult = namedtuple(
    "BestNResult", ["distances", "indexes", "subsequence_indexes"])
BestNResultOcurrences = namedtuple(
    "BestNResultOcurrences", ["distances", "indexes"])


def find_best_n_discords(profile, index, m, n, self_join=False):
    """ This function extracts the best N motifs from a previously calculated matrix profile.

    :param profile: KHIVA array with the matrix profile containing the minimum distance of each subsequence.
    :param index: KHIVA array with the matrix profile index containing where each minimum occurs.
    :param m: Subsequence length value used to calculate the input matrix profile.
    :param n: Number of discords to extract.
    :param self_join: Indicates whether the input profile comes from a self join operation or not. It determines
                      whether the mirror similar region is included in the output or not.
    :return: KHIVA arrays with the discord distances, the discord indexes and the subsequence indexes.
    """
    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)
    d = ctypes.c_void_p(0)

    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.find_best_n_discords(ctypes.pointer(profile.arr_reference),
                                                        ctypes.pointer(
                                                            index.arr_reference),
                                                        ctypes.c_long(m),
                                                        ctypes.c_long(n),
                                                        ctypes.pointer(b),
                                                        ctypes.pointer(c),
                                                        ctypes.pointer(d),
                                                        ctypes.c_bool(
                                                            self_join),
                                                        ctypes.pointer(
                                                            error_code),
                                                        error_message)
    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))

    return BestNResult(distances=Array(b), indexes=Array(c), subsequence_indexes=Array(d))


def find_best_n_motifs(profile, index, m, n, self_join=False):
    """ This function extracts the best N discords from a previously calculated matrix profile.

    :param profile: KHIVA array with the matrix profile containing the minimum distance of each subsequence.
    :param index: KHIVA array with the matrix profile index containing where each minimum occurs.
    :param m: Subsequence length value used to calculate the input matrix profile.
    :param n: Number of motifs to extract.
    :param self_join: Indicates whether the input profile comes from a self join operation or not. It determines
                      whether the mirror similar region is included in the output or not.
    :return: KHIVA arrays with the motif distances, the motif indexes and the subsequence indexes.
    """
    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)
    d = ctypes.c_void_p(0)

    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.find_best_n_motifs(ctypes.pointer(profile.arr_reference),
                                                      ctypes.pointer(
                                                          index.arr_reference),
                                                      ctypes.c_long(m),
                                                      ctypes.c_long(n),
                                                      ctypes.pointer(b),
                                                      ctypes.pointer(c),
                                                      ctypes.pointer(d),
                                                      ctypes.c_bool(self_join),
                                                      ctypes.pointer(
                                                          error_code),
                                                      error_message)
    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))

    return BestNResult(distances=Array(b), indexes=Array(c), subsequence_indexes=Array(d))


def find_best_n_occurrences(query_time_series, time_series, number_of_occurrences):
    """ Calculates the N best matches of several queries in several time series.

     The result has the following structure:
        - 1st dimension corresponds to the nth best match.
        - 2nd dimension corresponds to the number of queries.
        - 3rd dimension corresponds to the number of time series.

    For example, the distance in the position (1, 2, 3) corresponds to the second best distance of the third query in the
    fourth time series. The index in the position (1, 2, 3) is the index of the subsequence which leads to the
    second best distance of the third query in the fourth time series.

    :param query_time_series: Array whose first dimension is the length of the query time series and the second
    dimension is the number of queries.
    :param time_series: Array whose first dimension is the length of the time series and the second dimension is the
    number of time series.
    :param number_of_occurrences: Number of matches to return.
    :return: KHIVA arrays with the distances and indexes.
    """

    distances = ctypes.c_void_p(0)
    indexes = ctypes.c_void_p(0)
    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.find_best_n_occurrences(ctypes.pointer(query_time_series.arr_reference),
                                                           ctypes.pointer(
                                                               time_series.arr_reference),
                                                           ctypes.c_long(
                                                               number_of_occurrences),
                                                           ctypes.pointer(
                                                               distances),
                                                           ctypes.pointer(
                                                               indexes),
                                                           ctypes.pointer(
                                                               error_code),
                                                           error_message)
    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))

    return BestNResultOcurrences(distances=Array(distances), indexes=Array(indexes))


def mass(query_time_series, time_series):
    """ Mueen's Algorithm for Similarity Search.

     The result has the following structure:
        - 1st dimension corresponds to the index of the subsequence in the time series.
        - 2nd dimension corresponds to the number of queries.
        - 3rd dimension corresponds to the number of time series.

    For example, the distance in the position (1, 2, 3) correspond to the distance of the third query to the fourth time
    series for the second subsequence in the time series.

    :param query_time_series: Array whose first dimension is the length of the query time series and the second
    dimension is the number of queries.
    :param time_series: Array whose first dimension is the length of the time series and the second dimension is the
    number of time series.
    :return: KHIVA array with the distances.
    """

    distances = ctypes.c_void_p(0)
    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.mass(ctypes.pointer(query_time_series.arr_reference),
                                        ctypes.pointer(
                                            time_series.arr_reference),
                                        ctypes.pointer(distances),
                                        ctypes.pointer(error_code),
                                        error_message)
    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))

    return Array(array_reference=distances)


def stomp(first_time_series, second_time_series, subsequence_length):
    """ Stomp algorithm to calculate the matrix profile between `ta` and `tb` using a subsequence length of `m`.

    [1] Yan Zhu, Zachary Zimmerman, Nader Shakibay Senobari, Chin-Chia Michael Yeh, Gareth Funning, Abdullah Mueen,
    Philip Brisk and Eamonn Keogh (2016). Matrix Profile II: Exploiting a Novel Algorithm and GPUs to break the one
    Hundred Million Barrier for Time Series Motifs and Joins. IEEE ICDM 2016.

    :param first_time_series: KHIVA array with the first time series.
    :param second_time_series: KHIVA array with the second time series.
    :param subsequence_length: Length of the subsequence.
    :return: KHIVA arrays with the profile and index.
    """

    profile = ctypes.c_void_p(0)
    index = ctypes.c_void_p(0)

    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.stomp(ctypes.pointer(first_time_series.arr_reference),
                                         ctypes.pointer(
                                             second_time_series.arr_reference),
                                         ctypes.c_long(subsequence_length),
                                         ctypes.pointer(profile),
                                         ctypes.pointer(index),
                                         ctypes.pointer(error_code),
                                         error_message)
    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))

    return MatrixProfileResult(profile=Array(profile), index=Array(index))


def stomp_self_join(time_series, subsequence_length):
    """ Stomp algorithm to calculate the matrix profile between `t` and itself using a subsequence length of `m`.
    This method filters the trivial matches.

    [1] Yan Zhu, Zachary Zimmerman, Nader Shakibay Senobari, Chin-Chia Michael Yeh, Gareth Funning, Abdullah Mueen,
    Philip Brisk and Eamonn Keogh (2016). Matrix Profile II: Exploiting a Novel Algorithm and GPUs to break the one
    Hundred Million Barrier for Time Series Motifs and Joins. IEEE ICDM 2016.

    :param time_series: The query and reference time series in KHIVA array format.
    :param subsequence_length: Lenght of the subsequence
    :return: KHIVA arrays with the profile and index.
    """
    profile = ctypes.c_void_p(0)
    index = ctypes.c_void_p(0)

    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.stomp_self_join(ctypes.pointer(time_series.arr_reference),
                                                   ctypes.c_long(
                                                       subsequence_length),
                                                   ctypes.pointer(profile),
                                                   ctypes.pointer(index),
                                                   ctypes.pointer(error_code),
                                                   error_message)
    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))
    return MatrixProfileResult(profile=Array(profile), index=Array(index))


def matrix_profile(first_time_series, second_time_series, subsequence_length):
    """ Calculate the matrix profile between `ta` and `tb` using a subsequence length of `m`.

    [1] Yan Zhu, Zachary Zimmerman, Nader Shakibay Senobari, Chin-Chia Michael Yeh, Gareth Funning, Abdullah Mueen,
    Philip Brisk and Eamonn Keogh (2016). Matrix Profile II: Exploiting a Novel Algorithm and GPUs to break the one
    Hundred Million Barrier for Time Series Motifs and Joins. IEEE ICDM 2016.

    :param first_time_series: KHIVA array with the first time series.
    :param second_time_series: KHIVA array with the second time series.
    :param subsequence_length: Length of the subsequence.
    :return: KHIVA arrays with the profile and index.
    """

    profile = ctypes.c_void_p(0)
    index = ctypes.c_void_p(0)

    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.matrix_profile(ctypes.pointer(first_time_series.arr_reference),
                                                  ctypes.pointer(
                                                      second_time_series.arr_reference),
                                                  ctypes.c_long(
                                                      subsequence_length),
                                                  ctypes.pointer(profile),
                                                  ctypes.pointer(index),
                                                  ctypes.pointer(error_code),
                                                  error_message)
    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))

    return MatrixProfileResult(profile=Array(profile), index=Array(index))


def matrix_profile_self_join(time_series, subsequence_length):
    """ Calculate the matrix profile between `t` and itself using a subsequence length of `m`.
    This method filters the trivial matches.

    [1] Yan Zhu, Zachary Zimmerman, Nader Shakibay Senobari, Chin-Chia Michael Yeh, Gareth Funning, Abdullah Mueen,
    Philip Brisk and Eamonn Keogh (2016). Matrix Profile II: Exploiting a Novel Algorithm and GPUs to break the one
    Hundred Million Barrier for Time Series Motifs and Joins. IEEE ICDM 2016.

    :param time_series: The query and reference time series in KHIVA array format.
    :param subsequence_length: Lenght of the subsequence
    :return: KHIVA arrays with the profile and index.
    """
    profile = ctypes.c_void_p(0)
    index = ctypes.c_void_p(0)

    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.matrix_profile_self_join(ctypes.pointer(time_series.arr_reference),
                                                            ctypes.c_long(
                                                                subsequence_length),
                                                            ctypes.pointer(profile),
                                                            ctypes.pointer(index),
                                                            ctypes.pointer(
                                                                error_code),
                                                            error_message)
    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))

    return MatrixProfileResult(profile=Array(profile), index=Array(index))


def get_chains(time_series, subsequence_length):
    """ Calculate all the chains within `tss` using a subsequence length of `m`.

     [1] Yan Zhu, Makoto Imamura, Daniel Nikovski, and Eamonn Keogh. Matrix Profile VII: Time Series Chains: A New
     Primitive for Time Series Data Mining. IEEE ICDM 2017

     :param time_series: Time series to compute the chains within them.
     :param subsequence_length: Subsequence length.
     :return: The calculated chains in a KHIVA array with the following topology:
          - 1st dimension corresponds to the chains indexes flattened.
          - 2nd dimension:
            - [0] corresponds to all the indexes in the chains flattened
            - [1] corresponds to the index of the chain that the value in [0] belongs to.
          - 3rd dimension corresponds to the number of time series.

          Notice that the size of the first dimension is the maximum possible size which is n - m + 1. If the number of
          values belonging to a chain is lower than the maximum, the remaining values and indexes are 0. It implies
          that 0 is an invalid chain index.
    """
    c = ctypes.c_void_p(0)

    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.get_chains(ctypes.pointer(time_series.arr_reference),
                                              ctypes.c_long(
                                                  subsequence_length),
                                              ctypes.pointer(c),
                                              ctypes.pointer(error_code),
                                              error_message)
    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))

    return Array(array_reference=c)
