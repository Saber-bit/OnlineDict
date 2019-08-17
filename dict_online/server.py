from socket import *
import pymysql
from multiprocessing import *
from signal import *
from db_operate import  *
import sys
class OnlineDictServer():
    # 数据库对象，监听套接字初始化
    def __init__(self):
        # 数据库对象调用
        self.db=DataBase()
        # 套接字初始化
        self.ADDR=("127.0.0.1",5200) #服务器地址
        self.socketfd=socket()
        self.socketfd=socket()
        self.socketfd.bind(self.ADDR)
        self.socketfd.listen(5)
        self.socketfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        signal(SIGCHLD,SIG_IGN)
    # 循环监听，分配子进程
    def main(self):
        while True:
            try:
                conn,addr=self.socketfd.accept()
                print("connect from",addr)
            except Exception:
                print("服务器退出！")
            client=Process(target=self.handle,args=(conn,))
            client.start()
    # 子进程处理主逻辑，解析客户端请求内容
    def handle(self,client):
        while True:
            request=client.recv(1024).decode()
            if not request or request[0]=="E":
                sys.exit(0)
            elif request[0] == "R":
                self.regist(client,request)
            elif request[0] == "L":
                self.login(client,request)
            elif request[0]=="S":
                self.search(client,request)
            elif request[0] == "H":
                self.history(client,request)
    # 用户注册逻辑处理
    def regist(self, client,request):
        name=request.split(" ")[1]
        pwd=request.split(" ")[-1]
        if self.db.register(name,pwd):
            client.send(b"OK")
        else:
            client.send(b"name exist")
    # 用户登录逻辑处理
    def login(self,client,info_log):
        name = info_log.split(" ")[1]
        pwd = info_log.split(" ")[-1]
        print(name,pwd)
        if self.db.login(name,pwd):
            client.send(b"OK")
        else:
            client.send(b"incorrect")
    # 用户查询字典逻辑处理
    def search(self,client,request):
        name=request.split(" ")[-1]
        while True:
            word=client.recv(1024).decode()
            if word=="EXIT":
                break
            explain=self.db.search(name,word)
            if explain:
                client.send(explain.encode())
            else:
                client.send(b"404")
    # 用户查看历史记录逻辑处理
    def history(self,client,request):
        name=request.split(" ")[-1]
        records=self.db.history(name)
        if records:
            client.send(records.encode())
        else:
            client.send(("%s have no search history"%name).encode())
if __name__=="__main__":
    server=OnlineDictServer()
    server.main()



