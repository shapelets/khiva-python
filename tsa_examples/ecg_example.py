# Copyright (c) 2018 Grumpy Cat Software S.L.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

########################################################################################################################
# IMPORT
########################################################################################################################
from scipy.io import loadmat
import os
import tsa_datasets as a
from tsa.algorithms.matrix import stomp_self_join

########################################################################################################################

data = loadmat(os.path.join(a.__path__[0], 'sel102m.mat'))
ta = data["val"][0]

mp = stomp_self_join(ta[0:1000], 256)
print(mp)