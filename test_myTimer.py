import time
from cameraApp.myTimer import MyTimer

timer = MyTimer()

t = time.time()
for j in range(10):
    print(timer.hp_sleep(0.05), time.time() - t)
