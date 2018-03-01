import pytest
import pandas as pd
import os
import time
from tsa.tsa_algorithms.stamp import stamp
import tsa.tsa_datasets as a
from tsa.tsa_algorithms.scrimp import scrimp
"""
data = pd.read_csv(os.path.join(a.__path__[0], 'random_dataset_1000'), sep=',', header=None)
label = data.pop(data.columns[0])
ta = (data[label == 0].iloc[[0]].values.flatten())
tb = (data[label == 1].iloc[[0]].values.flatten())


from tsa.grumpy import grumpyAnaliser
########################################################################################################################

analiser_cat = grumpyAnaliser()
@pytest.mark.benchmark(
    group="stamp",
    #min_time=0.1,
    #max_time=0.5,
    min_rounds=5,
    timer=time.time,
    disable_gc=True,
    warmup=True
)

def test_stamp_cpu(benchmark):
    analiser_cat.set_cpu()
    @benchmark
    def result():
        # Code to be measured
        analiser_cat.stamp(ta, tb, 20)

    # Extra code, to verify that the run
    # completed correctly.
    # Note: this code is not measured.

@pytest.mark.benchmark(
    group="scrimp",
    #min_time=0.1,
    #max_time=0.5,
    min_rounds=5,
    timer=time.time,
    disable_gc=True,
    warmup=True,
)
def test_scrimp_cpu(benchmark):
    analiser_cat.set_cpu()
    @benchmark
    def result():
        # Code to be measured
        analiser_cat.scrimp(ta, 20)


@pytest.mark.benchmark(
    group="stamp",
    #min_time=0.1,
    #max_time=0.5,
    min_rounds=5,
    timer=time.time,
    disable_gc=True,
    warmup=True,
)

def test_stamp_gpu(benchmark):
    analiser_cat.set_opencl()
    @benchmark
    def result():
        # Code to be measured
        analiser_cat.stamp(ta, tb, 20)

    # Extra code, to verify that the run
    # completed correctly.
    # Note: this code is not measured.

@pytest.mark.benchmark(
    group="scrimp",
    # min_time=0.1,
    # max_time=0.5,
    min_rounds=5,
    timer=time.time,
    disable_gc=True,
    warmup=True,
)
def test_scrimp_gpu(benchmark):
    analiser_cat.set_opencl()
    @benchmark
    def result():
        # Code to be measured
        analiser_cat.scrimp(ta, 20)
# Extra code, to verify that the run
# completed correctly.
# Note: this code is not measured.



########################################################################################################################



"""