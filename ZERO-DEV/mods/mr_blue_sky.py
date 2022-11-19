import adafruit_bno055
import board
import time
import math
import talking_heads

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)
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
    print(f"accel (x,y,z): {accel}")
    return accel
def computeOrientation():
    accel = sensor.acceleration
    #Getting angle between gravity and y-axis
    #x is static. 
    #then value of gravity is <0,y,z>
    #find angle between <0,y,z> and <0,1,0>
    gMag = math.sqrt(accel[1]**2 + accel[2]**2)
    #Angle is in radians
    angle = math.acos(((accel[1]) / (gMag)))
    holes={
        "H1": [0,1,1],
        "H2": [0,-1,1],
        "H3": [0,-1,-1],
        "H4": [0,1,-1]
    }
    quadrant = 0
    if(angle <= math.pi/2 and accel[2] > 0):
        quadrant = 1
        holeToMove = "H3"
    elif(angle > math.pi/2 and accel[2] > 0):
        quadrant = 2
        holeToMove = "H4"
    elif(angle > math.pi/2 and accel[2] < 0):
        quadrant = 3
        angle = (math.pi*2) - (angle)
        holeToMove = "H1"
    elif(angle <= math.pi/2 and accel[2] < 0):
        quadrant = 4
        angle = (math.pi*2) - (angle)
        holeToMove = "H2"

    #Assumed initial camera position: <0,0,1>
    destVector = holes[holeToMove]
    #Dot product between camera and destination
    camVector = [0,0,1]
    dotDestCam = camVector[0]*destVector[0] + camVector[1]*destVector[1] + camVector[2]*destVector[2]
    #Magnitude of destination vector
    destMag = math.sqrt(destVector[0]**2 + destVector[1]**2 + destVector[2]**2)
    #Magnitude of camera vector
    camMag = math.sqrt(camVector[0]**2 + camVector[1]**2 + camVector[2]**2)
    #Angle between camera and destination
    angleDestCam = math.acos(dotDestCam/(destMag*camMag))


    return int( round(angleDestCam, 0) ) #round allows value to be rounded up to 131 if 130.9

def servoMover(degrees):
    talking_heads.talk('1-'+degrees)


def moveToHole():
    angle = 90
    #computeOrientation()
    talking_heads.talk('2-'+angle)


if __name__=="__main__":
    moveToHole()