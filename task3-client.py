# 导入 socket、sys 模块
import socket
import sys
import datetime
import matplotlib.pyplot as plt
from record import record_file
from utils import *
# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# 获取本地主机名
host = '192.168.0.105'

# 设置端口号
port = 10002

# 连接服务，指定主机和端口
s.connect((host, port))
time3 = record_file(5,'recv.wav',True)
# 接收小于 1024 字节的数据
time1 = s.recv(1024)
s.close()
data, nframes, framerate = open_wave_file('recv.wav')
plt.plot(data)
plt.show()

print (time1.decode('utf-8'))
print(float(time3)-float(time1.decode('utf-8').replace('\r\n','')))