
#!/usr/bin/env python3
import serial
import time
    
def talk():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        ser.write("Hello from Raspberry Pi!\n".encode('utf-8'))
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
if __name__ == "__main__":
    talk()