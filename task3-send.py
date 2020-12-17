# 导入 socket、sys 模块
import socket
import sys
import datetime
import pyaudio
import wave
# 创建 socket 对象
serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM) 

# 获取本地主机名
host = socket.gethostname()

port = 10002

# 绑定端口号
serversocket.bind((host, port))

# 设置最大连接数，超过后排队
serversocket.listen(5)

while True:
    # 建立客户端连接
    clientsocket,addr = serversocket.accept()    
    msg = str(datetime.datetime.timestamp(datetime.datetime.now())) + "\r\n"
    clientsocket.send(msg.encode('utf-8'))
    clientsocket.close()
    print("连接地址: %s" % str(addr))