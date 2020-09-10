import numpy as np
import pyroomacoustics as pra
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sys

input = "./test_tmp/test/wav/" + sys.argv[1]
output = "./test_tmp/test/wav/test_impulse/test/" + sys.argv[2]

print(input)
print(output)
# Simulation parameters
fs = 16000
absorption = 0.25
max_order = 17

# Geometry of the room and location of sources and microphones
room_dim = np.array([10, 7.5, 3])
source_loc = np.array([2.51, 3.57, 1.7])
mic_loc = np.c_[[7, 6.1, 1.3],[6.9, 6.1, 1.3]]

# Create the room itself
room = pra.ShoeBox(room_dim, fs=fs, absorption=absorption, max_order=max_order)

# Place a source of white noise playing for 5 s
fs, audio_anechoic = wavfile.read(input)
room.add_source(source_loc, signal=audio_anechoic)

# Place the microphone array
room.add_microphone_array(
        pra.MicrophoneArray(mic_loc, fs=room.fs)
        )

# Now the setup is finished, run the simulation
room.simulate()
audio_after = room.mic_array.to_wav(output, norm=True, mono=True, bitdepth=np.int16)

# As an example, we plot the simulated signals, the RIRs, and the room and a
# few images sources

# The microphone signal are in the rows of `room.mic_array.signals`


# mic_signals = room.mic_array.signals
# plt.figure()
# plt.subplot(1,2,1)
# plt.plot(np.arange(mic_signals.shape[1]) / fs, mic_signals[0])
# plt.title('Microphone 0 signal')
# plt.xlabel('Time [s]')
# plt.subplot(1,2,2)
# plt.plot(np.arange(mic_signals.shape[1]) / fs, mic_signals[1])
# plt.title('Microphone 1 signal')
# plt.xlabel('Time [s]')
# plt.tight_layout()

# # Plot the room and the image sources
# room.plot(img_order=4)
# plt.title('The room with 4 generations of image sources')

# # Plot the impulse responses
# plt.figure()
# room.plot_rir()

# plt.show()
