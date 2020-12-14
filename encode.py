import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import random
from utils import save_wave_file, int2code,str2code

fm1 = 6000  # signal 1 freq
fm0 = 4000  # signal 0 freq
fs = 48000  # sample rate
Am = 3e6
duration = 0.0125
symbol_len = int(duration * fs)
t = np.arange(0, (symbol_len)/fs, 1/fs)

smb1 = Am * np.cos(2*np.pi*fm1*t)

smb0 = Am * np.cos(2*np.pi*fm0*t)

pre_data = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
def encode(data):
    sig = []
    blank_len = symbol_len * 2
    sig.extend(np.zeros(blank_len))
    len_data = int2code(len(data))
    for data in pre_data + len_data + data:
        if data == 0:
            sig.extend(smb0)
        else:
            sig.extend(smb1)
    sig.extend(np.zeros(blank_len))
    return sig

if __name__ == '__main__':
    user_str = input("Please enter a string to be encoded:")
    sig = []
    blank_size = int(48000/4)
    sig.extend(np.zeros(2*blank_size))
    for i in range(0,len(user_str),30):
        j = 30 if i + 30 < len(user_str) else len(user_str)
        test_code = str2code(user_str[i:i+j])
        sig.extend(encode(test_code))
        sig.extend(np.zeros(blank_size))
    sig.extend(np.zeros(2*blank_size))
    save_wave_file(sig,'output.wav',framerate=fs)