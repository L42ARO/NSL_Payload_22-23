import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

# Set up PWM signal on GPIO 19
pwm_19 = GPIO.PWM(19, 50)  # 50 Hz frequency
pwm_19.start(0)

# Set up PWM signal on GPIO 18
pwm_18 = GPIO.PWM(18, 50)  # 50 Hz frequency
pwm_18.start(0)

# Set up PWM signal on GPIO 12
pwm_12 = GPIO.PWM(12, 50)  # 50 Hz frequency
pwm_12.start(0)

# Move servo on GPIO 19 to 90 degrees
pwm_19.ChangeDutyCycle(7.5)  # 7.5% duty cycle for 90 degrees
time.sleep(1)

# Move servo on GPIO 18 to 90 degrees
pwm_18.ChangeDutyCycle(7.5)  # 7.5% duty cycle for 90 degrees
time.sleep(1)

# Move servo on GPIO 12 to 90 degrees
pwm_12.ChangeDutyCycle(7.5)  # 7.5% duty cycle for 90 degrees
time.sleep(1)

# Clean up GPIO pins
pwm_19.stop()
pwm_18.stop()
pwm_12.stop()
GPIO.cleanup()
