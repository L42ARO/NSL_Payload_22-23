import serial

# Open serial port to USB device
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Send command to USB device
ser.write(b'Hello, USB device!\r\n')

# Read response from USB device
response = ser.readline().decode('utf-8').strip()
print(response)

# Close serial port
ser.close()