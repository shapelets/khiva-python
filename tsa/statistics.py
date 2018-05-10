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


def covariance(tss, unbiased=False):
    """ Returns the covariance matrix of the time series contained in tss.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series.
    :param unbiased: Determines whether it divides by n - 1 (if false) or n (if true).
    :return: The covariance matrix of the time series.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.covariance_statistics(ctypes.pointer(tss.arr_reference),
                                                     ctypes.pointer(ctypes.c_bool(unbiased)),
                                                     ctypes.pointer(b))
    return array(array_reference=b)


def moment(tss, k):
    """ Returns the kth moment of the given time series.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series.
    :param k: The specific moment to be calculated.
    :return: The kth moment of the given time series.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.moment_statistics(ctypes.pointer(tss.arr_reference),
                                                 ctypes.pointer(ctypes.c_int(k)),
                                                 ctypes.pointer(b))
    return array(array_reference=b)


def kurtosis(tss):
    """ Returns the kurtosis of tss (calculated with the adjusted Fisher-Pearson standardized moment coefficient G2).

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series.
    :return: The kurtosis of tss.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.kurtosis_statistics(ctypes.pointer(tss.arr_reference),
                                                   ctypes.pointer(b))
    return array(array_reference=b)


def quantile(tss, q, precision=1e8):
    """  Returns values at the given quantile.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series. NOTE: the time series should be sorted.
    :param q: Percentile(s) at which to extract score(s). One or many.
    :param precision: Number of decimals expected.
    :return: Values at the given quantile.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.quantile_statistics(ctypes.pointer(tss.arr_reference),
                                                   ctypes.pointer(q.arr_reference),
                                                   ctypes.pointer(ctypes.c_float(precision)),
                                                   ctypes.pointer(b))
    return array(array_reference=b)


def quantiles_cut(tss, quantiles, precision=1e-8):
    """ Discretizes the time series into equal-sized buckets based on sample quantiles.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series. NOTE: the time series should be sorted.
    :param quantiles: Number of quantiles to extract. From 0 to 1, step 1/quantiles.
    :param precision: Number of decimals expected.
    :return: Matrix with the categories, one category per row, the start of the category in the first column and
            the end in the second category.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.quantiles_cut_statistics(ctypes.pointer(tss.arr_reference),
                                                        ctypes.pointer(ctypes.c_float(quantiles)),
                                                        ctypes.pointer(ctypes.c_float(precision)),
                                                        ctypes.pointer(b))
    return array(array_reference=b)


def sample_stdev(tss):
    """ Estimates standard deviation based on a sample. The standard deviation is calculated using the "n-1" method.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series.
    :return: The sample standard deviation.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.sample_stdev_statistics(ctypes.pointer(tss.arr_reference),
                                                       ctypes.pointer(b))
    return array(array_reference=b)


def skewness(tss):
    """ Calculates the sample skewness of tss (calculated with the adjusted Fisher-Pearson standardized moment
    coefficient G1).

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series. NOTE: the time series should be sorted.
    :return: Array containing the skewness of each time series in tss.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.skewness_statistics(ctypes.pointer(tss.arr_reference),
                                                   ctypes.pointer(b))
    return array(array_reference=b)