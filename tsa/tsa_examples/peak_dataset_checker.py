#
# title           :peak_dataset_checker.py
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
import os
import tsa.tsa_datasets as a
from tsa.grumpy import grumpyAnaliser
import pandas as pd

########################################################################################################################

data = pd.read_csv(os.path.join(a.__path__[0], 'peak_dataset_1000'), sep=',', header=None)
label = data.pop(data.columns[0])

ta = (data[label == 0].iloc[[0]].values.flatten())
tb = (data[label == 1].iloc[[0]].values.flatten())
tc = []
for a in range(0,220):
    tc.append(0.5)
print(len(tc))
for a in range(0,300):
    tc.append(1)
    tc.append(0)
g_cat_analiser = grumpyAnaliser();

a= g_cat_analiser.stomp_self_join(ta,200)
print(a)

