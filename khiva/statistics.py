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


def covariance(tss, unbiased=False):
    """ Returns the covariance matrix of the time series contained in tss.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series.
    :param unbiased: Determines whether it divides by n - 1 (if false) or n (if true).
    :return: The covariance matrix of the time series.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.covariance_statistics(ctypes.pointer(tss.arr_reference),
                                                         ctypes.pointer(ctypes.c_bool(unbiased)),
                                                         ctypes.pointer(b))
    return Array(array_reference=b)


def kurtosis(tss):
    """ Returns the kurtosis of tss (calculated with the adjusted Fisher-Pearson standardized moment coefficient G2).

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series.
    :return: The kurtosis of tss.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.kurtosis_statistics(ctypes.pointer(tss.arr_reference),
                                                       ctypes.pointer(b))
    return Array(array_reference=b)


def ljung_box(tss, lags):
    """ The Ljung–Box test checks that data whithin the time series are independently distributed (i.e. the correlations
    in the population from which the sample is taken are 0, so that any observed correlations in the data result from
    randomness of the sampling process). Data are no independently distributed, if they exhibit serial correlation.
    The test statistic is:

    .. math::
        Q = n\\left(n+2\\right)\sum_{k=1}^h\\frac{\hat{\\rho}^2_k}{n-k}

    where :math:`n` is the sample size, :math:`\hat{\\rho}k` is the sample autocorrelation at lag :math:`k`, and
    :math:`h` is the number of lags being tested. Under :math:`H_0` the statistic Q follows a :math:`\\chi^2{(h)}`.
    For significance level :math:`\\alpha`, the :math:`critical region` for rejection of the hypothesis of randomness
    is:

    .. math::
        Q > \\chi_{1-\\alpha,h}^2

    where :math:`\\chi_{1-\\alpha,h}^2` is the :math:`\\alpha`-quantile of the chi-squared distribution with :math:`h`
    degrees of freedom.

    [1] G. M. Ljung G. E. P. Box (1978). On a measure of lack of fit in time series models.
    Biometrika, Volume 65, Issue 2, 1 August 1978, Pages 297–303.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and
                dimension one indicates the number of time series.
    :param lags: Number of lags being tested.
    :return: Array containing the Ljung-Box statistic test.
    """
    ljung_box_out = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.ljung_box(ctypes.pointer(tss.arr_reference), ctypes.pointer(ctypes.c_long(lags)),
                                             ctypes.pointer(ljung_box_out))
    return Array(array_reference=ljung_box_out)


def moment(tss, k):
    """ Returns the kth moment of the given time series.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series.
    :param k: The specific moment to be calculated.
    :return: The kth moment of the given time series.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.moment_statistics(ctypes.pointer(tss.arr_reference),
                                                     ctypes.pointer(ctypes.c_int(k)),
                                                     ctypes.pointer(b))
    return Array(array_reference=b)


def quantile(tss, q, precision=1e8):
    """  Returns values at the given quantile.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series. NOTE: the time series should be sorted.
    :param q: Percentile(s) at which to extract score(s). One or many.
    :param precision: Number of decimals expected.
    :return: Values at the given quantile.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.quantile_statistics(ctypes.pointer(tss.arr_reference),
                                                       ctypes.pointer(q.arr_reference),
                                                       ctypes.pointer(ctypes.c_float(precision)),
                                                       ctypes.pointer(b))
    return Array(array_reference=b)


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
    KhivaLibrary().c_khiva_library.quantiles_cut_statistics(ctypes.pointer(tss.arr_reference),
                                                            ctypes.pointer(ctypes.c_float(quantiles)),
                                                            ctypes.pointer(ctypes.c_float(precision)),
                                                            ctypes.pointer(b))
    return Array(array_reference=b)


def sample_stdev(tss):
    """ Estimates standard deviation based on a sample. The standard deviation is calculated using the "n-1" method.

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series.
    :return: The sample standard deviation.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.sample_stdev_statistics(ctypes.pointer(tss.arr_reference),
                                                           ctypes.pointer(b))
    return Array(array_reference=b)


def skewness(tss):
    """ Calculates the sample skewness of tss (calculated with the adjusted Fisher-Pearson standardized moment
    coefficient G1).

    :param tss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series. NOTE: the time series should be sorted.
    :return: Array containing the skewness of each time series in tss.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.skewness_statistics(ctypes.pointer(tss.arr_reference),
                                                       ctypes.pointer(b))
    return Array(array_reference=b)
