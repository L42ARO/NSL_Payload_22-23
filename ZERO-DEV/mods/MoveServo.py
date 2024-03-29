import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class ServoMotor:
    def __init__(self, pin):
        # Set up GPIO pin
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

        # Set up PWM signal
        self.pwm = GPIO.PWM(self.pin, 50)  # 50 Hz frequency
        self.pwm.start(0)

    def rotate(self, angle):
        # Convert angle to duty cycle
        duty_cycle = 2.5 + angle / 18

        # Move servo to specified angle
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.75)  # Wait for servo to move
    
class FullServo:
    def __init__(self, pin):
        # Set up GPIO pin
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

        # Set up PWM signal
        self.pwm = GPIO.PWM(self.pin, 50)  # 50 Hz frequency
        self.pwm.start(0)
        self.approximate_speed = 20000  

    def rotate(self, angle):
        # Calculate duration based on angle and approximate speed
        duration = abs(angle) /self.approximate_speed
        print(f'Rotating for {duration} seconds.')

        # Determine rotation direction
        if angle >= 0:
            duty_cycle = 7.5 + 1  # Clockwise rotation
        else:
            duty_cycle = 7.5 - 1  # Counterclockwise rotation

        # Set servo rotation speed
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(duration)  # Rotate for the calculated duration

        # Stop servo after rotation
        self.stop()

    def stop(self):
        # Stop servo by setting duty cycle to the neutral position (7.5%)
        self.pwm.ChangeDutyCycle(7.5)
        time.sleep(0.5)  # Allow time for the servo to stop

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

    #def __del__(self):
    #    # Clean up GPIO pin
    #    self.pwm.stop()
    #    GPIO.cleanup(self.pin)

'''from piservo import Servo
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
    b = begin(19, True)
    
    pin = 18
    startAngle = 0
    endAngle = 180
    
    bruh = begin(pin, True)
    time.sleep(1)
    rotate(bruh, 0, 90)
    
    pin = 12
    startAngle = 0
    endAngle = 180
    
    bruh2 = begin(pin, True)
    time.sleep(1)
    #rotate(bruh2, 0, 90)
    '''
