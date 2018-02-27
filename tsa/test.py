from scipy.io import loadmat
import os
import ctypes
import tsa.tsa_datasets as a
from tsa.tsa_visualisation import visualisation
from tsa.tsa_algorithms.scrimp import scrimp
from tsa.grumpy import grumpyAnaliser
import tsa
import pandas as pd
import numpy as np
########################################################################################################################

#data preprocessing

data = pd.read_csv(os.path.join(a.__path__[0], 'random_dataset_1000'), sep=',', header=None)
label = data.pop(data.columns[0])

ta = (data[label == 0].iloc[[0]].values.flatten())
tb = (data[label == 1].iloc[[0]].values.flatten())

label = data.pop(data.columns[0])
first_time_series_list= [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]
second_time_series_list = [5,6,7,8,9,10,11,12,13,14,5,6,7,8,9,10,11,12,13,14]



##double array in c of time series
first_time_series_double_array = (ctypes.c_double * len(first_time_series_list))(*first_time_series_list)
second_time_series_double_array = (ctypes.c_double * len(second_time_series_list))(*second_time_series_list)

##double array of zeros
initialized_mp_numpy_array = np.zeros(len(first_time_series_list) - 5)
initialized_ip_numpy_array = np.zeros(len(second_time_series_list) - 5)
zeros_time_series_double_array = (ctypes.c_double * len(initialized_mp_numpy_array))(*initialized_mp_numpy_array)
zeros_second_time_series_double_array = (ctypes.c_int * len(initialized_ip_numpy_array))(*initialized_ip_numpy_array.astype(int))

#configuration
analiser_cat = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libmylib-unified.dylib'))
a = ctypes.c_int(2)
analiser_cat.stamp(ctypes.pointer(first_time_series_double_array),ctypes.pointer(second_time_series_double_array),
                   ctypes.pointer(ctypes.c_long(5)),ctypes.pointer(ctypes.c_int(len(first_time_series_list))),
                   ctypes.pointer(zeros_time_series_double_array),ctypes.pointer(zeros_second_time_series_double_array))
m=(ctypes.c_long(0))
analiser_cat.test_int(ctypes.pointer(ctypes.c_long(1)),ctypes.pointer(m ))
print(m)
