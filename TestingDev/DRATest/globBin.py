import serial
import struct

ser = serial.Serial('COM15', 500000)  # Replace COM_PORT with the actual port of your Arduino

# Wait for data to start coming
while ser.in_waiting == 0:
    pass

text = ""
print("Incoming data...")
while True:
    byte = ser.read(1)
    if byte == b'>':
        break
    text += byte.decode('ascii')

print(text)

while ser.in_waiting == 0:
    pass

while True:
    try:
        data = ser.read(1)
        if(data == b'<'):
            break
        data2 = ser.read(1)
        val = struct.unpack('>H', data + data2)[0]
        print(val)
    except:
        print("Error")

text = ""
while True:
    byte = ser.read(1)
    if byte == b'>':
        break
    text += byte.decode('ascii')

print(text)   