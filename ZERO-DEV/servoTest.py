import time
from mods.MoveServo import FullServo

servo_pin = 18  # Replace with the GPIO pin you're using
servo = FullServo(servo_pin)

try:
    # Rotate the servo motor at maximum clockwise speed for 5 seconds
    servo.rotate(20)

finally:
    servo.cleanup()
