import datetime
import multiprocessing
import socket
import time

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
    time_00 = datetime.datetime.timestamp(datetime.datetime.now())
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    time_01 = datetime.datetime.timestamp(datetime.datetime.now())
    print(time_01, time_00)
    data = wf.readframes(CHUNK)
    time.sleep(1)
    global time1
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
    time_start_record = record_file(4, 'recv.wav', True)
    q.put(time_start_record)


def get_first_impulse(command, time_start_record):
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
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    clientsocket, addr = serversocket.accept()
    time_start=time.time()

    thread1 = multiprocessing.Process(target=pyaudioplay,args=(q1,))
    thread2 = multiprocessing.Process(target=pyaudiorecord,args=(q2,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    time1=q1.get(True)
    time_start_record=q2.get(True)
    get_first_impulse("send",time_start_record)

    clientsocket.recv(1024)
    msg = str(1) + "\r\n"
    clientsocket.send(msg.encode('utf-8'))
    time.sleep(1)
    time_start_record = record_file(4, 'recv.wav', True)
    get_first_impulse("recv",time_start_record)

    client_time = clientsocket.recv(1024)
    client_time = client_time.decode("utf-8").replace("\r\n", "")
    client_time = client_time.split(" ")
    print(client_time)
    print(time1,time2,time3)
    time_end=time.time()
    print("Total time:"+str(time_end-time_start))
    dis = 340.0/2.0*( float(time3)-float(time2)- float(client_time[1]) + float(client_time[2]) )
    print(dis)

