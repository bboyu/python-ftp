"""
【1】将关注的IO准备好，通常设置为非阻塞状态。

【2】通过IO多路复用方法提交，进行IO监控。

【3】阻塞等待，当监控的IO有发生时，结束阻塞。

【4】遍历返回值列表，确定就绪IO事件。

【5】处理发生的IO事件。

【6】继续循环监控IO发生。

重点代码
"""
from select import select
from socket import *

# 创建监听套接字作为关注的IO对象
s = socket()
s.bind(('0.0.0.0',8888))
s.listen(3)

# 设置为非阻塞
s.setblocking(False)
#一般网络IO才会设置成非阻塞，因为考虑到延迟，这样不会影响到其他IO的监控

# 设置关注列表
rlist = [s] # 初始关注监听套接字的读
wlist = []
xlist = []


while True:
    # 对IO进行监控
    rs,ws,xs = select(rlist,wlist,xlist)

    # 遍历列表分情况讨论
    for r in rs:
        if r is s:
            # 监听套接字就绪
            c, addr = r.accept()
            print("Connect from", addr)
            # 添加客户端链接套接字作为监控对象
            c.setblocking(False)
            rlist.append(c)
        else:
            # 客户端链接套接字就绪
            data = r.recv(1024).decode()
            if not data:
                # 客户端退出
                rlist.remove(r)  # 移除关注
                r.close()
                continue
            print(data)
            # r.send(b'OK')
            wlist.append(r) # 加入到写关注列表

    for w in ws:
        w.send(b'OK')
        wlist.remove(w)

    for x in xs:
        pass














