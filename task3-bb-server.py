import socket
import sys
import datetime
import matplotlib.pyplot as plt
from record import record_file
from utils import *
import pyaudio
import threading
import time
import multiprocessing

CHUNK = 1024
time1 = 0
time2 = 0
time3 = 0
time_start_record = 0



def pyaudioplay():
    wf = wave.open('getdistance.wav', 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    time.sleep(1)
    flag = True
    while len(data) > 0:
        if flag:
            global time1
            time1 = datetime.datetime.timestamp(datetime.datetime.now())
            flag = False
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()



def pyaudiorecord():
    global time_start_record
    time_start_record = record_file(3, 'recv.wav', True)


def get_first_impulse(command):
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
    if command == "send":
        global time2
        time2 = time_start_record + first_impulse / fs
    else:
        global time3
        time3 = time_start_record + first_impulse / fs


if __name__ == "__main__":
    # 创建 socket 对象
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = '0.0.0.0'
    port = 20002
    # 绑定端口号
    serversocket.bind((host, port))
    # 设置最大连接数，超过后排队
    serversocket.listen(5)

    clientsocket, addr = serversocket.accept()

    thread1 = multiprocessing.Process(target=pyaudioplay)
    thread2 = multiprocessing.Process(target=pyaudiorecord)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    get_first_impulse("send")

    clientsocket.recv(1024)
    msg = str(1) + "\r\n"
    clientsocket.send(msg.encode('utf-8'))

    pyaudiorecord()
    get_first_impulse("recv")

    client_time=clientsocket.recv(1024)
    client_time=client_time.decode("utf-8").replace("\r\n","")
    client_time=client_time.split(" ")