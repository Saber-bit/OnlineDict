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
        self.port=5200
        self.ip="127.0.0.1"
        self.ADDR=(self.ip,self.port) #服务器地址
        self.socketfd=socket()
        self.socketfd.bind(self.ADDR)
        self.socketfd.listen(5)
        print("Listen from port:%d"%self.port)
        self.socketfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        signal(SIGCHLD,SIG_IGN)
    # 循环监听，分配子进程
    def main(self):
        print("")
        while True:
            try:
                conn,addr=self.socketfd.accept()
                print("connect from",addr)
            except Exception:
                print("服务器退出！")
            self.p=Handle(conn,self.db)
            self.p.start()
class Handle(Process):
    def __init__(self,conn,db):
        self.conn=conn
        self.db=db
        super().__init__()
    # 子进程处理主逻辑，解析客户端请求内容
    def run(self):
        while True:
            request=self.conn.recv(1024).decode()
            if not request or request[0]=="E":
                sys.exit(0)
            elif request[0] == "R":
                self.regist(request)
            elif request[0] == "L":
                self.login(request)
            elif request[0]=="S":
                self.search(request)
            elif request[0] == "H":
                self.history(request)
    # 用户注册逻辑处理
    def regist(self, request):
        name=request.split(" ")[1]
        pwd=request.split(" ")[-1]
        if self.db.register(name,pwd):
            self.conn.send(b"OK")
        else:
            self.conn.send(b"name exist")
    # 用户登录逻辑处理
    def login(self,info_log):
        name = info_log.split(" ")[1]
        pwd = info_log.split(" ")[-1]
        if self.db.login(name,pwd):
            self.conn.send(b"OK")
        else:
            self.conn.send(b"incorrect")
    # 用户查询字典逻辑处理
    def search(self,request):
        name=request.split(" ")[-1]
        while True:
            word=self.conn.recv(1024).decode()
            if word=="EXIT":
                break
            explain=self.db.search(name,word)
            if explain:
                self.conn.send(explain.encode())
            else:
                self.conn.send(b"404")
    # 用户查看历史记录逻辑处理
    def history(self,request):
        name=request.split(" ")[-1]
        records=self.db.history(name)
        if records:
            self.conn.send(records.encode())
        else:
            self.conn.send(("%s have no search history"%name).encode())
if __name__=="__main__":
    server=OnlineDictServer()
    server.main()



