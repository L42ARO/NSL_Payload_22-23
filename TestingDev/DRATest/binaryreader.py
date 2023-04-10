import serial
import struct

ser = serial.Serial('COM15', 500000)  # Replace COM_PORT with the actual port of your Arduino

# Wait for data to start coming
while ser.in_waiting == 0:
    pass
print("Incoming data...")
num_samples = 10000
received_data = []

for _ in range(num_samples * 2):  # Each sample has 2 bytes
    received_data.append(ser.read(1))

readings = [struct.unpack('>H', received_data[i] + received_data[i + 1])[0] for i in range(0, num_samples * 2, 2)]
# Print the received ADC readings
print("ADC Readings:")
print(readings)

# Read and display the human-readable text
while True:
    byte = ser.read(1)
    if byte == b'<':
        break

text = ""
while True:
    byte = ser.read(1)
    if byte == b'>':
        break
    text += byte.decode('ascii')

print("Test Results:")
print(text)
