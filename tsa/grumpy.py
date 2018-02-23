import pandas as pd
import os
import time
import ctypes
import numpy as np
import os
import tsa.tsa_libraries
from tsa.tsa_algorithms.stamp import stamp
from tsa.tsa_algorithms.scrimp import scrimp
from tsa.tsa_algorithms.stampi import stampi

import tsa.tsa_datasets as a


class grumpyAnaliser:
    def __init__(self):
         self._c_tsa_library = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libmylib-unified.dylib'))

    def stamp(self,first_time_series_list, second_time_series_list, subsequence_length):
        return stamp(first_time_series_list, second_time_series_list, subsequence_length, self._c_tsa_library)

    def scrimp(self, time_series_list, subsequence_lenght):
        return scrimp(time_series_list, subsequence_lenght, self._c_tsa_library)

    def stampi(self,first_time_series_list, new_double_point, old_profile_list, old_index_list, subsequence_length):
        return stampi(first_time_series_list, new_double_point, old_profile_list, old_index_list,
                      subsequence_length,self._c_tsa_library)

    def set_cpu(self):
        self._c_tsa_library.set_backend(ctypes.c_int(0))
    def set_opencl(self):
        self._c_tsa_library.set_backend(ctypes.c_int(1))
    def set_cuda(self):
        self._c_tsa_library.set_backend(ctypes.c_int(2))
    def set_devices(self, device=0):
        self._c_tsa_library.set_device(ctypes.c_int(device))
    def get_info(self):
        self._c_tsa_library.get_info()


