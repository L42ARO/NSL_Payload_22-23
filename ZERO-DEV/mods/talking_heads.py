
#!/usr/bin/env python3
import serial
import time
    
def talk(cmd):
    
    flag = True
    while(flag):
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()
        ser.write((cmd+'\n').encode('utf-8'))
        line = ser.readline().decode('utf-8').rstrip()
        if (line == cmd):
            flag = False
    print("Received: ", line)

    flag = True
    while(flag):
        line = ser.readline().decode('utf-8').rstrip()
        if (line == 'High'):
            flag = False

    ser.write('0\n'.encode('utf-8'))
    
    time.sleep(1)

if __name__ == "__main__":
    talk()