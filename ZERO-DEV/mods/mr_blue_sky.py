import adafruit_bno055
import board
import vector_perkins as vp
import time
import math
import mods.talking_heads as talking_heads

i2c = board.I2C()  # uses board.SCL and board.SDA
rot_tresh = 1

sensor = adafruit_bno055.BNO055_I2C(i2c)
sensor2 = adafruit_bno055.BNO055_I2C(i2c, 0x29)

def getAcceleration():
    accel = sensor.acceleration
    print(f"accel (x,y,z): {accel}")
    return accel

def computeOrientation(holeList, imu1_gravity, imu2_gravity, imu1_axis=[0,1], axis2,imus_inverted=False):
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

    imu2_destiny = 
    
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
    #enter loop for at least 10 iterations (or until code inside breaks out)
    for i in range(10):
        #setup vp profile
        vp.LoadVectorProfile()
        #get gravity vectors from both sensors
        gravity1 = sensor1.acceleration
        #use vector perkins to get rotation angle
        #if angle is less than treshhold no need to rotate, break loop
        #else rotate  

    #angle = computeOrientation()
    #talking_heads.talk('2-'+str(angle))


if __name__=="__main__":
    moveToHole()