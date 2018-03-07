import ctypes
import tsa.tsa_libraries
import os
import time
c_performance_checker = ctypes.CDLL(os.path.join(tsa.tsa_libraries.__path__[0], 'libc_performance.dylib'))
start = time.time()
c_performance_checker.c_performance(ctypes.pointer(ctypes.c_int(1000)))
print(time.time() -start)