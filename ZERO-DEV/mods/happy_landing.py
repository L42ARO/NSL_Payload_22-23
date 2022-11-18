import adafruit_bno055
import board
import time
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)
def checkForLanding():
    while(True):
        velocity = sensor.acceleration
        print(f"Velocity: {velocity}", end="\r")
        time.sleep(1)
    return

if __name__=="__main__":
    checkForLanding()