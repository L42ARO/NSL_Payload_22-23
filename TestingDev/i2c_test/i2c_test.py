import smbus
import time

bus = smbus.SMBus(1)

address = 0x08

def send_command(command):
	bus.write_i2c_block_data(address,0,list(command.encode()))
def receive_response():
	data = bus.read_i2c_block_data(address, 0, 32)
	print(data)
	return "".join([chr(i) for i in data if i !=0])	
def main():
	command = "1-0"
	send_command(command)
	time.sleep(1)
	response=receive_response().strip()
	print("Received:",response)

if __name__=="__main__":
	main()
