#has to run sudo pigpiod before running
from piservo import Servo
import board
import RPi.GPIO as io
import time

'''
myservo = Servo(18)

myservo.write(180)
time.sleep(3)
myservo.write(0)
time.sleep(3)
myservo.stop()

'''

def setservozero(servo_):
    servo_.write(0)
    time.sleep(0.1)

def rotate(servo_, startAngle, endAngle):
    i = -1 if startAngle > endAngle else 1

    for pos in range(startAngle, endAngle, i):
        servo_.write(pos)
        time.sleep(15)

    servo_.write(endAngle)
    
def begin(pin):
    myservo = Servo(pin)
    return myservo

if __name__ == "__main__":
    pin = 17
    startAngle = 0
    endAngle = 180
    
    bruh = begin(pin)
    setservozero(bruh)
    rotate(bruh, 0, 180)


'''
DIFFERENT PROGRAM

myservo = Servo(12)

myservo.write(180)
time.sleep(3)
myservo.write(0)
time.sleep(3)
myservo.stop()

 DIFFERENT PROGRAM
import piServoCtl
import board
import RPi.GPIO as io
import time

class MainServo:
    def rotate(self, startAngle, endAngle):
        i = -1 if startAngle > endAngle else 1

        for pos in range(startAngle, endAngle, i):
            piServoCtl.write(pos)
            piServoCtl.delay(15)
        piServoCtl.write(endAngle)
    
    def begin(self):
        piServoCtl.pinMode(pin, piServoCtl.OUTPUT)
        piServoCtl.attach(pin)

if __name__ == "__main__":
    pin = 21
    startAngle = 0
    endAngle = 180
    
    servo = MainServo()
    servo.begin()
    servo.rotate(startAngle, endAngle)
'''
