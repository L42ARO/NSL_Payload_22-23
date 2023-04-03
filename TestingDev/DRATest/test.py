import serial

# Open serial port
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

# Send command to set frequency to 144.390 MHz
ser.write(b'AT+DMOSETGROUP=0,144390000,0,0\r\n')

# Read response from module
response = ser.readline().decode('utf-8').strip()
print(response)

# Read response from module
response = ser.readline().decode('utf-8').strip()
print(response)

# Send command to establish connection
ser.write(b'AT+DMOCONNECT\r\n')

# Read response from module
response = ser.readline().decode('utf-8').strip()
print(response)

# Close serial port
ser.close()