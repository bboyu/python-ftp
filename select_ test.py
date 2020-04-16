"""
select 函数示例
"""

from select import select
from socket import *
from time import sleep

s = socket()
s.bind(('127.0.0.1', 8888))
s.listen(3)

f = open('net.log', 'r+')

# 两个IO对象  -->  s    f
print("开始监控IO")
sleep(5)
rs, ws, xs = select([s], [f], [])
print("rlist:", rs)
print("wlist:", ws)
print("xlist:", xs)
