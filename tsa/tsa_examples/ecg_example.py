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
########################################################################################################################


data = loadmat(os.path.join(a.__path__[0], 'sel102m.mat'))
ta=data["val"][0]
mp = scrimp(ta,3000)
visualisation.motif(ta,mp["matrix_profile"],mp["index_profile"])
