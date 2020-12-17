# 导入 socket、sys 模块
import socket
import sys
import datetime
# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# 获取本地主机名
host = socket.gethostname() 

# 设置端口号
port = 10002

# 连接服务，指定主机和端口
s.connect((host, port))

# 接收小于 1024 字节的数据
msg1 = datetime.datetime.timestamp(datetime.datetime.now())
msg = s.recv(1024)

s.close()

print (msg1 ,msg.decode('utf-8'))