import smbus
import time

# Open I2C bus and specify the device address
bus = smbus.SMBus(1)
address = 8

while True:
    try:
        # Read a byte from the Arduino
        byte = bus.read_byte(address)
        # Convert the byte to a character and print it
        print(chr(byte), end='')
    except:
        # If an error occurs, wait for a short time before trying again
        time.sleep(0.1)