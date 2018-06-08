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


def abs_energy(arr):
    """ Calculates the sum over the square values of the time series.

    :param arr: KHIVA array with the time series.
    :type arr: khiva.array
    :return: KHIVA array with the absEnergy.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.abs_energy(ctypes.pointer(arr.arr_reference),
                                              ctypes.pointer(b))
    return Array(array_reference=b)


def absolute_sum_of_changes(arr):
    """ Calculates the value of an aggregation function f_agg (e.g. var or mean) of the autocorrelation
    (Compare to http://en.wikipedia.org/wiki/Autocorrelation#Estimation), taken over different all possible
    lags (1 to length of x)

    :param arr: KHIVA array with the time series.
    :type arr: khiva.array
    :return: KHIVA array with the absolute sum of changes.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.absolute_sum_of_changes(ctypes.pointer(arr.arr_reference),
                                                           ctypes.pointer(b))
    return Array(array_reference=b)


def aggregated_autocorrelation(arr, aggregation_function):
    """ Calculates a linear least-squares regression for values of the time series that were aggregated
    over chunks versus the sequence from 0 up to the number of chunks minus one.

    :param arr: A KHIVA array with the time series.
    :param aggregation_function: Function to be used in the aggregation. It receives an integer which indicates
                                the function to be applied.
                                0 : mean,
                                1 : median
                                2 : min,
                                3 : max,
                                4 : stdev,
                                5 : var,
                                default : mean

    :return: KHIVA array that contains the aggregated correlation for each time series.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.aggregated_autocorrelation(ctypes.pointer(arr.arr_reference),
                                                              ctypes.pointer(ctypes.c_int(aggregation_function)),
                                                              ctypes.pointer(b))

    return Array(array_reference=b)


def aggregated_linear_trend(arr, chunk_size, aggregation_function):
    """ Calculates a linear least-squares regression for values of the time series that were aggregated
    over chunks versus the sequence from 0 up to the number of chunks minus one.

    :param arr: A KHIVA array with the time series.
    :param chunk_size: The chunk size used to aggregate the data.
    :param aggregation_function: Function to be used in the aggregation. It receives an integer which indicates the
                                function to be applied:
                                0 : mean,
                                1 : median
                                2 : min,
                                3 : max,
                                4 : stdev,
                                default : mean
    :return: ( pvalue: KHIVA array with the pvalues for all time series.
            rvalue: KHIVA array with the rvalues for all time series.
            intercept: KHIVA array with the intercept values for all time series.
            slope: KHIVA array with the slope for all time series.
            stdrr: KHIVA array with the stderr values for all time series. )
    """
    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)
    d = ctypes.c_void_p(0)
    e = ctypes.c_void_p(0)
    f = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.aggregated_linear_trend(ctypes.pointer(arr.arr_reference),
                                                           ctypes.pointer(ctypes.c_long(chunk_size)),
                                                           ctypes.pointer(ctypes.c_int(aggregation_function)),
                                                           ctypes.pointer(b),
                                                           ctypes.pointer(c),
                                                           ctypes.pointer(d),
                                                           ctypes.pointer(e),
                                                           ctypes.pointer(f))

    return Array(array_reference=b), Array(array_reference=c,
                                           khiva_type=arr.khiva_type), Array(
        array_reference=d), Array(array_reference=e), Array(
        array_reference=f)


def approximate_entropy(arr, m, r):
    """ Calculates a vectorized Approximate entropy algorithm.
    https://en.wikipedia.org/wiki/Approximate_entropy
    For short time-series this method is highly dependent on the parameters, but should be stable for N > 2000,
    see: Yentes et al. (2012) - The Appropriate Use of Approximate Entropy and Sample Entropy with Short Data Sets
    Other shortcomings and alternatives discussed in:
    Richman & Moorman (2000) - Physiological time-series analysis using approximate entropy and sample entropy


    :param arr: A KHIVA array with the time series.
    :param m: Length of compared run of data.
    :param r: Filtering level, must be positive.
    :return: KHIVA array with the vectorized approximate entropy for all the input time series in tss.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.approximate_entropy(ctypes.pointer(arr.arr_reference),
                                                       ctypes.pointer(ctypes.c_int(m)),
                                                       ctypes.pointer(ctypes.c_float(r)),
                                                       ctypes.pointer(b))

    return Array(array_reference=b)


def cross_covariance(xss, yss, unbiased):
    """ Calculates the cross-covariance of the given time series.

    :param xss: A KHIVA array with time series.
    :param yss: A KHIVA Array with time series.
    :param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :return: KHIVA array with the cross-covariance value for the given time series.
    """

    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.cross_covariance(ctypes.pointer(xss.arr_reference),
                                                    ctypes.pointer(yss.arr_reference),
                                                    ctypes.pointer(ctypes.c_bool(unbiased)), ctypes.pointer(b))

    return Array(array_reference=b)


def auto_covariance(arr, unbiased=False):
    """ Calculates the auto-covariance the given time series.

    :param arr: KHIVA array with the time series.
    :param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :return: KHIVA array with the auto-covariance value for the given time series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.auto_covariance(ctypes.pointer(arr.arr_reference),
                                                   ctypes.pointer(ctypes.c_bool(unbiased)),
                                                   ctypes.pointer(b))

    return Array(array_reference=b)


def cross_correlation(xss, yss, unbiased):
    """ Calculates the cross-correlation of the given time series.

    :param xss: KHIVA array with the time series.
    :param yss: KHIVA array with the time series.
    :param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :return: KHIVA array with cross-correlation value for the given time series.
    """

    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.cross_correlation(ctypes.pointer(xss.arr_reference),
                                                     ctypes.pointer(yss.arr_reference),
                                                     ctypes.pointer(ctypes.c_bool(unbiased)), ctypes.pointer(b))

    return Array(array_reference=b)


def auto_correlation(arr, max_lag, unbiased):
    """ Calculates the autocorrelation of the specified lag for the given time series.

    :param arr: KHIVA array with the time series.
    :param max_lag: The maximum lag to compute.
    :param unbiased: Determines whether it divides by n - lag (if true) or n (if false).
    :return: KHIVA array with the autocorrelation value for the given time series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.auto_correlation(ctypes.pointer(arr.arr_reference),
                                                    ctypes.pointer(ctypes.c_long(max_lag)),
                                                    ctypes.pointer(ctypes.c_bool(unbiased)),
                                                    ctypes.pointer(b))

    return Array(array_reference=b)


def binned_entropy(arr, max_bins):
    """ Calculates the binned entropy for the given time series and number of bins.

    :param arr: KHIVA array with the time series.
    :param max_bins: The number of bins.
    :return: KHIVA array with the binned entropy value for the given time series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.binned_entropy(ctypes.pointer(arr.arr_reference),
                                                  ctypes.pointer(ctypes.c_int(max_bins)),
                                                  ctypes.pointer(b))

    return Array(array_reference=b)


def c3(arr, lag):
    """ Calculates the Schreiber, T. and Schmitz, A. (1997) measure of non-linearity
    for the given time series

    :param arr: KHIVA array with the time series.
    :param lag: The lag.
    :return: KHIVA array with non-linearity value for the given time series.
    """

    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.c3(ctypes.pointer(arr.arr_reference),
                                      ctypes.pointer(ctypes.c_long(lag)), ctypes.pointer(b))

    return Array(array_reference=b)


def cid_ce(arr, z_normalize):
    """ Calculates an estimate for the time series complexity defined by
    Batista, Gustavo EAPA, et al (2014). (A more complex time series has more peaks,
    valleys, etc.)

    :param arr: KHIVA array with the time series.
    :param z_normalize: Controls wheter the time series should be z-normalized or not.
    :return: KHIVA array with the complexity value for the given time series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.cid_ce(ctypes.pointer(arr.arr_reference),
                                          ctypes.pointer(ctypes.c_bool(z_normalize)), ctypes.pointer(b))

    return Array(array_reference=b)


def count_above_mean(arr):
    """ Calculates the number of values in the time series that are higher than
    the mean.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the number of values in the time series that are higher than the mean.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.count_above_mean(ctypes.pointer(arr.arr_reference),
                                                    ctypes.pointer(b))

    return Array(array_reference=b)


def count_below_mean(arr):
    """ Calculates the number of values in the time series that are lower than
    the mean.

    :param arr: KHIVA array with the time series.
    :return: KHIVA Array with the number of values in the time series that are lower than the mean.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.count_below_mean(ctypes.pointer(arr.arr_reference),
                                                    ctypes.pointer(b))

    return Array(array_reference=b)


def cwt_coefficients(tss, widths, coeff, w):
    """ Calculates a Continuous wavelet transform for the Ricker wavelet, also known as
    the "Mexican hat wavelet".

    :param tss: KHIVA array with the time series.
    :param widths: Widths. It accepts a list of lists or a numpy array with one or several widths.
    :param coeff: Coefficient of interest.
    :param w: Width of interest.
    :return: KHIVA Array with the result of calculated coefficients.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.cwt_coefficients(ctypes.pointer(tss.arr_reference),
                                                    ctypes.pointer(widths.arr_reference),
                                                    ctypes.pointer(ctypes.c_int(coeff)),
                                                    ctypes.pointer(ctypes.c_int(w)),
                                                    ctypes.pointer(b))

    return Array(array_reference=b)


def energy_ratio_by_chunks(arr, num_segments, segment_focus):
    """ Calculates the sum of squares of chunk i out of N chunks expressed as a ratio
    with the sum of squares over the whole series. segmentFocus should be lower
    than the number of segments.

    :param arr: KHIVA array with the time series.
    :param num_segments: The number of segments to divide the series into.
    :param segment_focus: The segment number (starting at zero) to return a feature on.
    :return: KHIVA array with the energy ratio by chunk of the time series.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.energy_ratio_by_chunks(ctypes.pointer(arr.arr_reference),
                                                          ctypes.pointer(ctypes.c_long(num_segments)),
                                                          ctypes.pointer(ctypes.c_long(segment_focus)),
                                                          ctypes.pointer(b))

    return Array(array_reference=b)


def fft_aggregated(arr):
    """ Calculates the spectral centroid(mean), variance, skew, and kurtosis of the absolute fourier transform
    spectrum.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the spectral centroid (mean), variance, skew, and kurtosis of the absolute fourier transform
            spectrum.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.fft_aggregated(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)


def fft_coefficient(arr, coefficient):
    """ Calculates the fourier coefficients of the one-dimensional discrete
    Fourier Transform for real input by fast fourier transformation algorithm.

    :param arr: KHIVA array with the time series.
    :param coefficient: The coefficient to extract from the FFT.
    :return: Tuple with:
        real: KHIVA array with the real part of the coefficient.
        imag: KHIVA array with the imaginary part of the coefficient.
        abs: KHIVA array with the absolute value of the coefficient.
        angle: KHIVA array with the angle of the coefficient.
    """
    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)
    d = ctypes.c_void_p(0)
    e = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.fft_coefficient(ctypes.pointer(arr.arr_reference),
                                                   ctypes.pointer(ctypes.c_long(coefficient)),
                                                   ctypes.pointer(b),
                                                   ctypes.pointer(c),
                                                   ctypes.pointer(d),
                                                   ctypes.pointer(e)
                                                   )

    return Array(array_reference=b), Array(array_reference=c,
                                           khiva_type=arr.khiva_type), Array(
        array_reference=d), Array(array_reference=e)


def first_location_of_maximum(arr):
    """ Calculates the first relative location of the maximal value for each time series.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the first relative location of the maximum value to the length of the time series, for each
            time series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.first_location_of_maximum(ctypes.pointer(arr.arr_reference),
                                                             ctypes.pointer(b))

    return Array(array_reference=b)


def first_location_of_minimum(arr):
    """ Calculates the first location of the minimal value of each time series. The position is calculated relatively
    to the length of the series.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the first relative location of the minimal value of each series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.first_location_of_minimum(ctypes.pointer(arr.arr_reference),
                                                             ctypes.pointer(b))

    return Array(array_reference=b)


def friedrich_coefficients(arr, m, r):
    """ Coefficients of polynomial :math:`h(x)`, which has been fitted to the deterministic dynamics of Langevin model:
    Largest fixed point of dynamics  :math:`argmax_x {h(x)=0}` estimated from polynomial :math:`h(x)`,
    which has been fitted to the deterministic dynamics of Langevin model:

    .. math::
        \\dot(x)(t) = h(x(t)) + R \\mathcal(N)(0,1)

    as described by [1]. For short time series this method is highly dependent on the parameters.

    [1] Friedrich et al. (2000): Physics Letters A 271, p. 217-222
    Extracting model equations from experimental data.


    :param arr: KHIVA array with the time series.
    :param m: Order of polynom to fit for estimating fixed points of dynamics.
    :param r: Number of quantiles to use for averaging.
    :return: KHIVA array with the coefficients for each time seriess.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.friedrich_coefficients(ctypes.pointer(arr.arr_reference),
                                                          ctypes.pointer(ctypes.c_int(m)),
                                                          ctypes.pointer(ctypes.c_float(r)),
                                                          ctypes.pointer(b))

    return Array(array_reference=b)


def has_duplicates(arr):
    """ Calculates if the input time series contain duplicated elements.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array containing True if the time series contains duplicated elements
     and false otherwise.
    """

    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.has_duplicates(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)


def has_duplicate_max(arr):
    """ Calculates if the maximum within input time series is duplicated.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array containing True if the maximum value of the time series is duplicated and false otherwise.
    """

    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.has_duplicate_max(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)


def has_duplicate_min(arr):
    """ Calculates if the minimum of the input time series is duplicated.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array containing True if the minimum of the time series is duplicated and False otherwise.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.has_duplicate_min(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)


def index_mass_quantile(arr, q):
    """ Calculates the index of the mass quantile.

    :param arr: KHIVA array with the time series.
    :param q: The quantile.
    :return: KHIVA array with the index of the mass quantile q.
    """

    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.index_mass_quantile(ctypes.pointer(arr.arr_reference),
                                                       ctypes.pointer(ctypes.c_float(q)),
                                                       ctypes.pointer(b))

    return Array(array_reference=b)


def kurtosis(arr):
    """ Returns the kurtosis of tss (calculated with the adjusted Fisher-Pearson
    standardized moment coefficient G2).

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the kurtosis of each time series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.kurtosis(ctypes.pointer(arr.arr_reference),
                                            ctypes.pointer(b))

    return Array(array_reference=b)


def large_standard_deviation(arr, r):
    """ Checks if the time series within tss have a large standard deviation.

    :param arr: KHIVA array with the time series.
    :param r: The threshold.
    :return: KHIVA array containing True for those time series in tss that have a large standard deviation.
    """

    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.large_standard_deviation(ctypes.pointer(arr.arr_reference),
                                                            ctypes.pointer(ctypes.c_float(r)),
                                                            ctypes.pointer(b))

    return Array(array_reference=b)


def last_location_of_maximum(arr):
    """ Calculates the last location of the maximum value of each time series. The position
    is calculated relatively to the length of the series.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the last relative location of the maximum value of each series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.last_location_of_maximum(ctypes.pointer(arr.arr_reference),
                                                            ctypes.pointer(b))

    return Array(array_reference=b)


def last_location_of_minimum(arr):
    """ Calculates the last location of the minimum value of each time series. The position
    is calculated relatively to the length of the series.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array the last relative location of the minimum value of each series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.last_location_of_minimum(ctypes.pointer(arr.arr_reference),
                                                            ctypes.pointer(b))

    return Array(array_reference=b)


def length(arr):
    """ Returns the length of the input time series.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array the length of tss.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.length(ctypes.pointer(arr.arr_reference),
                                          ctypes.pointer(b))

    return Array(array_reference=b)


def linear_trend(arr):
    """ Calculate a linear least-squares regression for the values of the time series versus the sequence from 0 to
    length of the time series minus one.

    :param arr: KHIVA array with the time series.
    :return  a tuple with:
            pvalue: KHIVA array the pvalues for all time series.
            rvalue: KHIVA array The rvalues for all time series.
            intercept: KHIVA array the intercept values for all time series.
            slope: KHIVA array the slope for all time series.
            stdrr: KHIVA array the stderr values for all time series.
    """
    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)
    d = ctypes.c_void_p(0)
    e = ctypes.c_void_p(0)
    f = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.linear_trend(ctypes.pointer(arr.arr_reference),
                                                ctypes.pointer(b),
                                                ctypes.pointer(c),
                                                ctypes.pointer(d),
                                                ctypes.pointer(e),
                                                ctypes.pointer(f)
                                                )

    return Array(array_reference=b), \
           Array(array_reference=c), \
           Array(array_reference=d), \
           Array(array_reference=e), \
           Array(array_reference=f)


def local_maximals(arr):
    """ Calculates all Local Maximals fot the time series in array.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the calculated local maximals for each time series in arr.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.local_maximals(ctypes.pointer(arr.arr_reference),
                                                  ctypes.pointer(b))

    return Array(array_reference=b)


def longest_strike_above_mean(arr):
    """ Calculates the length of the longest consecutive subsequence in tss that is bigger than the mean of tss.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the length of the longest consecutive subsequence in the input time series that is bigger
            than the mean.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.longest_strike_above_mean(ctypes.pointer(arr.arr_reference),
                                                             ctypes.pointer(b))

    return Array(array_reference=b)


def longest_strike_below_mean(arr):
    """ Calculates the length of the longest consecutive subsequence in tss that is below the mean of tss.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the length of the longest consecutive subsequence in the input time series that is below
            the mean.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.longest_strike_below_mean(ctypes.pointer(arr.arr_reference),
                                                             ctypes.pointer(b))

    return Array(array_reference=b)


def max_langevin_fixed_point(arr, m, r):
    """ Largest fixed point of dynamics  :math:`argmax_x {h(x)=0}` estimated from polynomial :math:`h(x)`,
    which has been fitted to the deterministic dynamics of Langevin model

    .. math::
        \\dot(x)(t) = h(x(t)) + R \\mathcal(N)(0,1)

    as described by

        Friedrich et al. (2000): Physics Letters A 271, p. 217-222
        *Extracting model equations from experimental data*

    :param arr: KHIVA array with the time series.
    :param m: Order of polynom to fit for estimating fixed points of dynamics.
    :param r: Number of quantiles to use for averaging.
    :return: KHIVA array with the largest fixed point of deterministic dynamics.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.max_langevin_fixed_point(ctypes.pointer(arr.arr_reference),
                                                            ctypes.pointer(ctypes.c_int(m)),
                                                            ctypes.pointer(ctypes.c_float(r)),
                                                            ctypes.pointer(b))

    return Array(array_reference=b)


def maximum(arr):
    """ Calculates the maximum value for each time series within tss.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the maximum value of each time series within tss.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.maximum(ctypes.pointer(arr.arr_reference),
                                           ctypes.pointer(b))

    return Array(array_reference=b)


def mean(arr):
    """ Calculates the mean value for each time series within tss.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the mean value of each time series within tss.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.mean(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)


def mean_absolute_change(arr):
    """ Calculates the mean over the absolute differences between subsequent time series values in tss.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the mean over the absolute differences between subsequent time series values.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.mean_absolute_change(ctypes.pointer(arr.arr_reference),
                                                        ctypes.pointer(b))

    return Array(array_reference=b)


def mean_change(arr):
    """ Calculates the mean over the differences between subsequent time series values in tss.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the mean over the differences between subsequent time series values.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.mean_change(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)


def mean_second_derivative_central(arr):
    """ Calculates mean value of a central approximation of the second derivative for each time series in tss.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the mean value of a central approximation of the second derivative for each time series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.mean_second_derivative_central(ctypes.pointer(arr.arr_reference),
                                                                  ctypes.pointer(b))

    return Array(array_reference=b)


def median(arr):
    """ Calculates the median value for each time series within tss.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the median value of each time series within tss.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.median(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)


def minimum(arr):
    """ Calculates the minimum value for each time series within tss.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the minimum value of each time series within tss.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.minimum(ctypes.pointer(arr.arr_reference),
                                           ctypes.pointer(b))

    return Array(array_reference=b)


def number_crossing_m(arr, m):
    """ Calculates the number of m-crossings. A m-crossing is defined as two sequential values where the first
    value is lower than m and the next is greater, or viceversa. If you set m to zero, you will get the number of
    zero crossings.

    :param arr: KHIVA array with the time series.
    :param m: The m value.
    :return: KHIVA array with the number of m-crossings of each time series within tss.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.number_crossing_m(ctypes.pointer(arr.arr_reference),
                                                     ctypes.pointer(ctypes.c_int(m)),
                                                     ctypes.pointer(b))

    return Array(array_reference=b)


def number_cwt_peaks(arr, max_w):
    """ This feature calculator searches for different peaks. To do so, the time series is smoothed by a ricker
    wavelet and for widths ranging from 1 to :math:'max_w`. This feature calculator returns the number of peaks that
    occur at enough width scales and with sufficiently high Signal-to-Noise-Ratio (SNR).

    :param arr: KHIVA array with the time series.
    :param max_w: The maximum width to consider.
    :return: KHIVA array with the number of peaks for each time series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.number_cwt_peaks(ctypes.pointer(arr.arr_reference),
                                                    ctypes.pointer(ctypes.c_int(max_w)),
                                                    ctypes.pointer(b))

    return Array(array_reference=b)


def number_peaks(arr, n):
    """ Calculates the number of peaks of at least support :math:`n` in the time series :math:`tss`. A peak of support
    :math:`n` is defined as a subsequence of :math:`tss where a value occurs, which is bigger than
    its :math:`n` neighbours to the left and to the right.

    :param arr: KHIVA array with the time series.
    :param n: The support of the peak.
    :return: KHIVA array with the number of peaks of at least support :math:`n`.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.number_peaks(ctypes.pointer(arr.arr_reference), ctypes.pointer(ctypes.c_int(n)),
                                                ctypes.pointer(b))

    return Array(array_reference=b)


def partial_autocorrelation(arr, lags):
    """ Calculates the value of the partial autocorrelation function at the given lag. The lag :math:`k'`  partial
    autocorrelation of a time series :math:`\\lbrace x_t, t = 1 \\ldots T \\rbrace` equals the partial correlation of
    :math:`x_t` and :math:`x_{t-k}`, adjusted for the intermediate variables :math:`\\lbrace x_{t-1}, \\ldots, x_{t-k+1}\\rbrace`
    ([1]). Following [2], it can be defined as:

    .. math::
          \\alpha_k = \\frac{ Cov(x_t, x_{t-k} | x_{t-1}, \\ldots, x_{t-k+1})}
          {\\sqrt{ Var(x_t | x_{t-1}, \\ldots, x_{t-k+1}) Var(x_{t-k} | x_{t-1}, \\ldots, x_{t-k+1} )}}

    with (a) :math:`x_t = f(x_{t-1}, \\ldots, x_{t-k+1})` and (b) :math:`x_{t-k} = f(x_{t-1}, \\ldots, x_{t-k+1})`
    being AR(k-1) models that can be fitted by OLS. Be aware that in (a), the regression is done on past values to
    predict :math:`x_t` whereas in (b), future values are used to calculate the past value :math:`x_{t-k}`.
    It is said in [1] that "for an AR(p), the partial autocorrelations :math:`\\alpha_k` will be nonzero for :math:`k<=p`
    and zero for :math:`k>p`."
    With this property, it is used to determine the lag of an AR-Process.

    [1] Box, G. E., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M. (2015).
    Time series analysis: forecasting and control. John Wiley & Sons.
    [2] https://onlinecourses.science.psu.edu/stat510/node/62

    :param arr: KHIVA array with the time series.
    :param lags: KHIVA array with the lags to be calculated.
    :return: KHIVA array with the partial autocorrelation for each time series for the given lag.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.partial_autocorrelation(ctypes.pointer(arr.arr_reference),
                                                           ctypes.pointer(lags.arr_reference),
                                                           ctypes.pointer(b))

    return Array(array_reference=b)


def percentage_of_reoccurring_datapoints_to_all_datapoints(arr, is_sorted):
    """ Calculates the percentage of unique values, that are present in the time series more than once.

    .. math::

        len(different values occurring more than once) / len(different values)

    This means the percentage is normalized to the number of unique values, in contrast to the
    percentage_of_reoccurring_values_to_all_values.

    :param arr: KHIVA array with the time series.
    :param is_sorted: Indicates if the input time series is sorted or not. Defaults to false.
    :return: KHIVA array with the percentage of unique values, that are present in the time series more than once.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.percentage_of_reoccurring_datapoints_to_all_datapoints(
        ctypes.pointer(arr.arr_reference),
        ctypes.pointer(
            ctypes.c_bool(is_sorted)),
        ctypes.pointer(
            b))

    return Array(array_reference=b)


def percentage_of_reoccurring_values_to_all_values(arr, is_sorted):
    """ Calculates the percentage of unique values, that are present in the time series more than once.

    .. math::

        \\frac{\\textit{number of data points occurring more than once}}{\\textit{number of all data points})}

    This means the percentage is normalized to the number of unique values, in contrast to the
    percentage_of_reoccurring_datapoints_to_all_datapoints.

    :param arr: KHIVA array with the time series.
    :param is_sorted: Indicates if the input time series is sorted or not. Defaults to false.
    :return: KHIVA array with the percentage of unique values, that are present in the time series more than once.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.percentage_of_reoccurring_values_to_all_values(ctypes.pointer(arr.arr_reference),
                                                                                  ctypes.pointer(
                                                                                      ctypes.c_bool(is_sorted)),
                                                                                  ctypes.pointer(b))

    return Array(array_reference=b)


def quantile(arr, q, precision=1e8):
    """ Returns values at the given quantile.

    :param arr: KHIVA array with the time series.
    :param q: Khiva array with the percentile(s) at which to extract score(s). One or many.
    :param precision: Number of decimals expected.
    :return: Values at the given quantile.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.quantile(ctypes.pointer(arr.arr_reference), ctypes.pointer(q.arr_reference),
                                            ctypes.pointer(ctypes.c_float(precision)),
                                            ctypes.pointer(b))

    return Array(array_reference=b)


def range_count(arr, min, max):
    """ Counts observed values within the interval [min, max).

    :param arr: KHIVA array with the time series.
    :param min: Value that sets the lower limit.
    :param max: Value that sets the upper limit.
    :return: KHIVA array with the values at the given range.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.range_count(ctypes.pointer(arr.arr_reference),
                                               ctypes.pointer(ctypes.c_int(min)),
                                               ctypes.pointer(ctypes.c_float(max)),
                                               ctypes.pointer(b))

    return Array(array_reference=b)


def ratio_beyond_r_sigma(arr, r):
    """ Calculates the ratio of values that are more than :math:`r*std(x)` (so :math:`r` sigma) away from the mean of
    :math:`x`.

    :param arr: KHIVA array with the time series.
    :param r: Number of times that the values should be away from.
    :return: KHIVA array with the ratio of values that are more than :math:`r*std(x)` (so :math:`r` sigma) away from
            the mean of :math:`x`.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.ratio_beyond_r_sigma(ctypes.pointer(arr.arr_reference),
                                                        ctypes.pointer(ctypes.c_float(r)),
                                                        ctypes.pointer(b))

    return Array(array_reference=b)


def ratio_value_number_to_time_series_length(arr):
    """ Calculates a factor which is 1 if all values in the time series occur only once, and below one if this is
    not the case. In principle, it just returns:

    .. math::
        \\frac{\\textit{number unique values}}{\\textit{number values}}

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the ratio of unique values with respect to the total number of values.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.ratio_value_number_to_time_series_length(ctypes.pointer(arr.arr_reference),
                                                                            ctypes.pointer(b))

    return Array(array_reference=b)


def sample_entropy(arr):
    """ Calculates a vectorized sample entropy algorithm.
    https://en.wikipedia.org/wiki/Sample_entropy
    https://www.ncbi.nlm.nih.gov/pubmed/10843903?dopt=Abstract
    For short time-series this method is highly dependent on the parameters, but should be stable for N > 2000,
    see: Yentes et al. (2012) - The Appropriate Use of Approximate Entropy and Sample Entropy with Short Data Sets
    Other shortcomings and alternatives discussed in:
    Richman & Moorman (2000) - Physiological time-series analysis using approximate entropy and sample entropy.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the same dimensions as tss, whose values (time series in dimension 0)
            contains the vectorized sample entropy for all the input time series in tss.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.sample_entropy(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)


def skewness(arr):
    """ Calculates the sample skewness of tss (calculated with the adjusted Fisher-Pearson standardized
    moment coefficient G1).

    :param arr: KHIVA array with the time series.
    :return: KHIVA array containing the skewness of each time series in tss.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.skewness(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)


def spkt_welch_density(arr, coeff):
    """ Estimates the cross power spectral density of the time series array at different frequencies. To do so, the
    time series is first shifted from the time domain to the frequency domain.

    Welch's method computes an estimate of the power spectral density by dividing the data into overlapping
    segments, computing a modified periodogram for each segment and averaging the periodograms.
    [1] P. Welch, "The use of the fast Fourier transform for the estimation of power spectra: A method based on time
    averaging over short, modified periodograms", IEEE Trans. Audio Electroacoust. vol. 15, pp. 70-73, 1967.
    [2] M.S. Bartlett, "Periodogram Analysis and Continuous Spectra", Biometrika, vol. 37, pp. 1-16, 1950.
    [3] Rabiner, Lawrence R., and B. Gold. "Theory and Application of Digital Signal Processing" Prentice-Hall, pp.
    414-419, 1975.

    :param arr: KHIVA array with the time series.
    :param coeff: The coefficient to be returned.
    :return: KHIVA array containing the power spectrum of the different frequencies for each time series in arr.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.spkt_welch_density(ctypes.pointer(arr.arr_reference),
                                                      ctypes.pointer(ctypes.c_int(coeff)), ctypes.pointer(b))

    return Array(array_reference=b)


def standard_deviation(arr):
    """ Calculates the standard deviation of each time series within tss.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array with the standard deviation of each time series within tss.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.standard_deviation(ctypes.pointer(arr.arr_reference),
                                                      ctypes.pointer(b))

    return Array(array_reference=b)


def sum_of_reoccurring_datapoints(arr, is_sorted=False):
    """ Calculates the sum of all data points, that are present in the time series more than once.

    :param arr: KHIVA array with the time series.
    :param is_sorted: Indicates if the input time series is sorted or not. Defaults to false.
    :return: KHIVA array with the sum of all data points, that are present in the time series more than once.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.sum_of_reoccurring_datapoints(ctypes.pointer(arr.arr_reference),
                                                                 ctypes.pointer(ctypes.c_bool(is_sorted)),
                                                                 ctypes.pointer(b))

    return Array(array_reference=b)


def sum_of_reoccurring_values(arr, is_sorted=False):
    """ Calculates the sum of all values, that are present in the time series more than once.

    :param arr: KHIVA array with the time series.
    :param is_sorted: Indicates if the input time series is sorted or not. Defaults to false.
    :return: KHIVA array with the sum of all values, that are present in the time series more than once.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.sum_of_reoccurring_values(ctypes.pointer(arr.arr_reference),
                                                             ctypes.pointer(ctypes.c_bool(is_sorted)),
                                                             ctypes.pointer(b))

    return Array(array_reference=b)


def sum_values(arr):
    """ Calculates the sum over the time series arr.

    :param arr: KHIVA array with the time series.
    :param is_sorted: Indicates if the input time series is sorted or not. Defaults to false.
    :return: KHIVA array with the sum of values in each time series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.sum_values(ctypes.pointer(arr.arr_reference),
                                              ctypes.pointer(b))

    return Array(array_reference=b)


def symmetry_looking(arr, r):
    """ Calculates if the distribution of tss *looks symmetric*. This is the case if

    .. math::

         | mean(tss)-median(tss)| < r * (max(tss)-min(tss))


    :param arr: KHIVA array with the time series.
    :param r: The percentage of the range to compare with.
    :return: KHIVA array denoting if the input time series look symmetric.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.symmetry_looking(ctypes.pointer(arr.arr_reference),
                                                    ctypes.pointer(ctypes.c_float(r)),
                                                    ctypes.pointer(b))

    return Array(array_reference=b)


def time_reversal_asymmetry_statistic(arr, lag):
    """ This function calculates the value of:

    .. math::

        \\frac{1}{n-2lag} \\sum_{i=0}^{n-2lag} x_{i + 2 \\cdot lag}^2 \\cdot x_{i + lag} - x_{i + lag} \\cdot  x_{i}^2

    which is

    .. math::

        \\mathbb{E}[L^2(X)^2 \\cdot L(X) - L(X) \\cdot X^2]

    where :math:`\\mathbb{E}` is the mean and :math:`L` is the lag operator. It was proposed in [1] as a promising
    feature to extract from time series.

    :param arr: KHIVA array with the time series.
    :param lag: The lag to be computed.
    :return: KHIVA array containing the count of the given value in each time series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.time_reversal_asymmetry_statistic(ctypes.pointer(arr.arr_reference),
                                                                     ctypes.pointer(ctypes.c_int(lag)),
                                                                     ctypes.pointer(b))

    return Array(array_reference=b)


def value_count(arr, v):
    """ Counts occurrences of value in the time series tss.

    :param arr: KHIVA array with the time series.
    :param v: The value to be counted.
    :return: KHIVA array containing the count of the given value in each time series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.value_count(ctypes.pointer(arr.arr_reference), ctypes.pointer(ctypes.c_float(v)),
                                               ctypes.pointer(b))

    return Array(array_reference=b)


def variance(arr):
    """ Computes the variance for the time series array.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array containing the variance in each time series.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.variance(ctypes.pointer(arr.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)


def variance_larger_than_standard_deviation(arr):
    """ Calculates if the variance of array is greater than the standard deviation. In other words, if the variance of
    array is larger than 1.

    :param arr: KHIVA array with the time series.
    :return: KHIVA array denoting if the variance of array is greater than the standard deviation.
    """
    b = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.variance_larger_than_standard_deviation(ctypes.pointer(arr.arr_reference),
                                                                           ctypes.pointer(b))

    return Array(array_reference=b)
