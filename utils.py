# -*- coding:utf-8 -*-
import wave
import numpy as np
from scipy import signal

def encode(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])

def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

def str2code(msg):
    code = []
    for c in msg:
        encode_c = encode(c)
        while(len(encode_c) < 8):
            encode_c = '0' + encode_c
        for i in encode_c:
            code.append(int(i))
    return code

def int2code(num):
    code = []
    num_bin = bin(num)[2:]
    for c in num_bin:
        code.append(int(c))
    while len(code) < 11:
        code = [0] + code
    return code

def code2int(code):
    num_int = 0
    for i in range(0,10):
        num_int += int(code[i]) * 2**(10-i)
    return num_int

def code2str(code):
    msg = ''
    for i in range(0, len(code), 8):
        if i + 8 > len(code):
            break
        c = ''
        for j in range(i,i+8):
            c += str(code[j])
        msg += decode(c)
    return msg

def save_wave_file(wave_data, file_name, nchannels=1, sampwidth=2, framerate=9600):
    wave_data = np.array(wave_data).astype(np.short)

    # open a wav document
    f = wave.open(file_name, "wb")

    # set wav params
    f.setnchannels(nchannels)
    f.setsampwidth(sampwidth)
    f.setframerate(framerate)

    # turn the data to string
    f.writeframes(wave_data.tostring())
    f.close()


def open_wave_file(file_name):
    """解析wav文件，返回音频数据，帧数，帧率"""
    f = wave.open(file_name, "rb")
    params = f.getparams()
    [nchannels, sampwidth, framerate, nframes] = params[:4]
    str_data = f.readframes(nframes)
    f.close()
    data = np.fromstring(str_data, dtype=np.short)
    return data, nframes, framerate

if __name__ == "__main__":
    txt = open("msg.txt")
    a = txt.read()
    print(a)
    b = str2code(a)
    for c in b:
        print(c,end=' ')
    txt.close()