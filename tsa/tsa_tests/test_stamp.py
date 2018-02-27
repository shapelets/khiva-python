#
# title           :test_stamp.py
# description     :
# author          :David Cuesta
# company         :Grumpy Cat Software
# date            :
# usage           :
# python_version  :3.6
# ==============================================================================
########################################################################################################################
# IMPORT
########################################################################################################################
import pandas as pd
import os
import time
import ctypes
import numpy as np
import os
import tsa.tsa_libraries
from tsa.tsa_algorithms.stamp import stamp
import tsa.tsa_datasets as a
from tsa.grumpy import grumpyAnaliser
########################################################################################################################
data = pd.read_csv(os.path.join(a.__path__[0], 'random_dataset_1000'), sep=',', header=None)
label = data.pop(data.columns[0])
c_tsa_library = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libmylib-unified.dylib'))

ta = (data[label == 0].iloc[[0]].values.flatten())
tb = (data[label == 1].iloc[[0]].values.flatten())

start = time.time()
c_tsa_library.set_cpu()

mp = stamp(ta,tb,20,c_tsa_library)
data = pd.read_csv(os.path.join(a.__path__[0], 'random_dataset_1000'), sep=',', header=None)
label = data.pop(data.columns[0])
t1 = (data[label == 0].iloc[[0]].values.flatten())
t2 = (data[label == 1].iloc[[0]].values.flatten())
c_tsa_library1 = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libmylib-unified.dylib'))

c_tsa_library1.set_gpu()
mp = stamp(ta,tb,20,c_tsa_library1)
