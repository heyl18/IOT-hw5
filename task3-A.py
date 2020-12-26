# 导入 socket、sys 模块
import socket
from record import record_file
from utils import *
import datetime
import wave
import pyaudio
import time
CHUNK = 1024

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = '0.0.0.0'
fs = 48000
port = 20002
C = 340.0
# 绑定端口号
serversocket.bind((host, port))

# 设置最大连接数，超过后排队
serversocket.listen(5)
wf = wave.open('getdistance.wav', 'rb')

def get_first_impulse():
    sig_rec, nframes, framerate = open_wave_file('recv.wav')
    f = 6000

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
    print(first_impulse)
    return first_impulse

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


while True:
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()
    time.sleep(1)
    time_begin = time.time()
    timeA1 = pyaudioplay()
    timeB2 = float(clientsocket.recv(1024).decode('utf-8').replace('\r\n',''))
    msg = str("1") + "\r\n"
    clientsocket.send(msg.encode('utf-8'))

    timeA2 = record_file(4, 'recv.wav', True)
    timeB3 = float(clientsocket.recv(1024).decode('utf-8').replace('\r\n',''))
    clientsocket.close()
    impulse = get_first_impulse()
    timeA3 = timeA2 + impulse/fs
    dis_ab = C*(timeB2-timeA1)
    dis_ba = C*(timeA3-timeB3)
    print(dis_ab,dis_ba)
    dis = (dis_ab+dis_ba)/2.0
    print(dis)
    time_end = time.time()
    print(time_end-time_begin)
    break
