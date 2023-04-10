import adafruit_bno055
import board
import math
import time
from datetime import datetime
import mods.talking_heads as talking_heads
import mods.buzzer as buzzer
import mods.reset_arduino as reset_arduino
import csv

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)
def checkForLanding(sleeptime = 120):
    #timestamp file
    timestamp = str(datetime.now().timestamp())
    timestr = timestamp.replace('.', '_') + ".csv"
    print(f"Writing to file: {timestr}")
    f = open(timestr, "w")
    writer=csv.writer(f)
    writer.writerow(["Time", "Velocity", "Magnitude"])
    
    buzzer.startBuzzer()
    print("Awaiting launch ...")
    flag = 1
    while(flag == 1):
        try:
            velocity = sensor.linear_acceleration
        except:
            print("Erro reading velocity, reseting")
            reset_arduino.reset()
            continue
        if ((velocity[0] == None) or (velocity[1] == None) or (velocity[2] == None)):
            continue
        magnitude = math.sqrt( (velocity[0] ** 2) + (velocity[1] ** 2) + (velocity[2] ** 2) )
        curTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Time: {curTime} Velocity: {velocity} magnitude: {magnitude}")
        data = [curTime, velocity, magnitude]
        writer.writerow(data)
        if (magnitude >= 30):
            flag = 0
        buzzer.updateBuzzer()
        time.sleep(0.25)
    buzzer.turnoffBuzzer()
    print("Starting 120 second countdown ...")
    # time.sleep(sleeptime)
    t_end = time.time() + sleeptime #Run for 2 Minutes or 120 seconds, grabs current time and adds the number of seconds from sleeptime
    while time.time() < t_end:
        try:
            velocity = sensor.linear_acceleration
        except:
            print("Erro reading velocity, reseting")
            reset_arduino.reset()
            continue
        if ((velocity[0] == None) or (velocity[1] == None) or (velocity[2] == None)):
            continue
        magnitude = math.sqrt( (velocity[0] ** 2) + (velocity[1] ** 2) + (velocity[2] ** 2) )
        curTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Time: {curTime} Velocity: {velocity} magnitude: {magnitude}")
        data = [curTime, velocity, magnitude]
        writer.writerow(data)
        time.sleep(0.001)
    
    print("Checking for having landed ...")
    buzzer.startBuzzer()
    flag = 1
    while(flag == 1):
        try:
            velocity = sensor.linear_acceleration
        except:
            print("Erro reading velocity, reseting")
            reset_arduino.reset()
            continue
        if ((velocity[0] == None) or (velocity[1] == None) or (velocity[2] == None)):
            continue
        magnitude = math.sqrt( (velocity[0] ** 2) + (velocity[1] ** 2) + (velocity[2] ** 2) )
        curTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Time: {curTime} Velocity: {velocity} magnitude: {magnitude}")
        data = [curTime, velocity, magnitude]
        writer.writerow(data)
        if (magnitude <= 10):
            flag = 0
        buzzer.updateBuzzer()
        time.sleep(1)

    f.close()
    print("Landing confirmed.")
    buzzer.startBuzzer()
    return



if __name__=="__main__":
    checkForLanding()
