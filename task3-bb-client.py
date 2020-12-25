import datetime
import multiprocessing
import socket
import time
import matplotlib.pyplot as plt
import pyaudio

from record import record_file
from utils import *

CHUNK = 1024
time1 = 0
time2 = 0
time3 = 0
time_start_record = 0



def pyaudioplay(q):
    wf = wave.open('getdistance.wav', 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    time.sleep(1)
    time1 = datetime.datetime.timestamp(datetime.datetime.now())
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()
    q.put(time1)


def pyaudiorecord(q):
    global time_start_record
    time_start_record = record_file(3, 'recv.wav', True)
    q.put(time_start_record)


def get_first_impulse(command,time_start_record):
    sig_rec, nframes, framerate = open_wave_file('recv.wav')

    f = 6000
    fs = 48000
    duration = 0.0125
    symbol_len = int(duration * fs)
    pre_threshold = 0.6
    max_symbol_sum = 0
    first_impulse = 0  # 取出impulse 第一个起始位置
    for i in range(0, len(sig_rec) - symbol_len):
        symbol_sum = np.sum(np.abs(sig_rec[i:i + symbol_len]))
        if symbol_sum > max_symbol_sum:
            max_symbol_sum = symbol_sum
        # print(max_symbol_sum)
    for i in range(0, len(sig_rec) - symbol_len):
        symbol_sum = np.sum(np.abs(sig_rec[i:i + symbol_len]))
        if symbol_sum > pre_threshold * max_symbol_sum:
            max_sum = symbol_sum
            for j in range(i - int(symbol_len / 2), i + int(symbol_len)):
                now_sum = np.sum(np.abs(sig_rec[j:j + symbol_len]))
                if now_sum > max_sum:
                    max_sum = now_sum
                    first_impulse = j
            break
    window = int(symbol_len)  # 窗口长度为采样点个数
    impulse_fft = np.zeros(window * 50)  # 定义变量数组impulse_fft，用于存储每个时刻对应的数据段中声音信号的强度
    sig_rec = sig_rec[first_impulse - symbol_len:first_impulse + symbol_len]
    for i in range(0, window * 5):
        y = abs(np.fft.fft(sig_rec[i:i + window]))
        index_impulse = round(f / fs * window)
        # 考虑到声音通信过程中的频率偏移，我们取以目标频率为中心的5个频率采样点中最大的一个来代表目标频率的强度
        impulse_fft[i] = max(y[index_impulse - 2:index_impulse + 2])
    impulse_fft = impulse_fft / max(impulse_fft)  # 幅值归一化
    max_impulse = max(impulse_fft)
    real_first_impulse = symbol_len
    for i in range(len(impulse_fft)):
        if impulse_fft == max_impulse:
            real_first_impulse = i
            break
    real_first_impulse = first_impulse-symbol_len + real_first_impulse
    print(real_first_impulse)
    print(first_impulse)
    if command == "send":
        global time2
        time2 = time_start_record + real_first_impulse / fs
    else:
        global time3
        time3 = time_start_record + real_first_impulse / fs


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = '192.168.0.101'
    # 设置端口号
    port = 20002
    # 连接服务，指定主机和端口
    s.connect((host, port))
    time_start_record = record_file(3, 'recv.wav', True)
    get_first_impulse("recv",time_start_record)

    msg = str(1) + "\r\n"
    s.send(msg.encode('utf-8'))
    s.recv(1024)

    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    thread1 = multiprocessing.Process(target=pyaudioplay,args=(q1,))
    thread2 = multiprocessing.Process(target=pyaudiorecord,args=(q2,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    time1=q1.get(True)
    time_start_record=q2.get(True)
    get_first_impulse("send",time_start_record)

    msg = str(time1)+" "+str(time2)+" "+str(time3)+ "\r\n"
    s.send(msg.encode('utf-8'))
