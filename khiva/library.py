#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Shapelets.io
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

KHIVA_ERROR_LENGTH = 256

########################################################################################################################

class KhivaLibrary(object):
    class __KhivaLibrary:
        def __init__(self):
            try:
                if platform.system() == 'Darwin':
                    self.c_khiva_library = ctypes.CDLL('libkhiva_c.dylib')
                elif platform.system() == 'Windows':
                    if sys.version_info.major == 3 and sys.version_info.minor == 8:
                        import os
                        os.add_dll_directory(os.getenv("KHIVA_DLL_DIR", default=r'C:\Program Files\Khiva\v0\lib'))
                    self.c_khiva_library = ctypes.CDLL('khiva_c.dll')
                elif platform.system() == 'Linux':
                    self.c_khiva_library = ctypes.CDLL('libkhiva_c.so')
            except:
                raise Exception("Khiva C++ library is required in order to use the Python Khiva library")

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


def get_backend_info():
    """ Gets information from the current backend.

    :return: A string with information from the current backend.
    """
    info_pointer = ctypes.c_char_p((" " * 1000).encode('utf8'))
    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.backend_info(ctypes.pointer(info_pointer),
                                                ctypes.pointer(error_code),
                                                error_message)

    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))
    return info_pointer.value.decode('utf8')


def set_backend(backend):
    """ Sets the KHIVABackend.

    :param backend: The desired backend. KHIVABackend type.
    """
    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.set_backend(ctypes.pointer(ctypes.c_int(backend.value)),
                                                ctypes.pointer(error_code),
                                                error_message)

    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))


def get_backend():
    """ Gets the active backend.

    :return: The active backend. KHIVABackend type.
    """
    backend = (ctypes.c_int * 1)(*[0])
    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.get_backend(ctypes.pointer(backend),
                                                ctypes.pointer(error_code),
                                                error_message)

    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))

    return KHIVABackend(backend[0])


def get_backends():
    """ Gets the available backends.

    :return: The available backends.
    """
    backends = (ctypes.c_int * 1)(*[0])
    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.get_backends(ctypes.pointer(backends),
                                                ctypes.pointer(error_code),
                                                error_message)

    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))
    return backends[0]


def set_device(device):
    """ Sets the device.

    :param device: The desired device.
    """
    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.set_device(ctypes.pointer(ctypes.c_int(device)),
                                                ctypes.pointer(error_code),
                                                error_message)

    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))


def get_device_id():
    """ Gets the active device.

    :return: The active device.
    """
    device = (ctypes.c_int * 1)(*[0])
    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.get_device_id(ctypes.pointer(device),
                                                ctypes.pointer(error_code),
                                                error_message)

    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))
    return device[0]


def get_device_count():
    """ Gets the devices count.

    :return: The devices count.
    """
    device_count = (ctypes.c_int * 1)(*[0])
    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.get_device_count(ctypes.pointer(device_count),
                                                ctypes.pointer(error_code),
                                                error_message)

    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))
    return device_count[0]


def version():
    """ Returns a string with the current version of the library.

    :return: A string with the current version of the library.
    """
    v = ctypes.c_char_p((" " * 40).encode('utf8'))
    error_code = ctypes.c_int(0)
    error_message = ctypes.create_string_buffer(KHIVA_ERROR_LENGTH)
    KhivaLibrary().c_khiva_library.version(ctypes.pointer(v),
                                                ctypes.pointer(error_code),
                                                error_message)

    if error_code.value != 0:
        raise Exception(str(error_message.value.decode()))

    return v.value.decode('utf8')
