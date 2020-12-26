# 导入 socket、sys 模块
import socket
import sys
import datetime
import wave
import pyaudio
CHUNK = 1024

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



def pyaudioplay():
    wf = wave.open('getdistance.wav', 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
    data = wf.readframes(CHUNK)
    flag = True
    time1 = 0
    while len(data) > 0:
        if flag:
            time1 = datetime.datetime.timestamp(datetime.datetime.now())
            flag = False
        stream.write(data)
        data = wf.readframes(CHUNK)
    time2 = datetime.datetime.timestamp(datetime.datetime.now())
    stream.stop_stream()
    stream.close()
    p.terminate()
    return time1,time2

while True:
    # 建立客户端连接
    from playsound import playsound
    import time
    clientsocket,addr = serversocket.accept()
    time.sleep(1)
    time1, time2 = pyaudioplay()
    print(time2 - time1)
    msg = str(time2) + "\r\n"
    clientsocket.send(msg.encode('utf-8'))
    clientsocket.close()
    break