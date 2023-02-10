import mods.mr_blue_sky as mr_blue_sky
import mods.happy_landing as happy_landing
import mods.talking_heads as talking_heads
import mods.bullseye as bullseye
import mods.utils as utils
import math
import mods.MoveServo as MoveServo
alkdsjfslakj
if __name__=="__main__":
    utils.exitListen()
    print("Starting ZERO-DEV")
    happy_landing.checkForLanding()
    mr_blue_sky.moveToHole()

    #define pins
    Servo1Pin = 18
    Servo2Pin = 19
    Servo3Pin = 12

    MoveServo.begin(Servo1Pin,True)
    MoveServo.begin(Servo2Pin,True)
    MoveServo.begin(Servo3Pin,True)
    
    mr_blue_sky.servoMover(90)
    #bullseye.TakePhoto("1stlaunch")
    bullseye.SeriesOfPics()


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
