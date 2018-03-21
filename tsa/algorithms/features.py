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

def abs_energy(time_series):
    """
    Calculates the sum over the square values of the timeseries

    :param time_series: Time series.
    :return: Numpy array with the absEnergy.
    """
    if isinstance(time_series, list):
        time_series = np.array(time_series)

    n = len(time_series)
    time_series_length = len(time_series[0])
    c_number_of_time_series = ctypes.c_long(n)
    c_time_series_length = ctypes.c_long(time_series_length)
    initialized_result_array = np.zeros(n).astype(np.double)
    c_result_array = (ctypes.c_double * n)(*initialized_result_array)
    time_series_joint = np.concatenate(time_series, axis=0)
    c_time_series_joint = (ctypes.c_double * len(time_series_joint))(*time_series_joint)

    TsaLibrary().c_tsa_library.abs_energy(ctypes.pointer(c_time_series_joint),
                                          ctypes.pointer(c_time_series_length),
                                          ctypes.pointer(c_number_of_time_series),
                                          ctypes.pointer(c_result_array))

    np_result = np.array(c_result_array)

    return np_result


def absolute_sum_of_changes(time_series):
    """
    Calculates the value of an aggregation function f_agg (e.g. var or mean) of the autocorrelation
    (Compare to http://en.wikipedia.org/wiki/Autocorrelation#Estimation), taken over different all possible
    lags (1 to length of x)

    :param time_series: Time series.
    :return: Numpy array with the absolute sum of changes.
    """
    if isinstance(time_series, list):
        time_series = np.array(time_series)

    n = len(time_series)
    time_series_length = len(time_series[0])
    c_number_of_time_series = ctypes.c_long(n)
    c_time_series_length = ctypes.c_long(time_series_length)
    initialized_result_array = np.zeros(n).astype(np.double)
    c_result_array = (ctypes.c_double * n)(*initialized_result_array)
    time_series_joint = np.concatenate(time_series, axis=0)
    c_time_series_joint = (ctypes.c_double * len(time_series_joint))(*time_series_joint)

    TsaLibrary().c_tsa_library.absolute_sum_of_changes(ctypes.pointer(c_time_series_joint),
                                                       ctypes.pointer(c_time_series_length),
                                                       ctypes.pointer(c_number_of_time_series),
                                                       ctypes.pointer(c_result_array))

    np_result = np.array(c_result_array)

    return np_result


def c3(tss, lag):
    """
    Calculates the Schreiber, T. and Schmitz, A. (1997) measure of non-linearity
    for the given time series

    :param tss: Time series.
    :param lag: The lag.
    :return: Numpy array with non-linearity value for the given time series.
    """
    if isinstance(tss, list):
        tss = np.array(tss)

    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_number_of_ts)(*result_initialized)
    lag_c = ctypes.c_long(lag)

    TsaLibrary().c_tsa_library.c3(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                  ctypes.pointer(tss_c_number_of_ts),
                                  ctypes.pointer(lag_c), ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def cid_ce(tss, z_normalize):
    """
    Calculates an estimate for the time series complexity defined by
    Batista, Gustavo EAPA, et al (2014). (A more complex time series has more peaks,
    valleys, etc.)

    :param tss: Time series.
    :param z_normalize: Controls wheter the time series should be z-normalized or not.
    :return: Numpy array with the complexity value for the given time series.
    """
    if isinstance(tss, list):
        tss = np.array(tss)

    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_number_of_ts)(*result_initialized)
    z_normalize_c = ctypes.c_bool(z_normalize)

    TsaLibrary().c_tsa_library.cidCe(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                     ctypes.pointer(tss_c_number_of_ts),
                                     ctypes.pointer(z_normalize_c), ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def cross_correlation(xss, yss, unbiased):
    """
    Calculates the cross-correlation of the given time series.


    :param xss: Time series.
    :param yss: Time series.
    :param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :return: Numpy array with cross-correlation value for the given time series.
    """
    if isinstance(xss, list):
        xss = np.array(xss)

    xss_number_of_ts = len(xss)
    xss_length = len(xss[0])
    xss_c_number_of_ts = ctypes.c_long(xss_number_of_ts)
    xss_c_length = ctypes.c_long(xss_length)
    xss_joint = np.concatenate(xss, axis=0)
    xss_c_joint = (ctypes.c_double * len(xss_joint))(*xss_joint)

    if isinstance(yss, list):
        yss = np.array(yss)

    yss_number_of_ts = len(yss)
    yss_length = len(yss[0])
    yss_c_number_of_ts = ctypes.c_long(yss_number_of_ts)
    yss_c_length = ctypes.c_long(yss_length)
    yss_joint = np.concatenate(yss, axis=0)
    yss_c_joint = (ctypes.c_double * len(yss_joint))(*yss_joint)
    result_initialized = np.zeros(max(xss_length, yss_length)).astype(np.double)
    result_c_initialized = (ctypes.c_double * max(xss_length, yss_length))(*result_initialized)
    unbiased_c = ctypes.c_bool(unbiased)

    TsaLibrary().c_tsa_library.cross_correlation(ctypes.pointer(xss_c_joint), ctypes.pointer(xss_c_length),
                                                 ctypes.pointer(xss_c_number_of_ts), ctypes.pointer(yss_c_joint),
                                                 ctypes.pointer(yss_c_length), ctypes.pointer(yss_c_number_of_ts),
                                                 ctypes.pointer(unbiased_c), ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def cross_covariance(xss, yss, unbiased):
    """
    Calculates the cross-covariance of the given time series.

    :param xss: Time series.
    :param yss: Time series.
    :param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :return: Numpy array with the cross-covariance value for the given time series.
    """
    if isinstance(xss, list):
        xss = np.array(xss)

    xss_number_of_ts = len(xss)
    xss_length = len(xss[0])
    xss_c_number_of_ts = ctypes.c_long(xss_number_of_ts)
    xss_c_length = ctypes.c_long(xss_length)
    xss_joint = np.concatenate(xss, axis=0)
    xss_c_joint = (ctypes.c_double * len(xss_joint))(*xss_joint)

    if isinstance(yss, list):
        yss = np.array(yss)

    yss_number_of_ts = len(yss)
    yss_length = len(yss[0])
    yss_c_number_of_ts = ctypes.c_long(yss_number_of_ts)
    yss_c_length = ctypes.c_long(yss_length)
    yss_joint = np.concatenate(yss, axis=0)
    yss_c_joint = (ctypes.c_double * len(yss_joint))(*yss_joint)
    result_initialized = np.zeros(xss_length * yss_length).astype(np.double)
    result_c_initialized = (ctypes.c_double * (xss_length * yss_length))(*result_initialized)
    unbiased_c = ctypes.c_bool(unbiased)

    TsaLibrary().c_tsa_library.cross_covariance(ctypes.pointer(xss_c_joint), ctypes.pointer(xss_c_length),
                                                ctypes.pointer(xss_c_number_of_ts), ctypes.pointer(yss_c_joint),
                                                ctypes.pointer(yss_c_length), ctypes.pointer(yss_c_number_of_ts),
                                                ctypes.pointer(unbiased_c), ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def auto_covariance(xss, unbiased):
    """
    Calculates the auto-covariance the given time series.

    :param xss: Time series.
    :param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :return: Numpy array with the auto-covariance value for the given time series.
    """
    if isinstance(xss, list):
        xss = np.array(xss)

    xss_number_of_ts = len(xss)
    xss_length = len(xss[0])
    xss_c_number_of_ts = ctypes.c_long(xss_number_of_ts)
    xss_c_length = ctypes.c_long(xss_length)
    xss_joint = np.concatenate(xss, axis=0)
    xss_c_joint = (ctypes.c_double * len(xss_joint))(*xss_joint)
    result_initialized = np.zeros(xss_number_of_ts * xss_length).astype(np.double)
    result_c_initialized = (ctypes.c_double * (xss_number_of_ts * xss_length))(*result_initialized)
    unbiased_c = ctypes.c_bool(unbiased)

    TsaLibrary().c_tsa_library.auto_covariance(ctypes.pointer(xss_c_joint), ctypes.pointer(xss_c_length),
                                               ctypes.pointer(xss_c_number_of_ts), ctypes.pointer(unbiased_c),
                                               ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def approximate_entropy(tss, m, r):
    """
    Calculates a vectorized Approximate entropy algorithm.
    https://en.wikipedia.org/wiki/Approximate_entropy
    For short time-series this method is highly dependent on the parameters, but should be stable for N > 2000,
    see: Yentes et al. (2012) - The Appropriate Use of Approximate Entropy and Sample Entropy with Short Data Sets
    Other shortcomings and alternatives discussed in:
    Richman & Moorman (2000) - Physiological time-series analysis using approximate entropy and sample entropy


    :param tss: Time series.
    :param m: Length of compared run of data.
    :param r: Filtering level, must be positive.
    :return: Numpy array with the vectorized approximate entropy for all the input time series in tss.
    """

    if isinstance(tss, list):
        tss = np.array(tss)

    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_number_of_ts)(*result_initialized)
    m_c = ctypes.c_int(m)
    r_c = ctypes.c_double(r)

    TsaLibrary().c_tsa_library.approximate_entropy(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                   ctypes.pointer(tss_c_number_of_ts), ctypes.pointer(m_c),
                                                   ctypes.pointer(r_c),
                                                   ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)
