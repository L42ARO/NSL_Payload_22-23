import adafruit_bno055
import board
import math
import time
import mods.talking_heads as talking_heads
import mods.buzzer as buzzer

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)
def checkForLanding():
    buzzer.startBuzzer()
    print("Awaiting launch ...")
    flag = 1
    while(flag == 1):
        velocity = sensor.linear_acceleration
        if ((velocity[0] == None) or (velocity[1] == None) or (velocity[2] == None)):
            continue
        magnitude = math.sqrt( (velocity[0] ** 2) + (velocity[1] ** 2) + (velocity[2] ** 2) )
        print(f"Velocity: {velocity} magnitude: {magnitude}", end="\r")
        if (magnitude >= 30):
            flag = 0
        buzzer.updateBuzzer()
        time.sleep(0.25)
    buzzer.turnoffBuzzer()
    print("Starting 120 second countdown ...")
    time.sleep(120)
    print("Checking for having landed ...")
    buzzer.startBuzzer()
    flag = 1
    while(flag == 1):
        velocity = sensor.linear_acceleration
        if ((velocity[0] == None) or (velocity[1] == None) or (velocity[2] == None)):
            continue
        magnitude = math.sqrt( (velocity[0] ** 2) + (velocity[1] ** 2) + (velocity[2] ** 2) )
        print(f"Velocity: {velocity} magnitude: {magnitude}", end="\r")
        if (magnitude <= 10):
            flag = 0
        buzzer.updateBuzzer()
        time.sleep(1)

    print("Landing confirmed.")
    buzzer.startBuzzer()
    return



if __name__=="__main__":
    checkForLanding()
