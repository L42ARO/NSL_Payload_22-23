import wave
import struct
import serial
import struct
import os
import re
import math
import scipy.signal
import soundfile as sf
import mods.contact as contact
import mods.reset_arduino as reset_arduino
import mods.talking_heads as talking_heads
import time
import platform
#create another 
def receive_signal(i):
    #reset_arduino.reset()
    #talking_heads.talk(4,0)
    #time.sleep(2)
    #write the signal into the file
    with open('output'+str(i)+'.txt', 'w+', encoding='UTF-16') as output:
        port='COM10'
        if platform.system()=='Linux':
            port='/dev/ttyAMA0'
        ser = serial.Serial(port, 500000)  # Replace COM_PORT with the actual port of your Arduino

        # Wait for data to start coming
        while ser.in_waiting == 0:
            pass

        text = ""
        #print("Incoming data...")
        output.write("Incoming data...")
        while True:
            byte = ser.read(1)
            if byte == b'>':
                break
            text += byte.decode('ascii')

        #print(text)
        output.write(text)

        #max_time = 5  # Set the maximum time in seconds
        #start_time = time.time()  # Record the start time of the loop
        #elapsed_time = 0  # Initialize the elapsed time to 0
        #counter=0

        while ser.in_waiting == 0:
            #elapsed_time = time.time() - start_time  # Calculate the elapsed time
            #if elapsed_time >= max_time:
                #run_receiver()
            pass

        while True:
            try:
                data = ser.read(1)
                if(data == b'<'):
                    break
                data2 = ser.read(1)
                val = struct.unpack('>H', data + data2)[0]
                
                #print(str(val))
                output.write(str(val)+'\n')
            except Exception as e:
                print(f'Error:{e}')

        text = ""
        while True:
            byte = ser.read(1)
            if byte == b'>':
                break
            text += byte.decode('ascii')
        output.write(text)
    output.close()

    #reopen the file to get the samples
    with open('output'+str(i)+'.txt', 'r', encoding='UTF-16') as output:
    #with open('output1.txt', 'r', encoding='UTF-16') as output:
        rows = [line.strip() for line in output.readlines()[16:-1]]
        samples=int(rows[-3].split(' ',1)[1])
    output.close()
    
    #creates file formatted for slicing
    with open('formatted_data'+str(i)+'.txt', 'w', encoding='UTF-16') as file:
        for row in rows:
            file.write(row+'\n')
    file.close()
    
    return samples
    

def create_audio_file(fileName):
    #opens formatted_data2.txt to get the time and framerate
    with open(fileName, 'r', encoding='UTF-16') as output:
        rows = [line.strip() for line in output.readlines()[16:]]
        time=int(rows[-5].split(' ', 1)[1])
        frameRate=int(float(rows[-1].split(' ', 1)[1]))
    output.close()

    # Read int values from file without last three ones
    with open(fileName, 'r', encoding='UTF-16') as data:
        values = [int(line.strip()) for line in data.readlines()[:-5]]
    data.close()

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
    duration = (nFrames / float(frameRate))
    checkTime=abs((time/1000000)-duration)<0.2

    #print(f'Time frm file:{time}, Duration calc:{duration}')
    #if the time on the file and the one calculated are the same, continue. Else, re-run everything
    if checkTime:
        pass
    else:
        run_receiver()

    # Close the wave file
    wav_file.close()

    if frameRate<6000:
        resample()

def decode_audio_file(wav_file):
    folder_path = os.getcwd()
    wav_path = os.path.join(folder_path, wav_file)
    
    #atest_path=r'C:\Users\alelo\Downloads\direwolf-1.7.0-dev-A_x86_64\direwolf-1.7.0-7fa91dd_i686\atest.exe'
    os.system('atest '+wav_path+' > ./decoded.txt')

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
        return msg
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

def resample():
    # Load the audio file
    audio_file = "signal.wav"
    audio_data, sample_rate = sf.read(audio_file)

    # Define the new sample rate
    new_sample_rate = 8000

    # Resample the audio data to the new sample rate
    resampled_data = scipy.signal.resample(audio_data, int(len(audio_data) * new_sample_rate / sample_rate))
    
    # Save the resampled data to a new audio file
    sf.write("signal.wav", resampled_data, new_sample_rate)

def get_commands():
    try:
        create_audio_file(run_receiver())
        decode_audio_file('signal.wav')
        commands=scan_decoded_file('decoded.txt', 'KQ4FYU')
        #reset_arduino.reset()
        if commands==['']:
            commands=contact.GetRAFCOSequence()
            return commands
        return commands
    except Exception as e:
        commands=contact.GetRAFCOSequence()
        print(e)
        return commands

if __name__=='__main__':
    commands=get_commands()
    print(commands)