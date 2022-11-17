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
    cal["avg"]= (sys/3+gyro/3+accel/3+mag/3)/4
    return cal
    #Check PICO IMU calibration
    

def align():
    print("Starting motor alignement")
    #Confidence treshold for calibration
    treshold = 0.9
    tresh_confirms=0
    zero_cal = CheckCalibration()
    vertical = False
    calib_need = True
    #Enter Loop to align
    while(vertical == False):
        #Sys must be zero before start trying to calibrate
        if(calib_need == True):
            while(zero_cal["sys"] != 0):
                print("Waiting to beign reading data")
                zero_cal=CheckCalibration()
                time.sleep(1)
            #Wait for calibration to be good
            while(tresh_confirms < 5):
                #Check for ZERO IMU calibration
                if(zero_cal["avg"] > treshold):
                    tresh_confirms += 1
                zero_cal = CheckCalibration()
                if(treshold>0.7):
                    treshold-=0.02
                time.sleep(1)
            print("Calibration seems good chief")
        gyro = sensor.euler
        gravity = sensor.gravity
        print(f"Gyro (x,y,z):{gyro}")
        print(f"Gravity (x,y,z): {gravity}")
        vertical=True #Just for testing
        #Check orientation ZERO
        #Check orientation PICO
        #Move motor
        #Check if vertical alignment is good
        #Exit loop


if __name__=="__main__":
    align()