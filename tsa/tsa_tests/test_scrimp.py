#
# title           :test_scrimp.py
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

from tsa.tsa_algorithms.scrimp import scrimp
import tsa.tsa_datasets as a
from tsa.tsa_visualisation import visualisation
########################################################################################################################

data = pd.read_csv(os.path.join(a.__path__[0], 'random_dataset_1000'), sep=',', header=None)
label = data.pop(data.columns[0])
ta = (data[label == 0].iloc[[0]].values.flatten())
tb = (data[label == 1].iloc[[0]].values.flatten())
mp = scrimp(ta,20,"opencl")
visualisation.plot_stamp(ta,ta,mp["matrix_profile"],mp["index_profile"],20)
