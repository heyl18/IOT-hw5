import time
import pyaudio
import socket
import datetime
from record import record_file
from utils import *
# 创建 socket 对象
fs = 48000
wf = wave.open('getdistance.wav', 'rb')

def pyaudioplay():
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    flag = True
    time1_now = 0
    while len(data) > 0:
        stream.write(data)
        if flag:
            time1_now = datetime.datetime.timestamp(datetime.datetime.now())
            flag = False
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return time1_now

def get_first_impulse():
    sig_rec, nframes, framerate = open_wave_file('recv.wav')
    duration = 0.0125
    symbol_len = int(duration * fs)
    pre_threshold = 0.6
    max_symbol_sum = 0
    first_impulse = 0  # 取出impulse 第一个起始位置
    for i in range(0, len(sig_rec) - symbol_len):
        symbol_sum = np.sum(np.abs(sig_rec[i:i + symbol_len]))
        if symbol_sum > max_symbol_sum:
            max_symbol_sum = symbol_sum
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
    print(first_impulse)
    return first_impulse


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取远程主机名
host = '192.168.0.107'
# 设置端口号
port = 20002
# 连接服务，指定主机和端口
s.connect((host, port))
timeB1 = record_file(4 ,'recv.wav', True)
impulse = get_first_impulse()
timeB2 = timeB1 + impulse/fs
msg = str(timeB2) + '\r\n'
s.send(msg)
# 接收小于 1024 字节的数据
begin = s.recv(1024)
time.sleep(1)
timeB3 = pyaudioplay()
msg = str(timeB3) + "\r\n"
s.send(timeB3)