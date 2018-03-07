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
from tsa.tsa_algorithms.stomp import stomp
from tsa.tsa_algorithms.stomp_self_join import stomp_self_join
from tsa.tsa_algorithms.binding_test import binding_test
########################################################################################################################


class grumpyAnaliser:
    def __init__(self):
         self._c_tsa_library = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libTSALIB.dylib'))

    def stomp(self,first_time_series_list, second_time_series_list, subsequence_length):
        return stomp(first_time_series_list, second_time_series_list, subsequence_length, self._c_tsa_library)
    def stomp_self_join(self,first_time_series_list, subsequence_length):
        return stomp_self_join(first_time_series_list, subsequence_length, self._c_tsa_library)
    def binding_test(self,first_time_series_list):
        return binding_test(first_time_series_list, self._c_tsa_library)




