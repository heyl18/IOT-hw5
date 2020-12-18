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
host = '192.168.0.102'

# 设置端口号
port = 20002

# 连接服务，指定主机和端口
s.connect((host, port))
time3 = record_file(2,'recv.wav',True)
# 接收小于 1024 字节的数据
time2 = s.recv(1024)
s.close()
sig_rec, nframes, framerate = open_wave_file('recv.wav')
# plt.plot(sig_rec)
# plt.show()
f = 6000
fs = 48000
duration = 0.0125
symbol_len = int(duration * fs)
size_data_len = 8
pre_data_len = 10
pre_threshold = 0.6
max_symbol_sum = 0
first_impulse = 0  # 取出impulse 第一个起始位置
for i in range(0, len(sig_rec) - symbol_len):
    symbol_sum = np.sum(np.abs(sig_rec[i:i + symbol_len]))
    if symbol_sum > max_symbol_sum:
        max_symbol_sum = symbol_sum
    #print(max_symbol_sum)
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
print (first_impulse)
print(float(time3)-float(time2.decode('utf-8').replace('\r\n','')) + float(first_impulse/fs)-0.274 + 1)
print((float(time3)-float(time2.decode('utf-8').replace('\r\n','')) + float(first_impulse/fs)-0.274 + 1)*340*100)