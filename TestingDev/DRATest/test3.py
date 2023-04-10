
# Open serial port to DRA818V module
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

# Send AT command to set frequency to 144.390 MHz
ser.write(b'AT+DMOSETGROUP=2457100,144390000,0,0,0\r\n')

# Read response from DRA818V module
response = ser.readline().decode('utf-8').strip()
print(response)

# Send AT command to set power level to 5W
ser.write(b'AT+DMOSETVOLUME=5\r\n')

# Read response from DRA818V module
response = ser.readline().decode('utf-8').strip()
print(response)

# Close serial port
ser.close()