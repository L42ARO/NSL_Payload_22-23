import mods.mr_blue_sky as mr_blue_sky
import mods.vector_perkins as vector
import mods.happy_landing as happy_landing
import mods.talking_heads as talking_heads
import mods.bullseye as bullseye
import mods.utils as utils
import math
import mods.MoveServo as MoveServo
import mods.vector_perkins as vector_perkins 

if __name__=="__main__":
    utils.exitListen()
    print("Starting ZERO-DEV")
    happy_landing.checkForLanding()

    # Move hole cover
    servo1Pin = 18
    servo1 = MoveServo.begin(servo1Pin,True)
    MoveServo.rotate(servo1, 0, 360)
    
    # Find the best hole and move the stepper
    vector_perkins.begin()
    angle = vector_perkins.getMainStepperAngle()
    talking_heads.talk(2, int(angle/math.pi * 180))
    vector_perkins.checkMainStepperRotation(angle)

    # Move camera extender
    servo2Pin = 19
    servo2 = MoveServo.begin(servo2Pin, True)
    MoveServo.rotate(servo2, 0, 90)

    # Move camera-tilting microstepper
    angle = vector_perkins.getMicroStepperAngle(angle)
    talking_heads.talk(5, int(angle/math.pi * 180))

    # Rotate 90 degrees and take 3 pics 
    for i in range(4):
        bullseye.SeriesOfPics()
        talking_heads.talk(5, 90)
        


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
