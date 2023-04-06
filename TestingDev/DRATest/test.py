import serial

# Open serial port
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
print("Opened serial port")
# Send command to establish connection
command = "AT+DMOCONNECT <CR><LF>"

ser.write(command.encode())
print("Sent: " + command)

# Read response from module
response = ser.readline().decode('utf-8').strip()
print(response)

# Close serial port
ser.close()