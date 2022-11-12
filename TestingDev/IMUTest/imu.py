import RPi.GPIO as GPIO

scl = 3
sda = 2

GPIO.setmode(GPOI.BOARD)
GPIO.setup(scl, GPIO.OUT)
GPIO.setup(sda, GPIO.IN)
