# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

########################################################################################################################
# IMPORT
########################################################################################################################
import ctypes
import numpy as np
from tsa.tsa_libraries.library import TsaLibrary

########################################################################################################################

def abs_energy(time_series):
    """ Calculates the sum over the square values of the time series

    :param time_series: Time series. It accepts a list of lists or a numpy array with one or several time series.
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
    """ Calculates the value of an aggregation function f_agg (e.g. var or mean) of the autocorrelation
    (Compare to http://en.wikipedia.org/wiki/Autocorrelation#Estimation), taken over different all possible
    lags (1 to length of x)

    :param time_series: Time series. It accepts a list of lists or a numpy array with one or several time series.
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


def aggregated_autocorrelation(tss, aggregation_function):
    """ Calculates a linear least-squares regression for values of the time series that were aggregated
    over chunks versus the sequence from 0 up to the number of chunks minus one.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param aggregation_function: Function to be used in the aggregation. It receives an integer which indicates
                                the function to be applied.
                                0 : mean,
                                1 : median
                                2 : min,
                                3 : max,
                                4 : stdev,
                                5 : var,
                                default : mean

    :return: A numpy array whose values contains the aggregated correlation for each time series.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_n = len(tss)
    tss_l = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_n)
    tss_c_length = ctypes.c_long(tss_l)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_n).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_n)(*result_initialized)
    TsaLibrary().c_tsa_library.aggregated_autocorrelation(ctypes.pointer(tss_c_joint),
                                                          ctypes.pointer(tss_c_length),
                                                          ctypes.pointer(tss_c_number_of_ts),
                                                          ctypes.pointer(ctypes.c_int(aggregation_function)),
                                                          ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def aggregated_linear_trend(tss, chunk_size, aggregation_function):
    """ Calculates a linear least-squares regression for values of the time series that were aggregated
    over chunks versus the sequence from 0 up to the number of chunks minus one.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param chunk_size: The chunk size used to aggregate the data.
    :param aggregation_function: Function to be used in the aggregation. It receives an integer which indicates the function to be applied:
                                  0 : mean,
                                  1 : median
                                  2 : min,
                                  3 : max,
                                  4 : stdev,
                                  default : mean
    :return: a tuple with:
            pvalue: The pvalues for all time series.
            rvalue: The rvalues for all time series.
            intercept: The intercept values for all time series.
            slope: The slope for all time series.
            stdrr: The stderr values for all time series.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_n = len(tss)
    tss_l = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_n)
    tss_c_length = ctypes.c_long(tss_l)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)

    slope_initialized = np.zeros(tss_n).astype(np.double)
    slope_c_initialized = (ctypes.c_double * tss_n)(*slope_initialized)
    intercept_initialized = np.zeros(tss_n).astype(np.double)
    intercept_c_initialized = (ctypes.c_double * tss_n)(*intercept_initialized)
    rvalue_initialized = np.zeros(tss_n).astype(np.double)
    rvalue_c_initialized = (ctypes.c_double * tss_n)(*rvalue_initialized)
    pvalue_initialized = np.zeros(tss_n).astype(np.double)
    pvalue_c_initialized = (ctypes.c_double * tss_n)(*pvalue_initialized)
    stderrest_initialized = np.zeros(tss_n).astype(np.double)
    stderrest_c_initialized = (ctypes.c_double * tss_n)(*stderrest_initialized)
    TsaLibrary().c_tsa_library.aggregated_linear_trend(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                       ctypes.pointer(tss_c_number_of_ts),
                                                       ctypes.pointer(ctypes.c_long(chunk_size)),
                                                       ctypes.pointer(ctypes.c_int(aggregation_function)),
                                                       ctypes.pointer(slope_c_initialized),
                                                       ctypes.pointer(intercept_c_initialized),
                                                       ctypes.pointer(rvalue_c_initialized),
                                                       ctypes.pointer(pvalue_c_initialized),
                                                       ctypes.pointer(stderrest_c_initialized))

    return np.array(slope_c_initialized), np.array(intercept_c_initialized), np.array(rvalue_c_initialized), np.array(
        pvalue_c_initialized), np.array(stderrest_c_initialized)


def approximate_entropy(tss, m, r):
    """ Calculates a vectorized Approximate entropy algorithm.
    https://en.wikipedia.org/wiki/Approximate_entropy
    For short time-series this method is highly dependent on the parameters, but should be stable for N > 2000,
    see: Yentes et al. (2012) - The Appropriate Use of Approximate Entropy and Sample Entropy with Short Data Sets
    Other shortcomings and alternatives discussed in:
    Richman & Moorman (2000) - Physiological time-series analysis using approximate entropy and sample entropy


    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
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


def cross_covariance(xss, yss, unbiased):
    """ Calculates the cross-covariance of the given time series.

    :param xss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param yss: Time series. It accepts a list of lists or a numpy array with one or several time series.
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
    """ Calculates the auto-covariance the given time series.

    :param xss: Time series. It accepts a list of lists or a numpy array with one or several time series.
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


def cross_correlation(xss, yss, unbiased):
    """ Calculates the cross-correlation of the given time series.

    :param xss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param yss: Time series. It accepts a list of lists or a numpy array with one or several time series.
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


def auto_correlation(tss, max_lag, unbiased):
    """ Calculates the autocorrelation of the specified lag for the given time series.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param max_lag: The maximum lag to compute.
    :param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :return: The autocorrelation value for the given time series.
    """
    if isinstance(tss, list):
        tss = np.array(tss)

    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts * tss_length).astype(np.double)
    result_c_initialized = (ctypes.c_double * (tss_number_of_ts * tss_length))(*result_initialized)
    max_lag_c = ctypes.c_long(max_lag)
    unbiased_c = ctypes.c_bool(unbiased)
    TsaLibrary().c_tsa_library.auto_correlation(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                ctypes.pointer(tss_c_number_of_ts), ctypes.pointer(max_lag_c),
                                                ctypes.pointer(unbiased_c),
                                                ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def binned_entropy(tss, max_bins):
    """ Calculates the binned entropy for the given time series and number of bins.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param max_bins: The number of bins.
    :return: The binned entropy value for the given time series.
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
    max_bins_c = ctypes.c_int(max_bins)
    TsaLibrary().c_tsa_library.binned_entropy(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                              ctypes.pointer(tss_c_number_of_ts), ctypes.pointer(max_bins_c),
                                              ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def c3(tss, lag):
    """ Calculates the Schreiber, T. and Schmitz, A. (1997) measure of non-linearity
    for the given time series

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
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
    """ Calculates an estimate for the time series complexity defined by
    Batista, Gustavo EAPA, et al (2014). (A more complex time series has more peaks,
    valleys, etc.)

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
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


def count_above_mean(tss):
    """ Calculates the number of values in the time series that are higher than
    the mean.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The number of values in the time series that are higher than the mean.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts).astype(np.uint32)
    result_c_initialized = (ctypes.c_uint32 * tss_number_of_ts)(*result_initialized)
    TsaLibrary().c_tsa_library.count_above_mean(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                ctypes.pointer(tss_c_number_of_ts),
                                                ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def count_below_mean(tss):
    """ Calculates the number of values in the time series that are lower than
    the mean.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The number of values in the time series that are lower than the mean.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts).astype(np.uint32)
    result_c_initialized = (ctypes.c_uint32 * tss_number_of_ts)(*result_initialized)
    TsaLibrary().c_tsa_library.count_below_mean(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                ctypes.pointer(tss_c_number_of_ts),
                                                ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def cwt_coefficients(tss, widths, coeff, w):
    """ Calculates a Continuous wavelet transform for the Ricker wavelet, also known as
    the "Mexican hat wavelet".

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param widths: Widths. It accepts a list of lists or a numpy array with one or several widths.
    :param coeff: Coefficient of interest.
    :param w: Width of interest.
    :return: Result of calculated coefficients.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_n = len(tss)
    tss_l = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_n)
    tss_c_length = ctypes.c_long(tss_l)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    if isinstance(widths, list):
        widths = np.array(widths)
    widths_n = len(widths)
    widths_l = len(widths[0])
    widths_c_number_of_ts = ctypes.c_long(widths_n)
    widths_c_length = ctypes.c_long(widths_l)
    widths_joint = np.concatenate(widths, axis=0)
    widths_c_joint = (ctypes.c_int * len(widths_joint))(*widths_joint)

    result_initialized = np.zeros(tss_n).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_n)(*result_initialized)
    TsaLibrary().c_tsa_library.cwt_coefficients(ctypes.pointer(tss_c_joint),
                                                ctypes.pointer(tss_c_length),
                                                ctypes.pointer(tss_c_number_of_ts),
                                                ctypes.pointer(widths_c_joint),
                                                ctypes.pointer(widths_c_length),
                                                ctypes.pointer(widths_c_number_of_ts),
                                                ctypes.pointer(ctypes.c_int(coeff)),
                                                ctypes.pointer(ctypes.c_int(w)),
                                                ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def energy_ratio_by_chunks(tss, num_segments, segment_focus):
    """ Calculates the sum of squares of chunk i out of N chunks expressed as a ratio
    with the sum of squares over the whole series. segmentFocus should be lower
    than the number of segments.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param num_segments: The number of segments to divide the series into.
    :param segment_focus: The segment number (starting at zero) to return a feature on.
    :return: The energy ratio by chunk of the time series.
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
    num_segments_c = ctypes.c_long(num_segments)
    segment_focus_c = ctypes.c_long(segment_focus)
    TsaLibrary().c_tsa_library.energy_ratio_by_chunks(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                      ctypes.pointer(tss_c_number_of_ts),
                                                      ctypes.pointer(num_segments_c),

                                                      ctypes.pointer(segment_focus_c),
                                                      ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def fftCoefficient(tss, coefficient):
    """ Calculates the fourier coefficients of the one-dimensional discrete
    Fourier Transform for real input by fast fourier transformation algorithm.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param coefficient: The coefficient to extract from the FFT.
    :return: Tuple with:
        real: The real part of the coefficient.
        imag: The imaginary part of the coefficient.
        abs: The absolute value of the coefficient.
        angle: The angle of the coefficient.
    """
    if isinstance(tss, list):
        tss = np.array(tss)

    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)

    coefficient_c = ctypes.c_long(coefficient)

    real_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    real_c_initialized = (ctypes.c_double * tss_number_of_ts)(*real_initialized)

    imag_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    imag_c_initialized = (ctypes.c_double * tss_number_of_ts)(*imag_initialized)

    absolute_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    absolute_c_initialized = (ctypes.c_double * tss_number_of_ts)(*absolute_initialized)

    angle_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    angle_c_initialized = (ctypes.c_double * tss_number_of_ts)(*angle_initialized)

    TsaLibrary().c_tsa_library.fftCoefficient(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                              ctypes.pointer(tss_c_number_of_ts),
                                              ctypes.pointer(coefficient_c),
                                              ctypes.pointer(real_c_initialized),
                                              ctypes.pointer(imag_c_initialized),
                                              ctypes.pointer(absolute_c_initialized),
                                              ctypes.pointer(angle_c_initialized)
                                              )

    return (np.array(real_c_initialized), np.array(imag_c_initialized),
            np.array(absolute_c_initialized), np.array(angle_c_initialized))


def first_location_of_maximum(tss):
    """ Calculates the first relative location of the maximal value for each time series.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The first relative location of the maximum value to the length of the time series, for each time series.
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
    TsaLibrary().c_tsa_library.first_location_of_maximum(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                         ctypes.pointer(tss_c_number_of_ts),
                                                         ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def first_location_of_minimum(tss):
    """ Calculates the first location of the minimal value of each time series. The position is calculated relatively
    to the length of the series.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The first relative location of the minimal value of each series.
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
    TsaLibrary().c_tsa_library.first_location_of_minimum(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                         ctypes.pointer(tss_c_number_of_ts),
                                                         ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def has_duplicates(tss):
    """ Calculates if the input time series contain duplicated elements.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: Array containing True if the time series contains duplicated elements
     and false otherwise.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts).astype(np.bool)
    result_c_initialized = (ctypes.c_bool * tss_number_of_ts)(*result_initialized)
    TsaLibrary().c_tsa_library.has_duplicates(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                              ctypes.pointer(tss_c_number_of_ts), ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def has_duplicate_max(tss):
    """ Calculates if the maximum within input time series is duplicated.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: Array containing True if the maximum value of the time series is duplicated and false otherwise.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts).astype(np.bool)
    result_c_initialized = (ctypes.c_bool * tss_number_of_ts)(*result_initialized)
    TsaLibrary().c_tsa_library.has_duplicate_max(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                 ctypes.pointer(tss_c_number_of_ts),
                                                 ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def has_duplicate_min(tss):
    """ Calculates if the minimum of the input time series is duplicated.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: Array containing True if the minimum of the time series is duplicated and False otherwise.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)

    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts).astype(np.bool)
    result_c_initialized = (ctypes.c_bool * tss_number_of_ts)(*result_initialized)
    TsaLibrary().c_tsa_library.has_duplicate_min(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                 ctypes.pointer(tss_c_number_of_ts),
                                                 ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def index_max_quantile(tss, q):
    """ Calculates the index of the max quantile.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param q: The quantile.
    :return: The index of the max quantile q.
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
    q_c = ctypes.c_double(q)
    TsaLibrary().c_tsa_library.index_max_quantile(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                  ctypes.pointer(tss_c_number_of_ts), ctypes.pointer(q_c),
                                                  ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def kurtosis(tss):
    """ Returns the kurtosis of tss (calculated with the adjusted Fisher-Pearson
    standardized moment coefficient G2).

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The kurtosis of each tss.
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
    TsaLibrary().c_tsa_library.kurtosis(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                        ctypes.pointer(tss_c_number_of_ts),
                                        ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def large_standard_deviation(tss, r):
    """ Checks if the time series within tss have a large standard deviation.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param r: The threshold.
    :return: Array containing True for those time series in tss that have a large standard deviation.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts).astype(np.bool)
    result_c_initialized = (ctypes.c_bool * tss_number_of_ts)(*result_initialized)
    r_c = ctypes.c_double(r)
    TsaLibrary().c_tsa_library.large_standard_deviation(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                        ctypes.pointer(tss_c_number_of_ts), ctypes.pointer(r_c),
                                                        ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def last_location_of_maximum(tss):
    """ Calculates the last location of the maximum value of each time series. The position
    is calculated relatively to the length of the series.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The last relative location of the maximum value of each series.
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
    TsaLibrary().c_tsa_library.last_location_of_maximum(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                        ctypes.pointer(tss_c_number_of_ts),
                                                        ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def last_location_of_minimum(tss):
    """ Calculates the last location of the minimum value of each time series. The position
    is calculated relatively to the length of the series.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The last relative location of the minimum value of each series.
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
    TsaLibrary().c_tsa_library.last_location_of_minimum(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                        ctypes.pointer(tss_c_number_of_ts),
                                                        ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def length(tss):
    """ Returns the length of the input time series.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The length of tss.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)
    result_initialized = np.zeros(tss_number_of_ts).astype(np.int)
    result_c_initialized = (ctypes.c_int * tss_number_of_ts)(*result_initialized)
    TsaLibrary().c_tsa_library.length(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                      ctypes.pointer(tss_c_number_of_ts),
                                      ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def linear_trend(tss):
    """ Calculate a linear least-squares regression for the values of the time series versus the sequence from 0 to
    length of the time series minus one.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return  a tuple with:
            pvalue: The pvalues for all time series.
            rvalue: The rvalues for all time series.
            intercept: The intercept values for all time series.
            slope: The slope for all time series.
            stdrr: The stderr values for all time series.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_number_of_ts = len(tss)
    tss_length = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_number_of_ts)
    tss_c_length = ctypes.c_long(tss_length)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)

    pvalue_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    pvalue_c_initialized = (ctypes.c_double * tss_number_of_ts)(*pvalue_initialized)

    rvalue_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    rvalue_c_initialized = (ctypes.c_double * tss_number_of_ts)(*rvalue_initialized)

    intercept_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    intercept_c_initialized = (ctypes.c_double * tss_number_of_ts)(*intercept_initialized)

    slope_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    slope_c_initialized = (ctypes.c_double * tss_number_of_ts)(*slope_initialized)

    stdrr_initialized = np.zeros(tss_number_of_ts).astype(np.double)
    stdrr_c_initialized = (ctypes.c_double * tss_number_of_ts)(*stdrr_initialized)

    TsaLibrary().c_tsa_library.linear_trend(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                            ctypes.pointer(tss_c_number_of_ts),
                                            ctypes.pointer(pvalue_c_initialized),
                                            ctypes.pointer(rvalue_c_initialized),
                                            ctypes.pointer(intercept_c_initialized),
                                            ctypes.pointer(slope_c_initialized),
                                            ctypes.pointer(stdrr_c_initialized)
                                            )

    return (np.array(pvalue_c_initialized), np.array(rvalue_c_initialized),
            np.array(intercept_c_initialized), np.array(slope_c_initialized),
            np.array(stdrr_c_initialized))


def longest_strike_above_mean(tss):
    """ Calculates the length of the longest consecutive subsequence in tss that is bigger than the mean of tss.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The length of the longest consecutive subsequence in the input time series that is bigger than the mean.
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
    TsaLibrary().c_tsa_library.longest_strike_above_mean(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                         ctypes.pointer(tss_c_number_of_ts),
                                                         ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def longest_strike_below_mean(tss):
    """ Calculates the length of the longest consecutive subsequence in tss that is below the mean of tss.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The length of the longest consecutive subsequence in the input time series that is below the mean.
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
    TsaLibrary().c_tsa_library.longest_strike_below_mean(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                         ctypes.pointer(tss_c_number_of_ts),
                                                         ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def max_langevin_fixed_point(tss, m, r):
    """ Largest fixed point of dynamics  :math:`argmax_x {h(x)=0}` estimated from polynomial :math:`h(x)`,
    which has been fitted to the deterministic dynamics of Langevin model

    .. math::
        \dot(x)(t) = h(x(t)) + R \mathcal(N)(0,1)

    as described by

        Friedrich et al. (2000): Physics Letters A 271, p. 217-222
        *Extracting model equations from experimental data*

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param m: Order of polynom to fit for estimating fixed points of dynamics.
    :param r: Number of quantiles to use for averaging.
    :return: Largest fixed point of deterministic dynamics.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_n = len(tss)
    tss_l = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_n)
    tss_c_length = ctypes.c_long(tss_l)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)

    result_initialized = np.zeros(tss_n).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_n)(*result_initialized)
    TsaLibrary().c_tsa_library.max_langevin_fixed_point(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                        ctypes.pointer(tss_c_number_of_ts),
                                                        ctypes.pointer(ctypes.c_int(m)),
                                                        ctypes.pointer(ctypes.c_double(r)),
                                                        ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def maximum(tss):
    """ Calculates the maximum value for each time series within tss.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The maximum value of each time series within tss.
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
    TsaLibrary().c_tsa_library.maximum(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                       ctypes.pointer(tss_c_number_of_ts),
                                       ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def mean(tss):
    """ Calculates the mean value for each time series within tss.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The mean value of each time series within tss.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_n = len(tss)
    tss_l = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_n)
    tss_c_length = ctypes.c_long(tss_l)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)

    result_initialized = np.zeros(tss_n).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_n)(*result_initialized)
    TsaLibrary().c_tsa_library.mean(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                    ctypes.pointer(tss_c_number_of_ts), ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def mean_absolute_change(tss):
    """ Calculates the mean over the absolute differences between subsequent time series values in tss.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The mean over the absolute differences between subsequent time series values.
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
    TsaLibrary().c_tsa_library.mean_absolute_change(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                                    ctypes.pointer(tss_c_number_of_ts),
                                                    ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def mean_change(tss):
    """ Calculates the mean over the differences between subsequent time series values in tss.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The mean over the differences between subsequent time series values.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_n = len(tss)
    tss_l = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_n)
    tss_c_length = ctypes.c_long(tss_l)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)

    result_initialized = np.zeros(tss_n).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_n)(*result_initialized)
    TsaLibrary().c_tsa_library.mean_change(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                           ctypes.pointer(tss_c_number_of_ts), ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def mean_second_derivative_central(tss):
    """ Calculates mean value of a central approximation of the second derivative for each time series in tss.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The mean value of a central approximation of the second derivative for each time series.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_n = len(tss)
    tss_l = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_n)
    tss_c_length = ctypes.c_long(tss_l)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)

    result_initialized = np.zeros(tss_n).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_n)(*result_initialized)
    TsaLibrary().c_tsa_library.mean_second_derivative_central(ctypes.pointer(tss_c_joint),
                                                              ctypes.pointer(tss_c_length),
                                                              ctypes.pointer(tss_c_number_of_ts),
                                                              ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def median(tss):
    """ Calculates the median value for each time series within tss.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The median value of each time series within tss.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_n = len(tss)
    tss_l = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_n)
    tss_c_length = ctypes.c_long(tss_l)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)

    result_initialized = np.zeros(tss_n).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_n)(*result_initialized)
    TsaLibrary().c_tsa_library.median(ctypes.pointer(tss_c_joint), ctypes.pointer(tss_c_length),
                                      ctypes.pointer(tss_c_number_of_ts), ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def minimum(tss):
    """ Calculates the minimum value for each time series within tss.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :return: The minimum value of each time series within tss.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_n = len(tss)
    tss_l = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_n)
    tss_c_length = ctypes.c_long(tss_l)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)

    result_initialized = np.zeros(tss_n).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_n)(*result_initialized)
    TsaLibrary().c_tsa_library.minimum(ctypes.pointer(tss_c_joint),

                                       ctypes.pointer(tss_c_length), ctypes.pointer(tss_c_number_of_ts),
                                       ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)


def number_crossing_m(tss, m):
    """ Calculates the number of m-crossings. A m-crossing is defined as two sequential values where the first
    value is lower than m and the next is greater, or viceversa. If you set m to zero, you will get the number of
    zero crossings.

    :param tss: Time series. It accepts a list of lists or a numpy array with one or several time series.
    :param m: The m value.
    :return: The number of m-crossings of each time series within tss.
    """
    if isinstance(tss, list):
        tss = np.array(tss)
    tss_n = len(tss)
    tss_l = len(tss[0])
    tss_c_number_of_ts = ctypes.c_long(tss_n)
    tss_c_length = ctypes.c_long(tss_l)
    tss_joint = np.concatenate(tss, axis=0)
    tss_c_joint = (ctypes.c_double * len(tss_joint))(*tss_joint)

    result_initialized = np.zeros(tss_n).astype(np.double)
    result_c_initialized = (ctypes.c_double * tss_n)(*result_initialized)
    TsaLibrary().c_tsa_library.number_crossing_m(ctypes.pointer(tss_c_joint),
                                                 ctypes.pointer(tss_c_length), ctypes.pointer(tss_c_number_of_ts),
                                                 ctypes.pointer(ctypes.c_int(m)),
                                                 ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)
