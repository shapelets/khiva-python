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

def lls(a, b):
    """ Calculates the minimum norm least squares solution :math:`x` :math:`(||A·x - b||^2)` to :math:`A·x = b`. This
    function uses the singular value decomposition function of Arrayfire. The actual formula that this function computes
    is :math:`x = V·D\\dagger·U^T·b`. Where :math:`U` and :math:`V` are orthogonal matrices and :math:`D\\dagger` contains
    the inverse values of the singular values contained in :math:`D` if they are not zero, and zero otherwise.

    :param a: KHIVA array with the coefficients of the linear equation problem to solve. It accepts a list of lists or
              a numpy array with one or several time series.
    :param b: KHIVA array with the measured values.
    :return: KHIVA array with the solution to the linear equation problem minimizing the norm 2.
    """
    c = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.lls(ctypes.pointer(a.arr_reference), ctypes.pointer(b.arr_reference),
                                       ctypes.pointer(c))

    return Array(array_reference=c)
