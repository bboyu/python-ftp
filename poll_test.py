"""
poll方法示例
"""

from select import *
from socket import *
from time import sleep

s = socket()
s.bind(('127.0.0.1', 8888))
s.listen(3)

f = open('net.log', 'r+')
print(f.fileno())

# 查找字典   通过文件描述符 --> 查找IO对象
fdmap = {s.fileno(): s, f.fileno(): f}

sleep(3)

# 创建对象
poll = poll()
poll.register(s, POLLIN)
poll.register(f, POLLIN | POLLOUT)

# 提交监控IO发生
events = poll.poll()  # 【poll（）是poll对象的属性方法】
print(events)  # [(4, 5)]  #4表示文件描述符，5表示对应的就绪事件类型
               # POLLIN是1，POLLOUT是4，5表示两个都就绪（4+1）
