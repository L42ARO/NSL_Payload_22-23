import RPi.GPIO as io
import time
try:
    resetPin = 17
    io.setmode(io.BCM)
    io.setup(resetPin, io.OUT)
    io.output(resetPin, True)
except Exception as e:
    print(f'Error reseting arduino: {e}')

def reset():
    io.output(resetPin, False)
    time.sleep(1)
    io.output(resetPin, True)
