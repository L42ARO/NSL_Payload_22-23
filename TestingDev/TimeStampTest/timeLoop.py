import time
from datetime import datetime

t_end = time.time() + 30
print(str(t_end) + "\n")
print(str(time.time()) + "\n")
curTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(str(curTime))
while time.time() < t_end:
    curTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(curTime)