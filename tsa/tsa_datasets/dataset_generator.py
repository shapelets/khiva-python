"""
Copyright (c) 2018 Grumpy Cat Software S.L.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
########################################################################################################################
# IMPORT
########################################################################################################################
import random
import os

import tsa.tsa_datasets as a

########################################################################################################################

def random_dataset_generator(name,points):
    """
    Generates a dataset of the desired number of points with a desired name indicated when calling the function.
    The dataset is composed by random doubles between 0 and 1.
    :param name: Name of the dataset
    :param points: NUmber of points of the dataset.
    """
    file = open(os.path.join(a.__path__[0], name), 'w')
    file.write("0,")
    for i in range(1,points):
        print("0," + str(i))
        file.write(str(random.uniform(0, 1)))
        file.write(',')
    file.write('1')
    file.write('\n')
    file.write("1,")
    for i in range(1,points):
        print("1," + str(i))
        file.write(str(random.uniform(0, 1)))
        file.write(',')
    file.write('1')

def section_defined_dataset_generator(name, points):
    """
    Generates a dataset of the desired number of points with a desired name indicated when calling the function.
    The dataset is composed by random doubles between 0 and 1 with a section in common to the two time series.

    :param name: Name of the dataset.
    :param points: NUmber of points of the dataset. :
    """
    file = open(os.path.join(a.__path__[0], name), 'w')
    file.write("0,")
    for i in range(1,points):
        if (i>500 and i < 700):
            print("0," + str(i))
            file.write(str(0.9))
            file.write(',')
        else:
            print("0," + str(i))
            file.write(str(random.uniform(0, 1)))
            file.write(',')
    file.write('1')
    file.write('\n')
    file.write("1,")
    for i in range(1,points):
        if (i>200 and i<400):
            print("1," + str(i))
            file.write(str(0.9))
            file.write(',')
        else:
            print("1," + str(i))
            file.write(str(random.uniform(0, 1)))
            file.write(',')
    file.write('1')