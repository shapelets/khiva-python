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

def lls(a, b):
    """ Calculates the minimum norm least squares solution :math:`x` :math:`(||A·x − b||^2)` to :math:`A·x = b`. This
    function uses the singular value decomposition function of Arrayfire. The actual formula that this function computes
    is :math:`x = V·D\dagger·U^T·b`. Where :math:`U` and :math:`V` are orthogonal matrices and :math:`D\dagger` contains
    the inverse values of the singular values contained in :math:`D` if they are not zero, and zero otherwise.

    :param a: Coefficients of the linear equation problem to solve. It accepts a list of lists or a numpy array
              with one or several time series.
    :param b: List or numpy array with the measured values.`
    :return: Contains the solution to the linear equation problem minimizing the norm 2.
    """
    if isinstance(a, list):
        a = np.array(a)
    a_n = len(a)
    a_l = len(a[0])
    a_c_number_of_ts = ctypes.c_long(a_n)
    a_c_length = ctypes.c_long(a_l)
    a_joint = np.concatenate(a, axis=0)
    a_c_joint = (ctypes.c_double * len(a_joint))(*a_joint)
    if isinstance(b, list):
        b = np.array(b)
    b_l = len(b)
    b_c_length = ctypes.c_long(b_l)
    b_c = (ctypes.c_double * len(b))(*b)

    result_initialized = np.zeros(a_n).astype(np.double)
    result_c_initialized = (ctypes.c_double * a_n)(*result_initialized)
    TsaLibrary().c_tsa_library.lls(ctypes.pointer(a_c_joint), ctypes.pointer(a_c_length),
                                   ctypes.pointer(a_c_number_of_ts), ctypes.pointer(b_c),
                                   ctypes.pointer(b_c_length), ctypes.pointer(result_c_initialized))

    return np.array(result_c_initialized)
