#!/user/bin/python

import board
import RPi.GPIO as io
import time


buzzPin = 23

def buzzTest():
    io.setmode(io.BCM)
    io.setup(buzzPin, io.OUT)

    while (True):
        io.output(buzzPin, True)
        time.sleep(2)
        io.output(buzzPin, False)
        time.sleep(2)

buzzTest()
