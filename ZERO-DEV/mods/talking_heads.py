
#!/usr/bin/env python3
#import serial
import smbus
import time

bus = smbus.SMBus(1)
address = 0x08

#Returns 1 if successful, 0 if timeout
def talk(command_number, value, timeout=5):
    try:
        command = str(command_number) + "_" + str(value)
        bus.write_i2c_block_data(address, 0, list(command.encode()))
        start_time = time.time()
        while True:
            data = bus.read_i2c_block_data(address, 0)
            data = ''.join(map(chr, data))
            if data == "ready":
                print("Success")
                return 1
            if time.time() - start_time > timeout:
                print("Error: Timeout")
                return 0
            time.sleep(0.1)
    except Exception as e:
        print(f'Error talking to Pico: {e}')
        return 0

# def talk(cmd):
#     try:
#         flag = True
#         print(f"Sending: {cmd}")
#         while(flag):
#             ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#             ser.reset_input_buffer()
#             ser.write((cmd+'\n').encode('utf-8'))
#             line = ser.readline().decode('utf-8').rstrip()
#             if (line == cmd):
#                 flag = False
#         print("Received: ", line)

#         flag = True
#         while(flag):
#             line = ser.readline().decode('utf-8').rstrip()
#             if (line == 'High'):
#                 flag = False

#         ser.write('0\n'.encode('utf-8'))
    
#         time.sleep(1)
#         pass
#     except Exception as e:
#         print(f'Error talking to Pico: {e}')


if __name__ == "__main__":
    talk("1", "-258")