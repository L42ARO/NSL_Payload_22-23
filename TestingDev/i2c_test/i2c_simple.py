import smbus
bus = smbus.SMBus(1)
address = 0x08

data = [ord(c) for c in "0_1"]
bus.write_i2c_block_data(address, 0, data)
