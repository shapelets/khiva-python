"""
Copyright (c) 2018 Grumpy Cat Software S.L.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
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

