import win32api
import time

num = 60

t = time.time()
for j in range(num):
    _t = time.time()
    time.sleep(0.001)
    print(j, time.time() - _t, time.time() - t)

print((time.time() - t) / num)

t = time.time()
for j in range(num):
    _t = time.time()
    win32api.Sleep(1)
    print(j, time.time() - _t, time.time() - t)

print((time.time() - t) / num)
