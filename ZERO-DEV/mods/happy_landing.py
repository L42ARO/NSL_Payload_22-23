import adafruit_bno055
import board
import math
import time


i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)
def checkForLanding():
    flag = 1
    while(flag == 1):
        velocity = sensor.linear_acceleration
        magnitude = math.sqrt( (velocity[0] ** 2) + (velocity[1] ** 2) + (velocity[2] ** 2) )
        print(f"Velocity: {velocity} magnitude: {magnitude}", end="\r")
        if (magnitude >= 69):
            flag = 0
        time.sleep(1)
    time.sleep(90)

    return

if __name__=="__main__":
    checkForLanding()