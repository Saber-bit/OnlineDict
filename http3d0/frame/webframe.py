"""
模拟网站后端应用

从httpserver接收具体请求
根据请求进行逻辑处理和数据处理
将需要的数据反馈给httpserver
"""
from socket import *
import json
from setting import *
import os,sys
from select import select

# 应用类实现具体应用功能
class Application():
    def __init__(self):
        self.host = frame_host
        self.port = frame_port
        self.create_socket()
        self.bind()
    def create_socket(self):
        self.appfd=socket()
        self.appfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
    def bind(self):
        self.ADDR=(self.host,self.port)
        self.appfd.bind(self.ADDR)
        self.appfd.listen(5)
    def start(self):
        rlist,wlist,xlist=[self.appfd],[],[]
        while True:
            print("wait:",rlist)
            rs,ws,xs=select(rlist,wlist,xlist)
            print("OK:",rs)
            for rio in rs:
                if rio is self.appfd:# 就绪的rio是监听套接字
                    connfd,addr=rio.accept()
                    print("Connect from",addr)
                    rlist.append(connfd)
                else: # 就绪的为其他连接套接字
                    data=rio.recv(2048)
                    #处理逻辑


    pass
if __name__=="__main__":
    app=Application()
    app.start()