"""
Copyright (c) 2018 Grumpy Cat Software S.L.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

########################################################################################################################
# IMPORT
########################################################################################################################
import ctypes
import os
import tsa.tsa_libraries


########################################################################################################################

class tsaLibrary(object):
    class __tsaLibrary:
        def __init__(self):
            self.c_tsa_library = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libTSALIB.dylib'))

    instance = None

    def __new__(cls):
        if not tsaLibrary.instance:
            tsaLibrary.instance = tsaLibrary.__tsaLibrary()
        return tsaLibrary.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


def info():
    """
    Get the devices info.
    """
    tsaLibrary().c_tsa_library.info()


def set_device(device):
    """
    Set the device.

    :param device: The desired device.
    """
    tsaLibrary().c_tsa_library.set_device(ctypes.pointer(ctypes.c_int(device)))


def set_backend(backend):
    """
    Set the back-end.

    :param backend: The desired back-end.
    """
    tsaLibrary().c_tsa_library.set_backend(ctypes.pointer(ctypes.c_int(backend)))
