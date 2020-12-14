import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import random
from utils import save_wave_file, int2code,str2code

fm1 = 6000  # signal 1 freq
fm0 = 4000  # signal 0 freq
fs = 48000  # sample rate
Am = 3e6
duration = 0.025
symbol_len = duration * fs
t = np.arange(0, (symbol_len)/fs, 1/fs)

smb1 = Am * np.cos(2*np.pi*fm1*t)

smb0 = Am * np.cos(2*np.pi*fm0*t)

pre_data = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
def encode(data):
    sig = []
    blank_len = int(symbol_len * 4)
    sig.extend(np.zeros(blank_len))
    len_data = int2code(len(data))
    for data in pre_data + len_data + data:
        if data == 0:
            sig.extend(smb0)
        else:
            sig.extend(smb1)
    sig.extend(np.zeros(blank_len))
    save_wave_file(sig,'output.wav',framerate=fs)
    return sig

if __name__ == '__main__':
    user_str = input("Please enter a string to be encoded:")
    # user_str = "I am a poor student from Tsinghua University!"
    test_code = str2code(user_str)
    encode(test_code)
    print(len(test_code))
