import smbus
from time import sleep
address = 0x3E
bus = smbus.SMBus(1) #Channel 1 is connected to the GPIO pins
i=1000
while True:
    sleep(1)
    try:
        print("Writing to device")
        bus.write_i2c_block_data(address, i&0xFF, [i>>8])
    except Exception as e:
        print("Write error: " + str(e))
        continue
    read = 0
    while read==0:
        try:
            print("Reading from device")
            rx_bytes = bus.read_i2c_block_data(address, 0, 2)
        except Exception as e:
            print("Read error: " + str(e))
            continue
        read = 1
    print(f"Received: {str(rx_bytes)}")
    value = rx_bytes[0] + (rx_bytes[1] << 8)
    print(f"Read value: {value}")
    i+=1
    