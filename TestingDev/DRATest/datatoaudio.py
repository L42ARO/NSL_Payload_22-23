import numpy as np
from scipy.io.wavfile import write

import scipy.io.wavfile as wav
import io
from pydub import AudioSegment
import re
import os

"""
# Timestamp and float values
data = '''
03:22:17.998 -> 325.00
03:22:18.046 -> 400.00
03:22:18.046 -> 466.00
...
'''

# Extract float values

# Normalize the values to range [-1, 1]
normalized_values = np.interp(float_values, (min(float_values), max(float_values)), (-1, 1))

# Set the sample rate (in Hz) and the duration of the signal (in seconds)
sample_rate = 48000
duration = len(float_values) / sample_rate

# Create the time array
t = np.linspace(0, duration, len(float_values), False)

# Convert the float values into a waveform
audio_data = (normalized_values * (2**15 - 1) / np.max(np.abs(normalized_values))).astype(np.int16)

# Write the audio data to a WAV file
write('output.wav', sample_rate, audio_data)


def convert_float_audio_to_file(float_audio_data, filename, sampling_rate=7500, file_format="wav"):
    
    # Convert float audio data to numpy array with int16 format
    int_audio_data = np.int16(float_audio_data * 32767)

    # Create io.BytesIO object to store audio data
    audio_bytes = io.BytesIO()

    # Write audio data to bytes buffer using wavfile.write() from SciPy
    wavfile.write(audio_bytes, sampling_rate, int_audio_data)

    # Reset byte stream position
    audio_bytes.seek(0)

    # Read audio data from bytes buffer as AudioSegment from pydub
    audio_segment = AudioSegment.from_file(audio_bytes, format="wav")

    # Export audio segment to file with given format
    audio_segment.export(filename, format=file_format)
"""
"""
def convert_file_to_audio(filename, output_filename, file_format="mp3"):
    # Read data from file
    with open(filename, 'r') as file:
        lines = file.readlines()

    timestamps = []
    float_audio_data = []

    # read the file and extract the timestamps and float values
    with open(filename) as file:
        for line in file:
            if "->" in line:
                timestamp, value = line.split("->")
                timestamps.append(float(timestamp.strip()))
                float_audio_data.append(float(value.strip()))

    # calculate the time differences between timestamps to obtain the sampling rate
    time_diffs = np.diff(timestamps)
    time_diffs = time_diffs[~np.isnan(time_diffs) & ~np.isinf(time_diffs)] 
    sampling_rate = int(1 / np.median(time_diffs) * 1000)

    # Convert float audio data to numpy array with int16 format
    int_audio_data = np.int16(np.array(audio_data) * 32767)

    # Create io.BytesIO object to store audio data
    audio_bytes = io.BytesIO()

    # Write audio data to bytes buffer using wavfile.write() from SciPy
    wavfile.write(audio_bytes, sampling_rate, int_audio_data)

    # Reset byte stream position
    audio_bytes.seek(0)

    # Read audio data from bytes buffer as AudioSegment from pydub
    audio_segment = AudioSegment.from_file(audio_bytes, format="wav")

    # Export audio segment to file with given format
    audio_segment.export(output_filename, format=file_format)

    # Return output filename
    return output_filename
"""

"""
def create_audio_file(file_name, samplenumber, time_taken, file_Output_name="AudioOutputTest.wav"):
    sampling_rate = 1000000.0 * samplenumber / time_taken
    # Read float values from text file
    with open(file_name, 'r') as f:
        float_array = np.array([float(line.rstrip()) for line in f])
    
    # Convert float values to audio data
    audio_data = np.int16(float_array * 32767) # Scale float values to 16-bit range
    audio_data = np.repeat(audio_data, sampling_rate//len(audio_data)) # Repeat samples to match desired sampling rate
    
    # Write audio data to WAV file
    wav.write(file_Output_name, sampling_rate, audio_data)
"""
"""
import numpy as np
import wave

def create_audio_file(filename, samplenumber, time_taken, filename_Output = "AudioOutputTest.wav"):
    sampling_rate = 1000000.0 * samplenumber / time_taken
    # Read float values from file
    with open(filename, 'r') as f:
        values = [float(line.strip()) for line in f.readlines()]

    # Convert float values to array of 16-bit integers
    max_vol = 2 ** 15 - 1
    audio_data = np.array(values) * max_vol
    audio_data = audio_data.astype(np.int16)

    # Create audio file
    audio_file = wave.open(filename_Output, 'w')
    audio_file.setnchannels(1)  # Mono audio
    audio_file.setsampwidth(2)  # 16-bit audio
    audio_file.setframerate(sampling_rate)
    audio_file.writeframes(audio_data.tobytes())
    audio_file.close()
"""
from pydub import AudioSegment
import wave
import struct

def create_audio_file(filename = "data3.txt", sampling_rate = 1000000.0 * 39484/ (39484/7800)):
    # Read float values from file
    with open(filename, 'r', encoding='UTF-16') as f:
        values = [int(line.strip()) for line in f.readlines()[:-3]]
    
    # Set the parameters for the wave file
    nchannels = 1
    sampwidth = 2
    framerate = 7800
    nframes = len(values)

    # Create a new wave file and set its parameters
    wav_file = wave.open('output3.wav', 'w')
    wav_file.setparams((nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed'))

    # Convert the list of numbers to binary data and write it to the wave file
    for value in values:
        # Convert the value to a 2-byte binary data string (assuming 16-bit samples)
        binary_data = struct.pack('<h', int(value * 4))
        wav_file.writeframes(binary_data)

    # Close the wave file
    wav_file.close()
    '''
    
    # Convert float values to array of 16-bit integers
    max_vol = 2 ** 15 - 1
    audio_data = np.array(values) * max_vol
    audio_data = audio_data.astype(np.int16)

    # Create audio file
    audio_segment = AudioSegment(audio_data.tobytes(), frame_rate=sampling_rate, sample_width=2, channels=1)
    audio_segment.export('output.wav', format='wav')
'''

if __name__ == "__main__":
    create_audio_file ("data3.txt")

