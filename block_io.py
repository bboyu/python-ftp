"""
非阻塞IO演示
套接字io --> 非阻塞
"""

from socket import *
from time import ctime,sleep


f = open('net.log','a+')  # 日志

# 创建tcp套接字
sockfd = socket()
sockfd.bind(('127.0.0.1',8888))
sockfd.listen(3)

# 设置套接字非阻塞
# sockfd.setblocking(False)

# 超时检测时间
sockfd.settimeout(2)

while True:
    print("Waiting for connect...")
    try:
        connfd,addr = sockfd.accept()  # 阻塞
        print("Connect from",addr)
    except timeout as e:
        f.write("%s : %s\n" % (ctime(), e))
        f.flush()
    except BlockingIOError as e:
        sleep(3)
        f.write("%s : %s\n"%(ctime(),e))
        f.flush()
    else:
        data = connfd.recv(1024)
        print(data)
