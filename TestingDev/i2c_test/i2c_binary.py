import smbus

command_size = 4 # Size of the command in bits
value_size = 16 # Size of the value in bits

'''Format of the data sent over I2C:
    5 bits for command size, 5 bits for value size, then the command bits and value bits according to the size specified'''
def send_command_via_i2c(command, value):
    # Initialize the I2C bus
    bus = smbus.SMBus(1)
    
    #Convert command and valus sizes to binary
    command_size_bin = format(command_size, '05b')
    value_size_bin = format(value_size, '05b')
    
    # Convert the command to binary
    command_binary = format(command, f'0{command_size}b')
    
    # Check if the value is positive or negative and convert it to binary using two's complement
    if value >= 0:
        value_binary = format(value, f'0{value_size}b')
    else:
        value_binary = format(2**16 + value, f'0{value_size}b')
    
    # Join the binary values and send it over I2C
    data = command_size_bin+value_size_bin+command_binary + value_binary
    print(f'Sending: {command} {value}\n Binary: {data} over I2C')
    bus.write_i2c_block_data(0x08, 0, [int(x) for x in data])

# Example usage
send_command_via_i2c(1, -258)