# Copyright (c) 2018 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


########################################################################################################################
# IMPORT
########################################################################################################################
from enum import Enum
import ctypes
import platform
import logging
import sys


########################################################################################################################

class KhivaLibrary(object):
    class __KhivaLibrary:
        def __init__(self):
            try:
                if platform.system() == 'Darwin':
                    self.c_khiva_library = ctypes.CDLL('libkhiva_c.dylib')
                elif platform.system() == 'Windows':
                    self.c_khiva_library = ctypes.CDLL('C:/Program Files/Khiva/v0/lib/khiva_c.dll')
                elif platform.system() == 'Linux':
                    self.c_khiva_library = ctypes.CDLL('libkhiva_c.so')
            except:
                logging.error(
                    "Khiva C++ library is needed to be installed in order to use the Python Khiva library")
                sys.exit(1)

    instance = None

    def __new__(cls):
        if not KhivaLibrary.instance:
            KhivaLibrary.instance = KhivaLibrary.__KhivaLibrary()
        return KhivaLibrary.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class KHIVABackend(Enum):
    """
    KHIVA Backend.
    """
    KHIVA_BACKEND_DEFAULT = 0
    """
    Default Backend.
    """
    KHIVA_BACKEND_CPU = 1
    """
    CPU Backend.
    """
    KHIVA_BACKEND_CUDA = 2
    """
    CUDA Backend.
    """
    KHIVA_BACKEND_OPENCL = 4
    """
    OPENCL Backend.
    """


def info():
    """ Get the devices info.
    """
    KhivaLibrary().c_khiva_library.info()


def set_backend(backend):
    """ Set the KHIVABackend.

    :param backend: The desired backend. KHIVABackend type.
    """
    KhivaLibrary().c_khiva_library.set_backend(ctypes.pointer(ctypes.c_int(backend.value)))


def get_backend():
    """ Get the active backend.

    :return: The active backend. KHIVABackend type.
    """
    backend = (ctypes.c_int * 1)(*[0])
    KhivaLibrary().c_khiva_library.get_backend(ctypes.pointer(backend))

    return KHIVABackend(backend[0])


def get_backends():
    """ Get the available backends.

    :return: The available backends.
    """
    backends = (ctypes.c_int * 1)(*[0])
    KhivaLibrary().c_khiva_library.get_backends(ctypes.pointer(backends))
    return backends[0]


def set_device(device):
    """ Set the device.

    :param device: The desired device.
    """
    KhivaLibrary().c_khiva_library.set_device(ctypes.pointer(ctypes.c_int(device)))


def get_device_id():
    """ Get the active device.

    :return: The active device.
    """
    device = (ctypes.c_int * 1)(*[0])
    KhivaLibrary().c_khiva_library.get_device_id(ctypes.pointer(device))
    return device[0]


def get_device_count():
    """ Get the devices count.

    :return: The devices count.
    """
    device_count = (ctypes.c_int * 1)(*[0])
    KhivaLibrary().c_khiva_library.get_device_count(ctypes.pointer(device_count))
    return device_count[0]


def version():
    """ Returns a string with the current version of the library.

    :return: A string with the current version of the library.
    """
    v = ctypes.c_char_p((" " * 40).encode('utf8'))
    KhivaLibrary().c_khiva_library.version(ctypes.pointer(v))
    return v.value.decode('utf8')
