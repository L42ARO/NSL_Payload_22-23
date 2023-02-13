from piservo import Servo
import board
import RPi.GPIO as io
import time

def rotate(servo_, startAngle, endAngle):
    i = -1 if startAngle > endAngle else 1
    #Pull
    for pos in range(startAngle, endAngle, i):
        servo_.write(pos)
        time.sleep(0.0015)

    servo_.write(endAngle)
    
def begin(pin, restarter = False, startAngle = 0):
    myservo = Servo(pin)
    if(restarter == True):
        myservo.write(startAngle)
        time.sleep(0.1)
    return myservo


if __name__ == "__main__":
    pin = 19
    startAngle = 0
    endAngle = 180
    
    bruh = begin(pin, True)
    time.sleep(1)
    rotate(bruh, 0, 90)
