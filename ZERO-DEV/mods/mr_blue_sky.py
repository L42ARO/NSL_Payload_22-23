import adafruit_bno055
import board
import time
import math
import mods.talking_heads as talking_heads

i2c = board.I2C()  # uses board.SCL and board.SDA

sensor = adafruit_bno055.BNO055_I2C(i2c, 0x28)
sensor2 = adafruit_bno055.BNO055_I2C(i2c, 0x29)
#Return the average of all calibration values

def CheckCalibration():
    #Check for ZERO IMU calibration
    sys, gyro, accel, mag = sensor.calibration_status
    cal = dict()
    cal["sys"] = sys
    cal["gyro"] = gyro
    cal["accel"] = accel
    cal["mag"] = mag
    return cal
    #Check PICO IMU calibration

def calib2():
    print("Starting motor alignement")
    #Confidence treshold for calibration
    vertical = False
    calib_need = True
    #Enter Loop to align
    while(vertical == False):
        if(calib_need == True):
            accel_confirms=0
            sys_confirms = 0
            zero_cal = CheckCalibration()
            while(zero_cal["gyro"] != 3):
                print(f"Waiting still for gyro: {zero_cal['gyro']}", end="\r")
                zero_cal=CheckCalibration()
                time.sleep(1)
            #Wait for calibration to be good
            print("Starting other sensors calibration")
            while(accel_confirms <=10 and sys_confirms <=10):
                #Check for ZERO IMU calibration
                if(zero_cal["accel"] >=3):
                    accel_confirms += 1
                if(zero_cal["sys"] >=3):
                    sys_confirms += 1
                print(f"Accel: {zero_cal['accel']}, Sys: {zero_cal['sys']} - Accel Good: {accel_confirms}/10, Sys_Good={sys_confirms}", end='\r')
                zero_cal = CheckCalibration()
                time.sleep(1)
            print("Calibration seems good chief")
        gyro = sensor.euler
        gravity = sensor.gravity
        accel = sensor.acceleration
        input("Press enter to continue chief")
        print(f"Gyro (x,y,z):{gyro}")
        print(f"Gravity (x,y,z): {gravity}")
        print(f"accel (x,y,z): {accel}")
        vertical=True #Just for testing
        #Check orientation ZERO
        #Check orientation PICO
        #Move motor
        #Check if vertical alignment is good
        #Exit loop

def getAcceleration():
    accel = sensor.acceleration
    accel2 = sensor2.acceleration
    print(f"accel (x,y,z): {accel}")
    print(f"accel (x,y,z): {accel2}")
    return (accel, accel2)

def computeOrientation(holeList, imu1_gravity, imu2_gravity, imu1_axis=[0,1], imu2_axis=[0,1],imus_inverted=False, cameraAngle=0):
    #accel = sensor.acceleration
    #cameraAccel = sensor2.acceleration
    #create a function that using the before statement can get an angle 
    #Getting angle between gravity and y-axis

    #get angle from x and y parameters of the gravity vector
    #there is a chance for the sensor to return NULL type. make sure functions deal witht this.
    gravityAngle = getAngleFromCoordinate(imu1_gravity[imu1_axis], imu1_gravity[imu1_axis])

    #invert it
    imu1_verticalAngle = invertGravityVector(gravityAngle)

    #find closest hole
    #holeList is to be given when calling the function
    holeAngle = angleCalc(holeList, imu1_verticalAngle)
    verticalDeviation = getAngleBetween(holeAngle, imu1_verticalAngle)
    if(imus_inverted): verticalDeviation = -verticalDeviation
    imu2_verticalAngle = getAngleFromCoordinate(imu2_gravity[imu2_axis], imu2_gravity[imu2_axis]) 
    
    #take two angles and find shortest rotation path
    rotationAngle = getAngleBetween(holeAngle, cameraAngle)

    #deal with possible negative angles - sending negative values is inconvenient

    return rotationAngle

#closest angle function // chooses hole
def angleCalc(angList, Angle):
    return min(angList, key=lambda x:abs(getAngleBetween(x, Angle)))

# Converts coordinates to polar and returns the angle
#function that turns x,y parameters into angle
def getAngleFromCoordinate(x, y):
    if (x == 0 and y == 0):
        raise Exception("Cannot assign angle to the origin.")
    elif (y == 0):
        return 0 if x > 0 else math.pi
    elif (x == 0):
        return math.pi/2 if y > 0 else 3*math.pi/2

    return math.atan(y/x) % (2*math.pi) if x > 0 else math.atan(y/x) + math.pi


def servoMover(degrees):
    talking_heads.talk('1-'+str(degrees))

# Inverts the gravity vector by pi radians.
# This funtion inverts the gravity vector and 
def invertGravityVector(gAngle):
    return (gAngle + math.pi) % (2*math.pi)

# Get the smaller angle between the camera and the hole.  Positive angle means counterclockwise rotation 
def getAngleBetween(holeAngle, cameraAngle):
    angle = holeAngle - cameraAngle
    if (angle > math.pi):
        angle -= 2*math.pi
    elif (angle < -math.pi):
        angle += 2*math.pi
        
    return angle

def moveToHole():
    angle = computeOrientation()
    talking_heads.talk('2-'+str(angle))


if __name__=="__main__":
    moveToHole()