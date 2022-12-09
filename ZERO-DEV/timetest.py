import time

from datetime import datetime

currTime=datetime.now()
print(currTime.strftime("%H:%M:%S"))
time.sleep(3.5)
currTime=datetime.now()
print(currTime.strftime("%H:%M:%S"))
