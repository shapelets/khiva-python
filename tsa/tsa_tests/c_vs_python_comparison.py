"""
Copyright (c) 2018 Grumpy Cat Software S.L.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
########################################################################################################################
# IMPORTS
########################################################################################################################
import ctypes
import tsa.tsa_libraries
import os
import time
c_performance_checker = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libc_performance.dylib'))
start = time.time()
c_performance_checker.c_performance(ctypes.pointer(ctypes.c_int(1000)))
print(time.time() -start)