from utils import open_wave_file, code2str, code2int
from record import record_file
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import sys

f = 6000
fs = 48000
duration = 0.0125
symbol_len = int(duration * fs)
size_data_len = 8
pre_data_len = 10
threshold = 0.5

def decode_wave(sig_rec):
    window = int(symbol_len)  # 窗口长度为采样点个数
    half_window = int(symbol_len/2)
    impulse_fft = np.zeros(window * 50)  # 定义变量数组impulse_fft，用于存储每个时刻对应的数据段中声音信号的强度
    for i in range(0,window * 50):
        y = abs(np.fft.fft(sig_rec[i:i+window]))
        index_impulse = round(f/fs*window)
        # 考虑到声音通信过程中的频率偏移，我们取以目标频率为中心的5个频率采样点中最大的一个来代表目标频率的强度
        impulse_fft[i] = max(y[index_impulse-2:index_impulse+2])
    impulse_fft = impulse_fft/max(impulse_fft)  # 幅值归一化
    plt.plot(impulse_fft)
    plt.show()
    first_impulse = 0  # 取出impulse 第一个起始位置
    header_data = []
    size_data = []
    for i in range(0,pre_data_len):
        if first_impulse + i*window >= len(impulse_fft):
            break
        header_data.append(1 if impulse_fft[first_impulse+i*window] > threshold else 0)
    if(header_data != [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]):
        return 0, None
    for i in range(pre_data_len,pre_data_len+size_data_len):
        if first_impulse + i*window >= len(impulse_fft):
            break
        size_data.append(1 if impulse_fft[first_impulse+i*window] > threshold else 0)
    size = code2int(size_data)
    if size <= 0 or size > 255:
        return 0,None
    impulse_fft = np.zeros(window*(size+1))
    decode_data =[]
    sig_rec = sig_rec[(size_data_len + pre_data_len) * window:(size_data_len + pre_data_len + size) * window]
    for i in range(0,len(sig_rec)-window):
        y = abs(np.fft.fft(sig_rec[i:i+window]))
        index_impulse = round(f/fs*window)
        # 考虑到声音通信过程中的频率偏移，我们取以目标频率为中心的5个频率采样点中最大的一个来代表目标频率的强度
        impulse_fft[i] = max(y[index_impulse-2:index_impulse+2])
    impulse_fft = impulse_fft/max(impulse_fft)
    # plt.plot(impulse_fft)
    # plt.show()
    for i in range(0,size):
        if first_impulse + i*window >= len(impulse_fft):
            break
        decode_data.append(1 if impulse_fft[first_impulse+i*window] > threshold else 0)
    # string = code2str(decode_data)
    print(header_data)
    print(size_data)
    print(decode_data)
    return size, decode_data
def decode(filename = 'recordfile.wav'):
    '''
    描述：对接收到的音频文件进行解码，返回相关信息
    输入：音频路径
    返回：size：编码长度，string：解码出的字符串
    '''
    sig_rec, nframes, framerate = open_wave_file(filename)

    max_symbol_sum = 0
    first_impulse = 0  # 取出impulse 第一个起始位置

    for i in range(0,len(sig_rec)-symbol_len):
        symbol_sum = np.sum(np.abs(sig_rec[i:i+symbol_len]))
        if symbol_sum > max_symbol_sum:
            max_symbol_sum = symbol_sum
    for i in range(0,len(sig_rec)-symbol_len):
        symbol_sum = np.sum(np.abs(sig_rec[i:i+symbol_len]))
        if symbol_sum > 0.8*max_symbol_sum:
            max_sum = symbol_sum
            for j in range(i-int(symbol_len/2),i+int(symbol_len)):
                now_sum = np.sum(np.abs(sig_rec[j:j+symbol_len]))
                if now_sum > max_sum:
                    max_sum = now_sum
                    first_impluse = j
            break
    print(first_impulse)
    onset = [first_impulse]
    for i in onset:
        size, decode_data = decode_wave(sig_rec[i:])
        print(size, decode_data)

if __name__ == '__main__':
    seconds = int(sys.argv[1])
    record_file(seconds,"recordfile.wav")
    size, string = decode('recordfile.wav')
    if(size != 0 and string != None):
        print('length: %d' % int(size/8),string)