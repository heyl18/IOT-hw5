from utils import open_wave_file, code2str, code2int, parse_csv, write_ans_to_csv
from record import record_file
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

f = 4000
fs = 48000
duration = 0.025
symbol_len = int(duration * fs)
size_data_len = 8
pre_data_len = 20
threshold = 0.6


def decode_wave(sig_rec):
    window = int(symbol_len)  # 窗口长度为采样点个数
    half_window = int(symbol_len / 2)
    impulse_fft = np.zeros(window * 50)  # 定义变量数组impulse_fft，用于存储每个时刻对应的数据段中声音信号的强度
    for i in range(0, window * 50):
        y = abs(np.fft.fft(sig_rec[i:i + window]))
        index_impulse = round(f / fs * window)
        # 考虑到声音通信过程中的频率偏移，我们取以目标频率为中心的5个频率采样点中最大的一个来代表目标频率的强度
        impulse_fft[i] = max(y[index_impulse - 2:index_impulse + 2])
    impulse_fft = impulse_fft / max(impulse_fft)  # 幅值归一化
    # plt.plot(impulse_fft)
    # plt.show()
    first_impulse = 0  # 取出impulse 第一个起始位置
    header_data = []
    size_data = []
    for i in range(0, pre_data_len):
        if first_impulse + i * window >= len(impulse_fft):
            break
        header_data.append(0 if impulse_fft[first_impulse + i * window] > threshold else 1)
    if header_data != [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]:
        return 0, None
    for i in range(pre_data_len, pre_data_len + size_data_len):
        if first_impulse + i * window >= len(impulse_fft):
            break
        size_data.append(0 if impulse_fft[first_impulse + i * window] > threshold else 1)
    size = code2int(size_data)
    if size <= 0 or size > 255:
        return 0, None
    impulse_fft = np.zeros(window * (size + 1))
    decode_data = []
    sig_rec = sig_rec[(size_data_len + pre_data_len) * window:(size_data_len + pre_data_len + size + 1) * window]
    for i in range(0, len(sig_rec) - window):
        y = abs(np.fft.fft(sig_rec[i:i + window]))
        index_impulse = round(f / fs * window)
        # 考虑到声音通信过程中的频率偏移，我们取以目标频率为中心的5个频率采样点中最大的一个来代表目标频率的强度
        impulse_fft[i] = max(y[index_impulse - 2:index_impulse + 2])
    impulse_fft = impulse_fft / max(impulse_fft)
    for i in range(0, size):
        if first_impulse + i * window >= len(impulse_fft):
            break
        decode_data.append(0 if impulse_fft[first_impulse + i * window] > threshold else 1)
    # string = code2str(decode_data)
    print(header_data)
    print(size_data)
    print(decode_data)
    return size, decode_data


def decode(filename='recordfile.wav', debug=False):
    '''
    描述：对接收到的音频文件进行解码，返回相关信息
    输入：音频路径
    返回：size：编码长度，string：解码出的字符串
    '''
    sig_rec, nframes, framerate = open_wave_file(filename)
    sig_rec=np.concatenate((sig_rec,np.zeros(symbol_len*2)))
    # b, a = signal.butter(8, [2*4000*0.9/48000,2*6000*1.1/48000], 'bandpass')
    # sig_rec = signal.filtfilt(b, a, sig_rec)

    onset = parse_csv(filename="content.csv")
    payload = []
    if debug:
        payload = parse_csv(need_payload=True)
    ans = []
    count = 0
    totalBytes=0
    errorBytes=0
    errorCount=0
    for i in onset:
        size, decode_data = decode_wave(sig_rec[i:])
        ans.append([size])
        for _ in decode_data:
            ans[-1].append(_)
        if debug:
            totalBytes+=len(decode_data)
            for j in range(len(decode_data)):
                errorBytes+=np.abs(payload[count][j]-decode_data[j])
            flag=(payload[count] == decode_data)
            errorCount+=int(not flag)
            print(flag)
            count += 1
    print("丢包率："+str(errorCount/count))
    print("比特错误率："+str(errorBytes/totalBytes))
    write_ans_to_csv(ans)


if __name__ == '__main__':
    decode('res.wav',debug=True)
    # size, string = decode('res.wav')
    # if(size != 0 and string != None):
    #     print('length: %d' % int(size/8),string)
