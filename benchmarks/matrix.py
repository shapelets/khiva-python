
import scipy.io
import matplotlib.pyplot as plt
import khiva as kv
import os
import time

print(kv.get_backend())
os.chdir("/Users/antonio.vilches/repositories/khiva-python/benchmarks")

print(os.getcwd())


mat = scipy.io.loadmat('./sel102m.mat')
plt.plot(range(len(mat['val'][1])), mat['val'][1])
plt.show()

start = time.time()

l = 400
lecg = len(mat['val'][1])
min = 50000
max = 60000

b = mat['val'][1][min:max]
a = kv.Array(b)
a2 = kv.Array(b)
profile, index = kv.stomp(a, a2, l)
distance, index, subsequence = kv.find_best_n_discords(profile, index, l, 1)

plt.plot(
    range(len(mat['val'][1])),
    mat['val'][1]
)
plt.plot(
    range(len(mat['val'][1]))[int(min + subsequence.to_list()):int(min + subsequence.to_list() + l)],
    mat['val'][1][int(min + subsequence.to_list()):int(min + subsequence.to_list() + l)]
)

plt.show()

end = time.time()
print("Execution time: " + str(end - start))
