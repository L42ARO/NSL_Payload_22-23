import mods.mr_blue_sky as mr_blue_sky
import mods.happy_landing as happy_landing
import mods.talking_heads as talking_heads
#import mods.bullseye as bullseye
import math

if __name__=="__main__":
    print("Starting ZERO-DEV")
    #happy_landing.checkForLanding
    mr_blue_sky.moveToHole()
    mr_blue_sky.servoMover(90)
    #bullseye.TakePhoto("69")


    #Check For Landing
    #Turn motor
    #Take camera out
    #Take pictures loop

#i2c = board.I2C()  # uses board.SCL and board.SDA
#sensor = adafruit_bno055.BNO055_I2C(i2c)
#def displayCalibrationStatus():
#    sys, gyro, accel, mag = sensor.calibration_status
#    print("Sys:", sys, "Gyro:", gyro, "Accel:", accel, "Mag:", mag)
#while True:
#    displayCalibrationStatus()
#    print(f"Gyro (x,y,z):{sensor.euler}")
#    print(f"Gravity (x,y,z): {sensor.gravity}")
#    time.sleep(1)
