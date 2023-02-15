import RPi.GPIO as io
import time

resetPin = 17
io.setmode(io.BCM)
io.setup(resetPin, io.OUT)
io.output(resetPin, True)

def reset():
    io.output(resetPin, False)
    time.sleep(1)
    io.output(resetPin, True)
