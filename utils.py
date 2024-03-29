# -*- coding:utf-8 -*-
import wave
import numpy as np
import pandas as pd
import csv
from scipy import signal


def encode(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])


def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])


def str2code(msg):
    code = []
    for c in msg:
        encode_c = encode(c)
        while (len(encode_c) < 8):
            encode_c = '0' + encode_c
        for i in encode_c:
            code.append(int(i))
    return code


def int2code(num):
    code = []
    num_bin = bin(num)[2:]
    for c in num_bin:
        code.append(int(c))
    while len(code) < 8:
        code = [0] + code
    return code


def code2int(code):
    num_int = 0
    for i in range(8):
        num_int += int(code[i]) * 2**(7-i)
    return num_int


def code2str(code):
    msg = ''
    for i in range(0, len(code), 8):
        if i + 8 > len(code):
            break
        c = ''
        for j in range(i, i + 8):
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


def parse_csv(filename="content.csv", need_payload=False):
    data = pd.read_csv(filename, skiprows=4, sep=",")
    if not need_payload:
        return data["onset"].tolist()
    payload = data.iloc[:, 4:]
    payload = np.array(payload)
    payload_formatted = []
    for _ in payload:
        payload_formatted.append(_[~pd.isnull(_)].tolist())
    return payload_formatted


def write_ans_to_csv(data, filename="res.csv"):
    with open(filename, 'w', newline="") as f:
        csv_writer = csv.writer(f)
        for row in data:
            csv_writer.writerow(row)


if __name__ == "__main__":
    data = parse_csv(need_payload=False)
    print(data)
    write_ans_to_csv(data)
