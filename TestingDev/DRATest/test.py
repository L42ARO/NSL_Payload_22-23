import serial

# Open serial port
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# Send command to establish connection
command = "AT+DMOCONNECT \r\n"
ser.write(command.encode())


# Read response from module
response = ser.readline().decode('utf-8').strip()
print(response)

# Close serial port
ser.close()