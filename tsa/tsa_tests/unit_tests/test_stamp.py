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
import pytest



from tsa.tsa_algorithms.stamp import stamp
import tsa.tsa_datasets as a
########################################################################################################################
"""
data = pd.read_csv(os.path.join(a.__path__[0], 'random_dataset_1000'), sep=',', header=None)
label = data.pop(data.columns[0])

ta = (data[label == 0].iloc[[0]].values.flatten())
tb = (data[label == 1].iloc[[0]].values.flatten())
mp = stamp(ta,tb,20)

def func(x):
    return x + 1

def test_answer():
    assert func(4) == 5
def test_answer2():
    with pytest.raises(SystemExit):
        assert f()
def f():
    raise SystemExit(1)

"""