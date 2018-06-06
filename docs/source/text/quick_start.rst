.. _quick-start-label:

Quick Start
===========


Install tsa
---------------

First of all, the TSA C++ library should be installed by using the installer that we offer in wwww.shapelets.io

Then, the compiled TSA package is hosted on the Python Package Index (PyPI) so it can be installed with pip:

.. code:: shell

   pip3 install tsa


Dive in
-------

In order to quickly dive into tsa, you can follow the following example:

First step, consists in setting what backend and device you want to use (there is a backend and a device set by default):

.. code-block:: python

    from tsa.library import *
    set_backend(TSABackend.TSA_BACKEND_OPENCL)
    set_device(0)

After that, we can create an array in the device:

.. code-block:: python

    from tsa.array import *
    a = array([1, 2, 3, 4, 5, 6, 7, 8])
    a.print()

The lines contained above print the dimensions and the content of the created array:

+-----------+
| [8 1 1 1] |
+===========+
|1.0000     |
+-----------+
|2.0000     |
+-----------+
|3.0000     |
+-----------+
|4.0000     |
+-----------+
|5.0000     |
+-----------+
|6.0000     |
+-----------+
|7.0000     |
+-----------+
|8.0000     |
+-----------+

We have to know that this array is created on the device and now we can concatenate operations applied to this array in
an asynchronous way and we will only receive the data in the host when 'to_list()', 'to_numpy()' or 'to_pandas()' (this
one only supports bi-dimensional time series) functions are called.

.. code-block:: python

    a = a.to_pandas()
    print(a)

The result is the next one:

+-+-------+
| | 0     |
+=+=======+
|1|1.0    |
+-+-------+
|2|2.00   |
+-+-------+
|3|3.00   |
+-+-------+
|4|4.00   |
+-+-------+
|5|5.00   |
+-+-------+
|6|6.00   |
+-+-------+
|7|7.00   |
+-+-------+
|8|8.00   |
+-+-------+

Now let's dive into the asynchronous usage of the library.

TSA's library provide us several time series analysis functionalities which include features extaction, time-series
re-dimension, distance calculations, motifs and discords detection, tools for similarity study, statistical parameters
extraction or time series normalization.

All of these functionalities can be concatenated in order to improve the performance, getting the data just in the
moment that you will not use functions of this library:

.. code-block:: python

    from tsa.matrix import *
    stomp_result = stomp(array(np.array([11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11])),
                             array(np.array([9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9])),
                             3)
    find_best_n_discords_result = find_best_n_discords(stomp_result[0],
                                                           stomp_result[1], 2)
    a = find_best_n_discords_result[2].to_numpy()
    print(a)

The previous produces the following output:

+-------------------------------------+
| [1.73190141 1.73185158] [8 8] [0 9] |
+-------------------------------------+

The first numpy array represents the minimum distances between the subsequences of length 3 between the two time series.
The second numpy array represents the location of those subsequences in the first time series and the
third one represents the indices in the second time series.

Another interesting thing that we want to demonstrate in this introductory section is the possibility of using the library
for computing the functions in different backends and with different devices, knowing that the operations should be executed
in the same device where the array was created.

.. code-block:: python

    #Adding operations in the different backends and devices.
    from tsa.features import *
    set_backend(TSABackend.TSA_BACKEND_OPENCL)
    set_device(0)
    a = array([1, 2, 3, 4, 5, 6, 7, 8])
    b = mean(a)

    set_device(1)
    c = array([1, 2, 3, 4, 5, 6, 7, 8])
    d = mean(c)

    set_backend(TSABackend.TSA_BACKEND_CPU)
    set_device(0)
    e = array([1, 2, 3, 4, 5, 6, 7, 8])
    f = mean(e)

    #Retrieving the results of the previous operations
    set_backend(TSABackend.TSA_BACKEND_OPENCL)
    set_device(0)
    print(b.to_numpy())

    set_device(1)
    print(d.to_numpy())

    set_backend(TSABackend.TSA_BACKEND_CPU)
    set_device(0)
    print(f.to_numpy())


The output is the next one:

+-----+
| 4.5 |
+-----+
| 4.5 |
+-----+
| 4.5 |
+-----+

Another important fact is that, by default, the data type used is floating point of 32
bits in order to not have problems with the different devices, but it can be changed deliberately.

The available data types are the next ones:

+-----------+----------------------+
| Data type |  Explanation         |
+===========+======================+
| f32       | 32 bits Float        |
+-----------+----------------------+
| c32       | 32 bits Complex      |
+-----------+----------------------+
| f64       | 64 bits Double       |
+-----------+----------------------+
| c64       | 64 bits Complex      |
+-----------+----------------------+
| b8        | 8 bits Boolean       |
+-----------+----------------------+
| s32       | 32 bits Int          |
+-----------+----------------------+
| 32u       | 32 bits Unsigned Int |
+-----------+----------------------+
| u8        | 8 bits Unsigned Int  |
+-----------+----------------------+
| s64       | 64 bits Integer      |
+-----------+----------------------+
| u64       | 64 bits Unsigned Int |
+-----------+----------------------+
| s16       | 16 bits Int          |
+-----------+----------------------+
| u16       | 16 bits Unsigned Int |
+-----------+----------------------+


There are functions that do not support 32 bits floating point data type, so it is necessary to indicate the data type.
The following is an example function requiring a 32bit signed integer array:

.. code:: python

    cwt_coefficients_result = cwt_coefficients(array([[0.1, 0.2, 0.3], [0.1, 0.2, 0.3]]),
                                                array(data=[1, 2, 3], tsa_type=dtype.s32), 2, 2).to_numpy()
    print(cwt_coefficients_result)

The output is:

+-------------------------+
| [0.26517162 0.26517162] |
+-------------------------+


Limitations
-----------

This open-source library provides a very good performance but it has got memory limitations.
For cases where you need to apply a time series analysis over a huge amount of data and in short-term fashion, please,
contact us. We are working on a cluster version which is coming soon.


Let's Rock!
-----------
Now, you have the basic concepts to start using the library. Please, follow the documentation of each function in order to
know how to use them.
Each function has its corresponding test(s). You can check there how to use the function.

Furthermore, we provide use cases and examples that you can use to learn where and how to apply the library.



