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

import tsa.tsa_datasets as a
from tsa.tsa_visualisation import visualisation
from tsa.tsa_algorithms.scrimp import scrimp
from tsa.grumpy import grumpyAnaliser
########################################################################################################################

#data preprocessing
data = loadmat(os.path.join(a.__path__[0], 'sel102m.mat'))
ta=data["val"][0][2500:7500]

#configuration
analiser_cat = grumpyAnaliser()
analiser_cat.set_cpu()


#data analysis
mp = analiser_cat.scrimp(ta,200)
print(mp["matrix_profile"])
#visualisation.plot_stamp(ta,ta,mp["matrix_profile"],mp["index_profile"],200)

analiser_cat.set_opencl()


#data analysis
mp = analiser_cat.scrimp(ta,200)
print(mp["matrix_profile"])