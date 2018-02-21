#
# title           :random_dataset_generator.py
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
import random
import os

import tsa.tsa_datasets as a

########################################################################################################################

def generate_dataset(name,points):
    """

    :param name:
    :param points:
    :return:
    """
    file = open(os.path.join(a.__path__[0], name), 'w')
    file.write("0,")
    for i in range(1,points):
        print("0," + str(i))
        a.write(str(random.uniform(0, 1)))
        a.write(',')
    a.write('1')
    a.write('\n')
    a.write("1,")
    for i in range(1,points):
        print("1," + str(i))
        a.write(str(random.uniform(0, 1)))
        a.write(',')
    a.write('1')
