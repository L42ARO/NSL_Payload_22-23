import adafruit_bno055
import board
import time

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)
def displayCalibrationStatus():
    sys, gyro, accel, mag = sensor.calibration_status
    print("Sys:", sys, "Gyro:", gyro, "Accel:", accel, "Mag:", mag)
while True:
    displayCalibrationStatus()
    print(f"Gyro (x,y,z):{sensor.euler}")
    print(f"Gravity (x,y,z): {sensor.gravity}")
    time.sleep(1)
