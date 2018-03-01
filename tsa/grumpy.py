#
# title           :grumpy.py
# description     :
# author          :David Cuesta
# company         :Grumpy Cat Software
# date            :
# usage           :
# python_version  :3.6
# ======================================================================================================================
########################################################################################################################
# IMPORT
########################################################################################################################
import ctypes
import os
import tsa.tsa_libraries
from tsa.tsa_algorithms.stamp import stamp
from tsa.tsa_algorithms.stamp_self_join import stamp_self_join
########################################################################################################################


class grumpyAnaliser:
    def __init__(self):
         self._c_tsa_library = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libTSALIB.dylib'))

    def stamp(self,first_time_series_list, second_time_series_list, subsequence_length):
        return stamp(first_time_series_list, second_time_series_list, subsequence_length, self._c_tsa_library)
    def stamp_self_join(self,first_time_series_list, subsequence_length):
        return stamp_self_join(first_time_series_list, subsequence_length, self._c_tsa_library)




