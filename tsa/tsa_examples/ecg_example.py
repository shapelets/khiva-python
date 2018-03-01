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
########################################################################################################################

#data preprocessing
data = loadmat(os.path.join(a.__path__[0], 'sel102m.mat'))
ta=data["val"][0]
print(len(ta))
#configuration
analiser_cat = grumpyAnaliser()
print("1000")
start = time.time()
#data analysis
mp = analiser_cat.stamp(ta[0:1000],ta[0:1000],200)
print(str(time.time() -start))

print("5000")
start = time.time()
#data analysis
mp = analiser_cat.stamp(ta[0:5000],ta[0:5000],200)
print(str(time.time() -start))

print("10000")
start = time.time()
#data analysis
mp = analiser_cat.stamp(ta[0:10000],ta[0:10000],200)
print(str(time.time() -start))

print("20000")
start = time.time()
#data analysis
mp = analiser_cat.stamp(ta[0:20000],ta[0:20000],200)
print(str(time.time() -start))

print("50000")
start = time.time()
#data analysis
mp = analiser_cat.stamp(ta[0:50000],ta[0:50000],200)
print(str(time.time() -start))

print("100000")
start = time.time()
#data analysis
mp = analiser_cat.stamp(ta[0:100000],ta[0:100000],200)
print(str(time.time() -start))


print("225000")
start = time.time()
#data analysis
mp = analiser_cat.stamp(ta,ta,200)
print(str(time.time() -start))
