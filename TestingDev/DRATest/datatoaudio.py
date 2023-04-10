import numpy as np
from scipy.io.wavfile import write

# Timestamp and float values
data = '''
03:22:17.998 -> 325.00
03:22:18.046 -> 400.00
03:22:18.046 -> 466.00
...
'''

# Extract float values
float_values = [float(line.split("->")[1]) for line in data.strip().split("\n")]

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
