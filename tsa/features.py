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
from tsa.array import array, dtype


########################################################################################################################


def abs_energy(arr):
    """ Calculates the sum over the square values of the time series.

    :param arr: TSA array with the time series.
    :type arr: tsa.array
    :return: TSA array with the absEnergy.
    :rtype: tsa.array
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.abs_energy(ctypes.pointer(arr.arr_reference),
                                          ctypes.pointer(b))
    return array(array_reference=b, tsa_type=arr.tsa_type)


def absolute_sum_of_changes(arr):
    """ Calculates the value of an aggregation function f_agg (e.g. var or mean) of the autocorrelation
    (Compare to http://en.wikipedia.org/wiki/Autocorrelation#Estimation), taken over different all possible
    lags (1 to length of x)

    :param arr: TSA array with the time series.
    :type arr: tsa.array
    :return: TSA array with the absolute sum of changes.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.absolute_sum_of_changes(ctypes.pointer(arr.arr_reference),
                                                       ctypes.pointer(b))
    return array(array_reference=b, tsa_type=arr.tsa_type)


def aggregated_autocorrelation(arr, aggregation_function):
    """ Calculates a linear least-squares regression for values of the time series that were aggregated
    over chunks versus the sequence from 0 up to the number of chunks minus one.

    :param arr: A TSA array with the time series.
    :param aggregation_function: Function to be used in the aggregation. It receives an integer which indicates
                                the function to be applied.
                                0 : mean,
                                1 : median
                                2 : min,
                                3 : max,
                                4 : stdev,
                                5 : var,
                                default : mean

    :return: TSA array that contains the aggregated correlation for each time series.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.aggregated_autocorrelation(ctypes.pointer(arr.arr_reference),
                                                          ctypes.c_int(aggregation_function),
                                                          ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def aggregated_linear_trend(arr, chunk_size, aggregation_function):
    """ Calculates a linear least-squares regression for values of the time series that were aggregated
    over chunks versus the sequence from 0 up to the number of chunks minus one.

    :param arr: A TSA array with the time series.
    :param chunk_size: The chunk size used to aggregate the data.
    :param aggregation_function: Function to be used in the aggregation. It receives an integer which indicates the function to be applied:
                                  0 : mean,
                                  1 : median
                                  2 : min,
                                  3 : max,
                                  4 : stdev,
                                  default : mean
    :return: ( pvalue: TSA array with the pvalues for all time series.
            rvalue: TSA array with the rvalues for all time series.
            intercept: TSA array with the intercept values for all time series.
            slope: TSA array with the slope for all time series.
            stdrr: TSA array with the stderr values for all time series. )
    :rtype: (tsa.array, tsa.array, tsa.array, tsa.array, tsa.array)
    """
    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)
    d = ctypes.c_void_p(0)
    e = ctypes.c_void_p(0)
    f = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.aggregated_linear_trend(ctypes.pointer(arr.arr_reference),
                                                       ctypes.c_long(chunk_size),
                                                       ctypes.c_int(aggregation_function),
                                                       ctypes.pointer(b),
                                                       ctypes.pointer(c),
                                                       ctypes.pointer(d),
                                                       ctypes.pointer(e),
                                                       ctypes.pointer(f))

    return array(array_reference=b, tsa_type=arr.tsa_type), array(array_reference=c,
                                                                  tsa_type=arr.tsa_type), array(
        array_reference=d, tsa_type=arr.tsa_type), array(array_reference=e, tsa_type=arr.tsa_type), array(
        array_reference=f, tsa_type=arr.tsa_type)


def approximate_entropy(arr, m, r):
    """ Calculates a vectorized Approximate entropy algorithm.
    https://en.wikipedia.org/wiki/Approximate_entropy
    For short time-series this method is highly dependent on the parameters, but should be stable for N > 2000,
    see: Yentes et al. (2012) - The Appropriate Use of Approximate Entropy and Sample Entropy with Short Data Sets
    Other shortcomings and alternatives discussed in:
    Richman & Moorman (2000) - Physiological time-series analysis using approximate entropy and sample entropy


    :param arr: A TSA array with the time series.
    :param m: Length of compared run of data.
    :param r: Filtering level, must be positive.
    :return: TSA array with the vectorized approximate entropy for all the input time series in tss.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.approximate_entropy(ctypes.pointer(arr.arr_reference), ctypes.c_int(m),
                                                   ctypes.c_float(r),
                                                   ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def cross_covariance(xss, yss, unbiased):
    """ Calculates the cross-covariance of the given time series.

    :param xss: A TSA array with time series.
    :param yss: A TSA Array with time series.
    :param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :return: TSA array with the cross-covariance value for the given time series.
    """

    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.cross_covariance(ctypes.pointer(xss.arr_reference), ctypes.pointer(yss.arr_reference),
                                                ctypes.c_bool(unbiased), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=xss.tsa_type)


def auto_covariance(arr, unbiased=False):
    """ Calculates the auto-covariance the given time series.

    :param arr: TSA array with the time series.
    :param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :return: TSA array with the auto-covariance value for the given time series.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.auto_covariance(ctypes.pointer(arr.arr_reference), ctypes.c_bool(unbiased),
                                               ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def cross_correlation(xss, yss, unbiased):
    """ Calculates the cross-correlation of the given time series.

    :param xss: TSA array with the time series.
    :param yss: TSA array with the time series.
    :param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :return: TSA array with cross-correlation value for the given time series.
    """

    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.cross_correlation(ctypes.pointer(xss.arr_reference), ctypes.pointer(yss.arr_reference),
                                                 ctypes.c_bool(unbiased), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=xss.tsa_type)


def auto_correlation(arr, max_lag, unbiased):
    """ Calculates the autocorrelation of the specified lag for the given time series.

    :param arr: TSA array with the time series.
    :param max_lag: The maximum lag to compute.
    :param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :return: TSA array with the autocorrelation value for the given time series.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.auto_correlation(ctypes.pointer(arr.arr_reference),
                                                ctypes.c_long(max_lag),
                                                ctypes.c_bool(unbiased),
                                                ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def binned_entropy(arr, max_bins):
    """ Calculates the binned entropy for the given time series and number of bins.

    :param arr: TSA array with the time series.
    :param max_bins: The number of bins.
    :return: TSA array with the binned entropy value for the given time series.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.binned_entropy(ctypes.pointer(arr.arr_reference), ctypes.c_int(max_bins),
                                              ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def c3(arr, lag):
    """ Calculates the Schreiber, T. and Schmitz, A. (1997) measure of non-linearity
    for the given time series

    :param arr: TSA array with the time series.
    :param lag: The lag.
    :return: TSA array with non-linearity value for the given time series.
    """

    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.c3(ctypes.pointer(arr.arr_reference),
                                  ctypes.c_long(lag), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def cid_ce(arr, z_normalize):
    """ Calculates an estimate for the time series complexity defined by
    Batista, Gustavo EAPA, et al (2014). (A more complex time series has more peaks,
    valleys, etc.)

    :param arr: TSA array with the time series.
    :param z_normalize: Controls wheter the time series should be z-normalized or not.
    :return: TSA array with the complexity value for the given time series.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.cid_ce(ctypes.pointer(arr.arr_reference),
                                      ctypes.c_bool(z_normalize), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def count_above_mean(arr):
    """ Calculates the number of values in the time series that are higher than
    the mean.

    :param arr: TSA array with the time series.
    :return: TSA array with the number of values in the time series that are higher than the mean.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.count_above_mean(ctypes.pointer(arr.arr_reference),
                                                ctypes.pointer(b))

    return array(array_reference=b, tsa_type=dtype.u32)


def count_below_mean(arr):
    """ Calculates the number of values in the time series that are lower than
    the mean.

    :param arr: TSA array with the time series.
    :return: TSA Array with the number of values in the time series that are lower than the mean.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.count_below_mean(ctypes.pointer(arr.arr_reference),
                                                ctypes.pointer(b))

    return array(array_reference=b, tsa_type=dtype.u32)


def cwt_coefficients(tss, widths, coeff, w):
    """ Calculates a Continuous wavelet transform for the Ricker wavelet, also known as
    the "Mexican hat wavelet".

    :param tss: TSA array with the time series.
    :param widths: Widths. It accepts a list of lists or a numpy array with one or several widths.
    :param coeff: Coefficient of interest.
    :param w: Width of interest.
    :return: TSA Array with the result of calculated coefficients.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.cwt_coefficients(ctypes.pointer(tss.arr_reference),
                                                ctypes.pointer(widths.arr_reference),
                                                ctypes.c_int(coeff),
                                                ctypes.c_int(w),
                                                ctypes.pointer(b))

    return array(array_reference=b, tsa_type=tss.tsa_type)


def energy_ratio_by_chunks(arr, num_segments, segment_focus):
    """ Calculates the sum of squares of chunk i out of N chunks expressed as a ratio
    with the sum of squares over the whole series. segmentFocus should be lower
    than the number of segments.

    :param arr: TSA array with the time series.
    :param num_segments: The number of segments to divide the series into.
    :param segment_focus: The segment number (starting at zero) to return a feature on.
    :return: TSA array with the energy ratio by chunk of the time series.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.energy_ratio_by_chunks(ctypes.pointer(arr.arr_reference),
                                                      ctypes.c_long(num_segments),
                                                      ctypes.c_long(segment_focus),
                                                      ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def fft_aggregated(arr):
    """ Calculates the spectral centroid(mean), variance, skew, and kurtosis of the absolute fourier transform
    spectrum.

    :param arr: TSA array with the time series.
    :return: TSA array with the spectral centroid (mean), variance, skew, and kurtosis of the absolute fourier transform
            spectrum.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.fft_aggregated(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def fft_coefficient(arr, coefficient):
    """ Calculates the fourier coefficients of the one-dimensional discrete
    Fourier Transform for real input by fast fourier transformation algorithm.

    :param arr: TSA array with the time series.
    :param coefficient: The coefficient to extract from the FFT.
    :return: Tuple with:
        real: TSA array with the real part of the coefficient.
        imag: TSA array with the imaginary part of the coefficient.
        abs: TSA array with the absolute value of the coefficient.
        angle: TSA array with the angle of the coefficient.
    """
    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)
    d = ctypes.c_void_p(0)
    e = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.fft_coefficient(ctypes.pointer(arr.arr_reference),
                                              ctypes.c_long(coefficient),
                                              ctypes.pointer(b),
                                              ctypes.pointer(c),
                                              ctypes.pointer(d),
                                              ctypes.pointer(e)
                                              )

    return array(array_reference=b, tsa_type=arr.tsa_type), array(array_reference=c,
                                                                  tsa_type=arr.tsa_type), array(
        array_reference=d, tsa_type=arr.tsa_type), array(array_reference=e, tsa_type=arr.tsa_type)


def first_location_of_maximum(arr):
    """ Calculates the first relative location of the maximal value for each time series.

    :param arr: TSA array with the time series.
    :return: TSA array with the first relative location of the maximum value to the length of the time series, for each time series.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.first_location_of_maximum(ctypes.pointer(arr.arr_reference),
                                                         ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def first_location_of_minimum(arr):
    """ Calculates the first location of the minimal value of each time series. The position is calculated relatively
    to the length of the series.

    :param arr: TSA array with the time series.
    :return: TSA array with the first relative location of the minimal value of each series.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.first_location_of_minimum(ctypes.pointer(arr.arr_reference),
                                                         ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def has_duplicates(arr):
    """ Calculates if the input time series contain duplicated elements.

    :param arr: TSA array with the time series.
    :return: TSA array containing True if the time series contains duplicated elements
     and false otherwise.
    """

    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.has_duplicates(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=dtype.b8)


def has_duplicate_max(arr):
    """ Calculates if the maximum within input time series is duplicated.

    :param arr: TSA array with the time series.
    :return: TSA array containing True if the maximum value of the time series is duplicated and false otherwise.
    """

    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.has_duplicate_max(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=dtype.b8)


def has_duplicate_min(arr):
    """ Calculates if the minimum of the input time series is duplicated.

    :param arr: TSA array with the time series.
    :return: TSA array containing True if the minimum of the time series is duplicated and False otherwise.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.has_duplicate_min(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=dtype.b8)


def index_max_quantile(arr, q):
    """ Calculates the index of the max quantile.

    :param arr: TSA array with the time series.
    :param q: The quantile.
    :return: TSA array with the index of the max quantile q.
    """

    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.index_max_quantile(ctypes.pointer(arr.arr_reference), ctypes.c_float(q),
                                                  ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def kurtosis(arr):
    """ Returns the kurtosis of tss (calculated with the adjusted Fisher-Pearson
    standardized moment coefficient G2).

    :param arr: TSA array with the time series.
    :return: TSA array with the kurtosis of each time series.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.kurtosis(ctypes.pointer(arr.arr_reference),
                                        ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def large_standard_deviation(arr, r):
    """ Checks if the time series within tss have a large standard deviation.

    :param arr: TSA array with the time series.
    :param r: The threshold.
    :return: TSA array containing True for those time series in tss that have a large standard deviation.
    """

    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.large_standard_deviation(ctypes.pointer(arr.arr_reference), ctypes.c_float(r),
                                                        ctypes.pointer(b))

    return array(array_reference=b, tsa_type=dtype.b8)


def last_location_of_maximum(arr):
    """ Calculates the last location of the maximum value of each time series. The position
    is calculated relatively to the length of the series.

    :param arr: TSA array with the time series.
    :return: TSA array with the last relative location of the maximum value of each series.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.last_location_of_maximum(ctypes.pointer(arr.arr_reference),
                                                        ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def last_location_of_minimum(arr):
    """ Calculates the last location of the minimum value of each time series. The position
    is calculated relatively to the length of the series.

    :param arr: TSA array with the time series.
    :return: TSA array the last relative location of the minimum value of each series.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.last_location_of_minimum(ctypes.pointer(arr.arr_reference),
                                                        ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def length(arr):
    """ Returns the length of the input time series.

    :param arr: TSA array with the time series.
    :return: TSA array the length of tss.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.length(ctypes.pointer(arr.arr_reference),
                                      ctypes.pointer(b))

    return array(array_reference=b, tsa_type=dtype.s32)


def linear_trend(arr):
    """ Calculate a linear least-squares regression for the values of the time series versus the sequence from 0 to
    length of the time series minus one.

    :param arr: TSA array with the time series.
    :return  a tuple with:
            pvalue: TSA array the pvalues for all time series.
            rvalue: TSA array The rvalues for all time series.
            intercept: TSA array the intercept values for all time series.
            slope: TSA array the slope for all time series.
            stdrr: TSA array the stderr values for all time series.
    """
    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)
    d = ctypes.c_void_p(0)
    e = ctypes.c_void_p(0)
    f = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.linear_trend(ctypes.pointer(arr.arr_reference),
                                            ctypes.pointer(b),
                                            ctypes.pointer(c),
                                            ctypes.pointer(d),
                                            ctypes.pointer(e),
                                            ctypes.pointer(f)
                                            )

    return array(array_reference=b, tsa_type=arr.tsa_type), \
           array(array_reference=c, tsa_type=arr.tsa_type), \
           array(array_reference=d, tsa_type=arr.tsa_type), \
           array(array_reference=e, tsa_type=arr.tsa_type), \
           array(array_reference=f, tsa_type=arr.tsa_type)


def longest_strike_above_mean(arr):
    """ Calculates the length of the longest consecutive subsequence in tss that is bigger than the mean of tss.

    :param arr: TSA array with the time series.
    :return: TSA array with the length of the longest consecutive subsequence in the input time series that is bigger than the mean.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.longest_strike_above_mean(ctypes.pointer(arr.arr_reference),
                                                         ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def longest_strike_below_mean(arr):
    """ Calculates the length of the longest consecutive subsequence in tss that is below the mean of tss.

    :param arr: TSA array with the time series.
    :return: TSA array with the length of the longest consecutive subsequence in the input time series that is below the mean.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.longest_strike_below_mean(ctypes.pointer(arr.arr_reference),
                                                         ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def max_langevin_fixed_point(arr, m, r):
    """ Largest fixed point of dynamics  :math:`argmax_x {h(x)=0}` estimated from polynomial :math:`h(x)`,
    which has been fitted to the deterministic dynamics of Langevin model

    .. math::
        \dot(x)(t) = h(x(t)) + R \mathcal(N)(0,1)

    as described by

        Friedrich et al. (2000): Physics Letters A 271, p. 217-222
        *Extracting model equations from experimental data*

    :param arr: TSA array with the time series.
    :param m: Order of polynom to fit for estimating fixed points of dynamics.
    :param r: Number of quantiles to use for averaging.
    :return: TSA array with the largest fixed point of deterministic dynamics.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.max_langevin_fixed_point(ctypes.pointer(arr.arr_reference),
                                                        ctypes.c_int(m),
                                                        ctypes.c_float(r),
                                                        ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def maximum(arr):
    """ Calculates the maximum value for each time series within tss.

    :param arr: TSA array with the time series.
    :return: TSA array with the maximum value of each time series within tss.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.maximum(ctypes.pointer(arr.arr_reference),
                                       ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def mean(arr):
    """ Calculates the mean value for each time series within tss.

    :param arr: TSA array with the time series.
    :return: TSA array with the mean value of each time series within tss.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.mean(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def mean_absolute_change(arr):
    """ Calculates the mean over the absolute differences between subsequent time series values in tss.

    :param arr: TSA array with the time series.
    :return: TSA array with the mean over the absolute differences between subsequent time series values.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.mean_absolute_change(ctypes.pointer(arr.arr_reference),
                                                    ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def mean_change(arr):
    """ Calculates the mean over the differences between subsequent time series values in tss.

    :param arr: TSA array with the time series.
    :return: TSA array with the mean over the differences between subsequent time series values.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.mean_change(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def mean_second_derivative_central(arr):
    """ Calculates mean value of a central approximation of the second derivative for each time series in tss.

    :param arr: TSA array with the time series.
    :return: TSA array with the mean value of a central approximation of the second derivative for each time series.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.mean_second_derivative_central(ctypes.pointer(arr.arr_reference),
                                                              ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def median(arr):
    """ Calculates the median value for each time series within tss.

    :param arr: TSA array with the time series.
    :return: TSA array with the median value of each time series within tss.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.median(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def minimum(arr):
    """ Calculates the minimum value for each time series within tss.

    :param arr: TSA array with the time series.
    :return: TSA array with the minimum value of each time series within tss.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.minimum(ctypes.pointer(arr.arr_reference),
                                       ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def number_crossing_m(arr, m):
    """ Calculates the number of m-crossings. A m-crossing is defined as two sequential values where the first
    value is lower than m and the next is greater, or viceversa. If you set m to zero, you will get the number of
    zero crossings.

    :param arr: TSA array with the time series.
    :param m: The m value.
    :return: TSA array with the number of m-crossings of each time series within tss.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.number_crossing_m(ctypes.pointer(arr.arr_reference),
                                                 ctypes.c_int(m),
                                                 ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def number_peaks(arr, n):
    """Calculates the number of peaks of at least support :math: `n` in the time series :math: `tss`. A peak of support
    :math: `n` is defined as a subsequence of :math: `tss where a value occurs, which is bigger than
    its :math: `n` neighbours to the left and to the right.

    :param arr: TSA array with the time series.
    :param n: The support of the peak.
    :return: TSA array with the number of peaks of at least support :math: `n`.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.number_peaks(ctypes.pointer(arr.arr_reference), ctypes.c_int(n),
                                            ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def percentage_of_reoccurring_datapoints_to_all_datapoints(arr, is_sorted):
    """Calculates the percentage of unique values, that are present in the time series more than once.

    .. math::

        len(different values occurring more than once) / len(different values)

    This means the percentage is normalized to the number of unique values, in contrast to the
    percentageOfReoccurringValuesToAllValues.

    :param arr: TSA array with the time series.
    :param is_sorted: Indicates if the input time series is sorted or not. Defaults to false.
    :return: TSA array with the percentage of unique values, that are present in the time series more than once.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.percentage_of_reoccurring_datapoints_to_all_datapoints(ctypes.pointer(arr.arr_reference),
                                                                                      ctypes.c_bool(is_sorted),
                                                                                      ctypes.pointer(
                                                                                          b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def quantile(arr, q, precision=1e8):
    """Returns values at the given quantile.

    :param arr: TSA array with the time series.
    :param q: Tsa array with the percentile(s) at which to extract score(s). One or many.
    :param precision: Number of decimals expected.
    :return: Values at the given quantile.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.quantile(ctypes.pointer(arr.arr_reference), ctypes.pointer(q.arr_reference),
                                        ctypes.c_float(precision),
                                        ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def ratio_beyond_r_sigma(arr, r):
    """ Calculates the ratio of values that are more than :math: `r*std(x)` (so :math: `r` sigma) away from the mean of
    :math: `x`.

    :param arr: TSA array with the time series.
    :param r: Number of times that the values should be away from.
    :return: TSA array with the ratio of values that are more than :math: `r*std(x)` (so :math: `r` sigma) away from the mean of
    :math: `x`.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.ratio_beyond_r_sigma(ctypes.pointer(arr.arr_reference), ctypes.c_float(r),
                                                    ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def sample_entropy(arr):
    """ Calculates a vectorized sample entropy algorithm.
    https://en.wikipedia.org/wiki/Sample_entropy
    https://www.ncbi.nlm.nih.gov/pubmed/10843903?dopt=Abstract
    For short time-series this method is highly dependent on the parameters, but should be stable for N > 2000,
    see: Yentes et al. (2012) - The Appropriate Use of Approximate Entropy and Sample Entropy with Short Data Sets
    Other shortcomings and alternatives discussed in:
    Richman & Moorman (2000) - Physiological time-series analysis using approximate entropy and sample entropy.

    :param arr: TSA array with the time series.
    :return: TSA array with the same dimensions as tss, whose values (time series in dimension 0)
            contains the vectorized sample entropy for all the input time series in tss.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.sample_entropy(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def skewness(arr):
    """ Calculates the sample skewness of tss (calculated with the adjusted Fisher-Pearson standardized
    moment coefficient G1).

    :param arr: TSA array with the time series.
    :return: TSA array containing the skewness of each time series in tss.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.skewness(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def standard_deviation(arr):
    """ Calculates the standard deviation of each time series within tss.

    :param arr: TSA array with the time series.
    :return: TSA array with the standard deviation of each time series within tss.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.standard_deviation(ctypes.pointer(arr.arr_reference),
                                                  ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def sum_of_reoccurring_datapoints(arr, is_sorted=False):
    """Calculates the sum of all data points, that are present in the time series more than once.

    :param arr: TSA array with the time series.
    :param is_sorted: Indicates if the input time series is sorted or not. Defaults to false.
    :return: TSA array with the sum of all data points, that are present in the time series more than once.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.sum_of_reoccurring_datapoints(ctypes.pointer(arr.arr_reference),
                                                             ctypes.c_bool(is_sorted),
                                                             ctypes.pointer(b))

    return array(array_reference=b, tsa_type=arr.tsa_type)


def symmetry_looking(arr, r):
    """ Calculates if the distribution of tss *looks symmetric*. This is the case if
    .. math::

         | mean(tss)-median(tss)| < r * (max(tss)-min(tss))


    :param arr: TSA array with the time series.
    :param r: The percentage of the range to compare with.
    :return: TSA array denoting if the input time series look symmetric.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.symmetry_looking(ctypes.pointer(arr.arr_reference), ctypes.c_float(r),
                                                ctypes.pointer(b))

    return array(array_reference=b, tsa_type=dtype.b8)


def value_count(arr, v):
    """Counts occurrences of value in the time series tss.

    :param arr: TSA array with the time series.
    :param v: The value to be counted.
    :return: TSA array containing the count of the given value in each time series.
    """
    b = ctypes.c_void_p(0)

    TsaLibrary().c_tsa_library.value_count(ctypes.pointer(arr.arr_reference), ctypes.c_float(v),
                                           ctypes.pointer(b))

    return array(array_reference=b, tsa_type=dtype.u32)
