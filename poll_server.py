"""
poll实现并发服务
"""

from select import *
from socket import *

# 创建监听套接字作为关注的IO对象
s = socket()
s.bind(('0.0.0.0',8888))
s.listen(3)

# 设置为非阻塞
s.setblocking(False)

# 查找字典   通过文件描述符 --> 查找IO对象  必须时刻与regiser的IO保持一致
fdmap = {s.fileno():s}

# 创建poll对象
p = poll()
# 设置关注列表
p.register(s,POLLIN) # 初始关注监听套接字的读


while True:
    # 对IO进行监控   [(fileno,event),(),()]
    events = p.poll()
    print(events)
    # 遍历列表分情况讨论
    for fd,event in events:
        if fd == s.fileno():
            # 监听套接字就绪  通过字典找io对象
            c, addr = fdmap[fd].accept()
            print("Connect from", addr)
            # 添加客户端链接套接字作为监控对象
            c.setblocking(False)
            p.register(c,POLLIN)    # 增加关注的IO
            fdmap[c.fileno()] = c  # 字典随之维护
        else:
            # 客户端链接套接字就绪
            data = fdmap[fd].recv(1024).decode()
            if not data:
                # 客户端退出
                p.unregister(fd)  # 移除关注
                fdmap[fd].close()
                del fdmap[fd]
                continue
            print(data)
            fdmap[fd].send(b'OK')