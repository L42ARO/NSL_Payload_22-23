import wave
import struct
import serial
import struct
import os
import re
import math

def receive_signal(i):
    #ser = serial.Serial('COM11', 500000)  # Replace COM_PORT with the actual port of your Arduino
    
    #with open('output'+str(i)+'.txt', 'w+', encoding='UTF-16') as output:

        # # Wait for data to start coming
        # while ser.in_waiting == 0:
        #     pass

        # text = ""
        # print("Incoming data...")
        # output.write("Incoming data...")
        # while True:
        #     byte = ser.read(1)
        #     if byte == b'>':
        #         break
        #     text += byte.decode('ascii')

        # print(text)
        # output.write(text)

        # while ser.in_waiting == 0:
        #     pass

        # while True:
        #     try:
        #         data = ser.read(1)
        #         if(data == b'<'):
        #             break
        #         data2 = ser.read(1)
        #         val = struct.unpack('>H', data + data2)[0]
                
        #         print(str(val))
        #         output.write(str(val))
        #     except Exception as e:
        #         print(f'Error:{e}')

        # text = ""
        # while True:
        #     byte = ser.read(1)
        #     if byte == b'>':
        #         break
        #     text += byte.decode('ascii')
        # output.write(text)

        # rows = [line.strip() for line in output.readlines()[16:-2]]
        # #print(rows)
        # samples=int(rows[-3].split(' ',1)[1])

    #output.close()
    with open('outputNasa50.txt', 'r', encoding='UTF-16') as output:
        rows = [line.strip() for line in output.readlines()[16:-2]]
        samples=int(rows[-3].split(' ',1)[1])
    with open('formatted_data'+str(i)+'.txt', 'w', encoding='UTF-16') as file:
        for row in rows:
            file.write(row+'\n')
    file.close()
    
    return samples 
    

def create_audio_file(fileName, frameRate):
    # Read int values from file without last three ones
    with open(fileName, 'r', encoding='UTF-16') as data:
        values = [int(line.strip()) for line in data.readlines()[:-5]]
    
    # Set the parameters for the wave file
    nChannels = 1
    sampWidth = 2
    nFrames = len(values)

    # Create a new wave file and set its parameters
    wav_file = wave.open('signal.wav', 'w')
    wav_file.setparams((nChannels, sampWidth, frameRate, nFrames, 'NONE', 'not compressed'))

    # Convert the list of numbers to binary data and write it to the wave file
    for value in values:
        # Convert the value to a 2-byte binary data string (assuming 16-bit samples)
        binary_data = struct.pack('<h', int(value * 4))
        wav_file.writeframes(binary_data)

    #check if length is the same
    duration = int(nFrames / float(frameRate))
    print(values[-1])


    # Close the wave file
    wav_file.close()

def decode_audio_file(wav_file):
    folder_path = os.getcwd()
    wav_path = os.path.join(folder_path, wav_file)
    
    atest_path=r'C:\Users\alelo\Downloads\direwolf-1.7.0-dev-A_x86_64\direwolf-1.7.0-7fa91dd_i686\atest.exe'
    os.system(atest_path+' '+wav_path+' > ./decoded.txt')

def scan_decoded_file(fileName, callSign):
    message=''
    c=0
    with open(fileName, 'r') as file:
        #gets the string after the second callSign has been read
        for line in file:
            if callSign in line:
                c+=1
                if c==2:
                    message=line
    formatted_message=re.sub('_1', '~', re.sub('X/`', '~', message))
    msg=re.split('~', formatted_message)
    
    try:
        commands=msg[1].split()
    except:
        return f'No APRS packets received: {msg}'
    return commands

def run_receiver():
    sample=[]
    for i in range(1,4):
        sample.append(receive_signal(i))

    #if not math.isclose((sample[0]+sample[1]+sample[2])/3, sample[0], abs_tol=200):
    if math.isclose(sample[0], sample[1], abs_tol=5000) and math.isclose(sample[0], sample[2], abs_tol=5000) and math.isclose(sample[1], sample[2], abs_tol=5000):
        return 'formatted_data2.txt'
    else:
        run_receiver()
    
if __name__=='__main__':
    create_audio_file(run_receiver(), 5400)
    decode_audio_file('signal.wav')
    commands=scan_decoded_file('decoded.txt', 'KQ4FYU')
    print(commands)