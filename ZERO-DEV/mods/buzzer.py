import board
import RPi.GPIO as io
import time

starttime = 0
buzzPin = 23
interval = 1    # in seconds
buzzerOn = False
io.setmode(io.BCM)
io.setup(buzzPin, io.OUT)


def toggleBuzzer():
    buzzerOn = not buzzerOn
    io.output(buzzPin, buzzerOn)

def startBuzzer(time):
    starttime = time.time()
    io.output(buzzPin, True)

def turnoffBuzzer():
    io.output(buzzPin, False)

def updateBuzzer():
    if (time.time() - starttime > interval):
        toggleBuzzer()
        starttime = time.time()


if (__name__=="__main__"):
    i = 0
    startBuzzer()
    while (i < 100):
        updateBuzzer()
        i+=1
    turnoffBuzzer()