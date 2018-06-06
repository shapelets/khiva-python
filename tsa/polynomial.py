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
from tsa.array import Array


########################################################################################################################

def polyfit(x, y, deg):
    """ Least squares polynomial fit. Fit a polynomial :math:`p(x) = p[0] * x^{deg} + ... + p[deg]` of degree
    :math:`deg` to points :math:`(x, y)`. Returns a vector of coefficients :math:`p` that minimises the squared error.

    :param x: TSA array with the x-coordinates of the M sample points :math:`(x[i], y[i])`.
    :param y: TSA array with the y-coordinates of the sample points.
    :param deg: Degree of the fitting polynomial

    :return: TSA array with the polynomial coefficients, highest power first.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.polyfit(ctypes.pointer(x.arr_reference), ctypes.pointer(y.arr_reference),
                                       ctypes.pointer(ctypes.c_int(deg)),
                                       ctypes.pointer(b))

    return Array(array_reference=b)


def roots(p):
    """ Calculates the roots of a polynomial with coefficients given in :math:`p`. The values in the rank-1 array
    :math:`p` are coefficients of a polynomial. If the length of :math:`p` is :math:`n+1` then the polynomial is
    described by:

    .. math::
        p[0] * x^n + p[1] * x^{n-1} + ... + p[n-1] * x + p[n]

    :param p: TSA array with the polynomial coefficients.

    :return: TSA array with the roots of the polynomial.
    """
    b = ctypes.c_void_p(0)
    TsaLibrary().c_tsa_library.roots(ctypes.pointer(p.arr_reference), ctypes.pointer(b))

    return Array(array_reference=b)
