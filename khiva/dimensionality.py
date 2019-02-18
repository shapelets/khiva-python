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


def paa(a, bins):
    """ Piecewise Aggregate Approximation (PAA) approximates a time series :math:`X` of length :math:`n` into vector
    :math:`\\bar{X}=(\\bar{x}_{1},…,\\bar{x}_{M})` of any arbitrary length :math:`M \\leq n` where each of
    :math:`\\bar{x_{i}}` is calculated as follows:

    .. math::
        \\bar{x}_{i} = \\frac{M}{n} \\sum_{j=n/M(i-1)+1}^{(n/M)i} x_{j}.

    Which simply means that in order to reduce the dimensionality from :math:`n` to :math:`M`, we first divide the original
    time series into :math:`M` equally sized frames and secondly compute the mean values for each frame. The sequence
    assembled from the mean values is the PAA approximation (i.e., transform) of the original time series.

    :param a: Set of points.
    :param bins: Sets the total number of divisions.

    :return: KHIVA array of points with the reduced dimensionality.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.paa(ctypes.pointer(a.arr_reference), ctypes.pointer(ctypes.c_int(bins)),
                                       ctypes.pointer(b))

    return Array(array_reference=b)


def pip(a, number_ips):
    """ Calculates the number of Perceptually Important Points (PIP) in the time series.

    [1] Fu TC, Chung FL, Luk R, and Ng CM. Representing financial time series based on data point importance.
    Engineering Applications of Artificial Intelligence, 21(2):277-300, 2008.

    :param a: KHIVA array whose dimension zero is the length of the time series.
    :param number_ips: The number of points to be returned.

    :return: KHIVA array with the most Perceptually Important number_ips.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.pip(ctypes.pointer(a.arr_reference), ctypes.pointer(ctypes.c_int(number_ips)),
                                       ctypes.pointer(b))

    return Array(array_reference=b)


def pla_bottom_up(ts, max_error):
    """
    Applies the Piecewise Linear Approximation (PLA BottomUP) to the time series.

    [1] Zhu Y, Wu D, Li Sh (2007). A Piecewise Linear Representation Method of Time Series Based on Feature Points.
    Knowledge-Based Intelligent Information and Engineering Systems 4693:1066-1072.

    :param ts: Expects a khiva array containing the set of points to be reduced. The first component of the points in
                the first column and the second component of the points in the second column.
    :param max_error: The maximum approximation error allowed.
    :return: The reduced number of points.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.pla_bottom_up(ctypes.pointer(ts.arr_reference),
                                                 ctypes.pointer(ctypes.c_float(max_error)),
                                                 ctypes.pointer(b))

    return Array(array_reference=b)


def pla_sliding_window(ts, max_error):
    """
    Applies the Piecewise Linear Approximation (PLA Sliding Window) to the time series.

    [1] Zhu Y, Wu D, Li Sh (2007). A Piecewise Linear Representation Method of Time Series Based on Feature Points.
    Knowledge-Based Intelligent Information and Engineering Systems 4693:1066-1072.

    :param ts: Expects a khiva array containing the set of points to be reduced. The first component of the points in
                the first column and the second component of the points in the second column.
    :param max_error: The maximum approximation error allowed.
    :return: The reduced number of points.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.pla_sliding_window(ctypes.pointer(ts.arr_reference),
                                                      ctypes.pointer(ctypes.c_float(max_error)),
                                                      ctypes.pointer(b))

    return Array(array_reference=b)


def ramer_douglas_peucker(a, epsilon):
    """ The Ramer–Douglas–Peucker algorithm (RDP) is an algorithm for reducing the number of points in a curve that is
    approximated by a series of points. It reduces a set of points depending on the perpendicular distance of the points
    and epsilon, the greater epsilon, more points are deleted.

    [1] Urs Ramer, "An iterative procedure for the polygonal approximation of plane curves", Computer Graphics and Image
    Processing, 1(3), 244–256 (1972) doi:10.1016/S0146-664X(72)80017-0.

    [2] David Douglas & Thomas Peucker, "Algorithms for the reduction of the number of points required to represent a
    digitized line or its caricature", The Canadian Cartographer 10(2), 112–122 (1973) doi:10.3138/FM57-6770-U75U-7727

    :param a: KHIVA array with the x-coordinates and y-coordinates of the input points (x in column 0 and y in column 1).
    :param epsilon: It acts as the threshold value to decide which points should be considered meaningful or not.

    :return: KHIVA array with the x-coordinates and y-coordinates of the selected points (x in column 0 and y in
            column 1).
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.ramer_douglas_peucker(ctypes.pointer(a.arr_reference),
                                                         ctypes.pointer(ctypes.c_double(epsilon)),
                                                         ctypes.pointer(b))

    return Array(array_reference=b)


def sax(a, alphabet_size):
    """ Symbolic Aggregate approXimation (SAX). It transforms a numeric time series into a time series of symbols with
    the same size. The algorithm was proposed by Lin et al.) and extends the PAA-based approach inheriting the original
    algorithm simplicity and low computational complexity while providing satisfactory sensitivity and selectivity in
    range query processing. Moreover, the use of a symbolic representation opened a door to the existing wealth of
    data-structures and string-manipulation algorithms in computer science such as hashing, regular expression, pattern
    matching, suffix trees, and grammatical inference.

    [1] Lin, J., Keogh, E., Lonardi, S. & Chiu, B. (2003) A Symbolic Representation of Time Series, with Implications
    for Streaming Algorithms. In proceedings of the 8th ACM SIGMOD Workshop on Research Issues in Data Mining and
    Knowledge Discovery. San Diego, CA. June 13.

    :param a: KHIVA array with the input time series.
    :param alphabet_size: Number of element within the alphabet.

    :return: KHIVA array of points with the reduced dimensionality.
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.sax(ctypes.pointer(a.arr_reference), ctypes.pointer(ctypes.c_int(alphabet_size)),
                                       ctypes.pointer(b))

    return Array(array_reference=b)


def visvalingam(a, num_points):
    """ Reduces a set of points by applying the Visvalingam method (minimun triangle area) until the number
    of points is reduced to numPoints.

    [1] M. Visvalingam and J. D. Whyatt, Line generalisation by repeated elimination of points,
    The Cartographic Journal, 1993.

    :param a: KHIVA array with the x-coordinates and y-coordinates of the input points (x in column 0 and y in column 1).
    :param num_points: Sets the number of points returned after the execution of the method.

    :return: KHIVA array with the x-coordinates and y-coordinates of the selected points (x in column 0 and y in
            column 1).
    """
    b = ctypes.c_void_p(0)
    KhivaLibrary().c_khiva_library.visvalingam(ctypes.pointer(a.arr_reference),
                                               ctypes.pointer(ctypes.c_int(num_points)),
                                               ctypes.pointer(b))

    return Array(array_reference=b)
