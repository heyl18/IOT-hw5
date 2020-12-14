from utils import open_wave_file, code2str, code2int
from record import record_file
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

f = 1800
fs = 48000
symbol_len = 512
alias = 2000
def decode(filename = 'recordfile.wav'):
    '''
    描述：对接收到的音频文件进行解码，返回相关信息
    输入：音频路径
    返回：size：编码长度，string：解码出的字符串
    '''
    sig_rec, nframes, framerate = open_wave_file(filename)
    b, a = signal.butter(8, 0.125, 'lowpass')
    sig_rec = signal.filtfilt(b, a, sig_rec)
    
    base_sig = []
    for i in range(alias, len(sig_rec), symbol_len):
        smb = sig_rec[i:i+symbol_len]
        base_sig.extend(smb)

    n = len(sig_rec)
    window = int(symbol_len)  # 窗口长度为采样点个数
    half_window = int(symbol_len/2)
    impulse_fft = np.zeros(n)  # 定义变量数组impulse_fft，用于存储每个时刻对应的数据段中声音信号的强度
    for i in range(0, n-window):
        y = abs(np.fft.fft(sig_rec[i:i+window]))
        index_impulse = round(f/fs*window)
        # 考虑到声音通信过程中的频率偏移，我们取以目标频率为中心的5个频率采样点中最大的一个来代表目标频率的强度
        impulse_fft[i] = max(y[index_impulse-2:index_impulse+2])
    impulse_fft = impulse_fft/max(impulse_fft)  # 幅值归一化
    plt.plot(impulse_fft)
    plt.show()
    first_impulse = 0  # 取出impulse 第一个起始位置
    for i in range(half_window+1, n - half_window):
        if impulse_fft[i] > 0.5 and impulse_fft[i] == max(impulse_fft[i-half_window:i+half_window]):
            first_impulse = i
            break
    # print(first_impulse)
    header_datas = []
    size_datas = []
    decode_datas =[]
    for i in range(0,6):
        if first_impulse + i*window >= len(impulse_fft):
            break
        header_datas.append(1 if impulse_fft[first_impulse+i*window] > 0.4 else 0)
    # if(header_datas != [1,0,1,0,1,0]):
    #     return 0, None
    for i in range(6,17):
        if first_impulse + i*window >= len(impulse_fft):
            break
        size_datas.append(1 if impulse_fft[first_impulse+i*window] > 0.4 else 0)
    size = code2int(size_datas)
    # if size <= 0 or size > 2048:
    #     return 0,None
    for i in range(17,17+size):
        if first_impulse + i*window >= len(impulse_fft):
            break
        decode_datas.append(1 if impulse_fft[first_impulse+i*window] > 0.4 else 0)
    string = code2str(decode_datas)
    print(header_datas)
    print(size_datas)
    print(decode_datas)
    return size, string

if __name__ == '__main__':
    record_file(10,"recordfile.wav")
    size, string = decode('recordfile.wav')
    if(size != 0 and string != None):
        print('length: %d' % int(size/8),string)