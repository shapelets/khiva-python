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
from khiva.library import KhivaLibrary
from khiva.array import Array


########################################################################################################################


def linear(xss, yss):
    """Calculates a linear least-squares regression for two sets of measurements. Both arrays should have the same
    length.

    :param xss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series.
    :param yss: Expects an input array whose dimension zero is the length of the time series (all the same) and dimension
                one indicates the number of time series.

    :return: slope Slope of the regression line.
            intercept Intercept of the regression line.
            rvalue Correlation coefficient.
            pvalue Two-sided p-value for a hypothesis test whose null hypothesis is that the slope is zero, using Wald
            Test with t-distribution of the test statistic.
            stderrest Standard error of the estimated gradient.
    """
    b = ctypes.c_void_p(0)
    c = ctypes.c_void_p(0)
    d = ctypes.c_void_p(0)
    e = ctypes.c_void_p(0)
    f = ctypes.c_void_p(0)

    KhivaLibrary().c_khiva_library.linear(ctypes.pointer(xss.arr_reference),
                                          ctypes.pointer(yss.arr_reference),
                                          ctypes.pointer(b),
                                          ctypes.pointer(c),
                                          ctypes.pointer(d),
                                          ctypes.pointer(e),
                                          ctypes.pointer(f)
                                          )
    return Array(array_reference=b), Array(array_reference=c), Array(array_reference=d), Array(
        array_reference=e), Array(array_reference=f)
