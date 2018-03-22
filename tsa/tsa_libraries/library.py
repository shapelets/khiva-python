"""
Copyright (c) 2018 Grumpy Cat Software S.L.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

########################################################################################################################
# IMPORT
########################################################################################################################
from enum import Enum
import ctypes
import os
import tsa.tsa_libraries
import platform


########################################################################################################################

class TsaLibrary(object):
    class __TsaLibrary:
        def __init__(self):
            if platform.system() == 'Darwin':
                self.c_tsa_library = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libtsa_c.dylib'))
            if platform.system() == 'Windows':
                self.c_tsa_library = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libtsa_c.dll'))
            if platform.system() == 'Linux':
                self.c_tsa_library = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libtsa_c.so'))

    instance = None

    def __new__(cls):
        if not TsaLibrary.instance:
            TsaLibrary.instance = TsaLibrary.__TsaLibrary()
        return TsaLibrary.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class TSABackend(Enum):
    TSA_BACKEND_DEFAULT = 0
    TSA_BACKEND_CPU = 1
    TSA_BACKEND_CUDA = 2
    TSA_BACKEND_OPENCL = 4


def info():
    """
    Get the devices info.
    """
    TsaLibrary().c_tsa_library.info()


def set_backend(backend):
    """
    Set the TSABackend.

    :param backend: The desired backend. TSABackend type.
    """
    TsaLibrary().c_tsa_library.set_backend(ctypes.pointer(ctypes.c_int(backend.value)))


def get_backend():
    """
    Get the active backend.

    :return The active backend. TSABackend type.

    """
    backend = (ctypes.c_int * 1)(*[0])

    TsaLibrary().c_tsa_library.get_backend(ctypes.pointer(backend))

    return TSABackend(backend[0])


def get_backends():
    """
    Get the available backends.

    :return The available backends.
    """
    backends = (ctypes.c_int * 1)(*[0])
    TsaLibrary().c_tsa_library.get_backends(ctypes.pointer(backends))
    return backends[0]


def set_device(device):
    """
    Set the device.

    :param device: The desired device.
    """
    TsaLibrary().c_tsa_library.set_device(ctypes.pointer(ctypes.c_int(device)))


def get_device_id():
    """
    Get the active device.

    :return The active device.
    """
    device = (ctypes.c_int * 1)(*[0])
    TsaLibrary().c_tsa_library.get_device_id(ctypes.pointer(device))
    return device[0]


def get_device_count():
    """
    Get the active device.

    :return The active device.
    """
    device_count = (ctypes.c_int * 1)(*[0])
    TsaLibrary().c_tsa_library.get_device_count(ctypes.pointer(device_count))
    return device_count[0]
