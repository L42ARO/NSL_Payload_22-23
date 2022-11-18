import adafruit_bno055
import board
import time

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
    

def align():
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


if __name__=="__main__":
    align()