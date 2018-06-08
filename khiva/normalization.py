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

def decimal_scaling_norm(tss):
    """ Normalizes the given time series according to its maximum value and adjusts each value within the range (-1, 1).

    :param tss: KHIVA array with the time series.

    :return: KHIVA array with the same dimensions as tss, whose values (time series in dimension 0) have been
             normalized by dividing each number by :math::`10^j` , where j is the number of integer digits of the max number in
             the time series.`
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.decimal_scaling_norm(ctypes.pointer(tss.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)


def decimal_scaling_norm_in_place(tss):
    """ Same as decimal_scaling_norm, but it performs the operation in place, without allocating further memory.

    :param tss: KHIVA array with the time series.
    """
    KhivaLibrary().c_khiva_library.decimal_scaling_norm_in_place(ctypes.pointer(tss.arr_reference))


def max_min_norm(tss, high=1.0, low=0.0, epsilon=0.00000001):
    """ Normalizes the given time series according to its minimum and maximum value and adjusts each value within the
    range [low, high].

    :param tss: KHIVA array with the time series.
    :param high: Maximum final value (Defaults to 1.0).
    :param low: Minimum final value (Defaults to 0.0).
    :param epsilon: Safeguard for constant (or near constant) time series as the operation implies a unit scale
                    operation between min and max values in the tss.

    :return: KHIVA array with the same dimensions as tss where the time series have been adjusted for zero mean and
            one as standard deviation.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.max_min_norm(ctypes.pointer(tss.arr_reference),
                                                ctypes.pointer(ctypes.c_double(high)),
                                                ctypes.pointer(ctypes.c_double(low)),
                                                ctypes.pointer(ctypes.c_double(epsilon)),
                                                ctypes.pointer(b))

    return Array(array_reference=b)


def max_min_norm_in_place(tss, high=1.0, low=0.0, epsilon=0.00000001):
    """ Same as max_min_norm, but it performs the operation in place, without allocating further memory.

    :param tss: KHIVA array with the time series.
    :param high: Maximum final value (Defaults to 1.0).
    :param low: Minimum final value (Defaults to 0.0).
    :param epsilon: Safeguard for constant (or near constant) time series as the operation implies a unit scale
                    operation between min and max values in the tss.
    """
    KhivaLibrary().c_khiva_library.max_min_norm_in_place(ctypes.pointer(tss.arr_reference),
                                                         ctypes.pointer(ctypes.c_double(high)),
                                                         ctypes.pointer(ctypes.c_double(low)),
                                                         ctypes.pointer(ctypes.c_double(epsilon)))


def mean_norm(tss):
    """ Normalizes the given time series according to its maximum-minimum value and its mean. It follows the following
    formulae:

    .. math::
        \\acute{x} = frac{x - mean(x)}{max(x) - min(x)}.

    :param tss: KHIVA array with the time series.

    :return: An array with the same dimensions as tss, whose values (time series in dimension 0) have been
            normalized by substracting the mean from each number and dividing each number by :math:`max(x) - min(`x)`,
            in the time series.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.mean_norm(ctypes.pointer(tss.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)


def mean_norm_in_place(tss):
    """ Normalizes the given time series according to its maximum-minimum value and its mean. It follows the following
    formulae:

    .. math:
        \\acute{x} = frac{x - mean(x)}{max(x) - min(x)}.

    :param tss: KHIVA array with the time series.
    """
    KhivaLibrary().c_khiva_library.mean_norm_in_place(ctypes.pointer(tss.arr_reference))


def znorm(tss, epsilon=0.00000001):
    """ Calculates a new set of time series with zero mean and standard deviation one.

    :param tss: KHIVA array with the time series.
    :param epsilon: Minimum standard deviation to consider. It acts as a gatekeeper for those time series that
           may be constant or near constant.

    :return: KHIVA array with the same dimensions as tss where the time series have been adjusted for zero mean and
            one as standard deviation.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.znorm(ctypes.pointer(tss.arr_reference), ctypes.pointer(ctypes.c_double(epsilon)),
                                         ctypes.pointer(b))

    return Array(array_reference=b)


def znorm_in_place(tss, epsilon=0.00000001):
    """ Adjusts the time series in the given input and performs z-norm
    in place (without allocating further memory).

    :param tss: KHIVA array with the time series.
    :param epsilon: epsilon Minimum standard deviation to consider. It acts as a gatekeeper for
                    those time series that may be constant or near constant.
    """
    KhivaLibrary().c_khiva_library.znorm_in_place(ctypes.pointer(tss.arr_reference),
                                                  ctypes.pointer(ctypes.c_double(epsilon)))
