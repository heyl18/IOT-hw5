import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import random
from utils import save_wave_file, int2code,str2code

fm1 = 6000  # signal 1 freq
fm0 = 0  # signal 0 freq
fs = 48000  # sample rate
Am = 3e6
duration = 0.0125
symbol_len = int(duration * fs)
t = np.arange(0, (symbol_len)/fs, 1/fs)

smb1 = Am * np.cos(2*np.pi*fm1*t)

smb0 = Am * np.cos(2*np.pi*fm0*t)

pre_data = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
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
    sig = []
    blank_size = int(fs/4)
    for i in range(200):
        if i % 2 == 0:
            sig.extend(smb1)
        else:
            sig.extend(smb0)
    sig.extend(np.zeros(2*blank_size))
    save_wave_file(sig,'getdistance.wav',framerate=fs)