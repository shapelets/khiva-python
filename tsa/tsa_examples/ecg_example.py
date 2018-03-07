#
# title           :ecg_example.py
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
from scipy.io import loadmat
import os
import time
import tsa.tsa_datasets as a
from tsa.grumpy import grumpyAnaliser
import pandas as pd
########################################################################################################################

#data preprocessing
data = loadmat(os.path.join(a.__path__[0], 'sel102m.mat'))
ta=data["val"][0]
print(ta)
print(len(ta))


analiser_cat = grumpyAnaliser()
for i in range(10):
    print("-----")
    print("stomp")
    print("-----")
    start = time.time()
    #data analysis
    mp = analiser_cat.stomp(ta[0:13000],ta[0:13000],256)
    print(str(time.time() -start))

