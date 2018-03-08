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
import os
import tsa.tsa_libraries
from tsa.tsa_algorithms.stomp import _stomp
from tsa.tsa_algorithms.stomp_self_join import _stomp_self_join
from tsa.tsa_algorithms.binding_test import binding_test
from tsa.tsa_algorithms.find_best_n_motifs import _find_best_n_motifs
from tsa.tsa_algorithms.find_best_n_discords import _find_best_n_discords


########################################################################################################################


class analiser:

    def __init__(self):
        self._c_tsa_library = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libTSALIB.dylib'))

    def stomp(self, first_time_series_list, second_time_series_list, subsequence_length):
        """

        Stomp algorithm to calculate the matrix profile between two time series using a subsequence_length.

        :param first_time_series_list: list of doubles representing the first time series.
        :param second_time_series_list: list of doubles representing the second time series.
        :param subsequence_length: Subsequence length.
        :return:  Dict with the Matrix Profile.
        """
        return _stomp(first_time_series_list, second_time_series_list, subsequence_length, self._c_tsa_library)

    def stomp_self_join(self, first_time_series_list, subsequence_length):
        """

        Stomp algorithm to calculate the matrix profile between two time series using a subsequence_length.


        :param first_time_series_list: list of doubles representing the time series.
        :param subsequence_length: Subsequence length.
        :return: Dict with the Matrix Profile.
        """
        return _stomp_self_join(first_time_series_list, subsequence_length, self._c_tsa_library)

    def find_best_n_motifs(self, profile_list, index_list, n):
        """

        This function extracts the best N motifs from a previously calculated matrix profile

        :param profile_list: The matrix profile containing the minimum distance of each subsequence
        :param index_list: The matrix profile index containing where each minimum occurs
        :param n: Number of motifs to extract
        :return: Dict with the motif distances, motif indices and indices in the other sequence.
        """
        return _find_best_n_motifs(profile_list, index_list, n, self._c_tsa_library)

    def find_best_n_discords(self, profile_list, index_list, n):
        """

        This function extracts the best N discords from a previously calculated matrix profile

        :param profile_list: The matrix profile containing the minimum distance of each subsequence
        :param index_list: The matrix profile index containing where each minimum occurs
        :param n: Number of discords to extract
        :return: Dict with the discord distances, discord indices and indices in the other sequence.
        """
        return _find_best_n_discords(profile_list, index_list, n, self._c_tsa_library)

    def binding_test(self, first_time_series_list):
        """

        :param first_time_series_list:
        :return: Dict with the distance, indices and indices in the other sequence.
        """
        return binding_test(first_time_series_list, self._c_tsa_library)
