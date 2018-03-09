"""
Copyright (c) 2018 Grumpy Cat Software S.L.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
########################################################################################################################
# IMPORT
########################################################################################################################
from scipy.io import loadmat
import os
import time
import tsa.tsa_datasets as a
from tsa.analyser import analiser
import pandas as pd

########################################################################################################################

# data preprocessing
data = loadmat(os.path.join(a.__path__[0], 'sel102m.mat'))
ta = data["val"][0]
print(ta)
print(len(ta))
analiser_cat = analiser()
for i in range(1):
    print("-----")
    print("stomp")
    print("-----")
    start = time.time()
    # data analysis
    l = []
    l.append(list(ta[0:1000]))
    l.append(list(ta[1000:2000]))
    mp = analiser_cat.stomp(ta[0:1000], ta[1000:2000], 256)
    tp = analiser_cat.find_best_n_motifs(mp['matrix_profile'], mp['index_profile'], 4)
    dp = analiser_cat.find_best_n_discords(mp['matrix_profile'], mp['index_profile'], 4)
    print(analiser_cat.absolute_sum_of_change([[1, 2, 3, 5, 6, 7, 8, 10],
        [4, 5, 6, 24, 24, 24, 3, 3]]))
    print(tp)
    print(dp)
    print(str(time.time() - start))
