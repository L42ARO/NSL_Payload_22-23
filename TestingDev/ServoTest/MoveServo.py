#has to run sudo pigpiod before running
from piservo import Servo
import board
import RPi.GPIO as io
import time

myservo = Servo(18)

myservo.write(180)
time.sleep(3)
myservo.write(0)
time.sleep(3)
myservo.stop()

'''
class MainServo:
    def rotate(self, startAngle, endAngle):
        i = -1 if startAngle > endAngle else 1

        for pos in range(startAngle, endAngle, i):
            piservo.write(pos)
            time.sleep(15)
        piservo.write(endAngle)
    
    def begin(self):
        myservo = piservo(21)

if __name__ == "__main__":
    pin = 21
    startAngle = 0
    endAngle = 180
    
    servo = MainServo()
    servo.begin(21)
    servo.rotate(startAngle, endAngle)

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
