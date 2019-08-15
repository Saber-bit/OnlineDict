from socket import *
import pymysql
from multiprocessing import *
from signal import *
from dboperate import  *
import sys
class OnlineDictServer():
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
        # signal(SO,SIG_IGN)
    def main(self):
        while True:
            try:
                conn,addr=self.socketfd.accept()
                print("connect from",addr)
            except Exception:
                print("服务器退出！")
            client=Process(target=self.handle,args=(conn,))
            client.start()
    def handle(self,client):
        while True:
            request=client.recv(1024).decode()
            if not request[0] or request[0]=="E":
                sys.exit(0)
            elif request[0] == "R":
                self.regist(client,request)
            elif request[0] == "L":
                self.login(client,request)
            elif request[0]=="S":
                self.search(client,request)
            elif request[0] == "H":
                self.history(client,request)
    def regist(self, client,request):
        name=request.split(" ")[1]
        pwd=request.split(" ")[-1]
        if self.db.register(name,pwd):
            client.send(b"OK")
        else:
            client.send(b"name exist")
    def login(self,client,info_log):
        name = info_log.split(" ")[1]
        pwd = info_log.split(" ")[-1]
        print(name,pwd)
        if self.db.login(name,pwd):
            client.send(b"OK")
        else:
            client.send(b"incorrect")
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
    def history(self,client,request):
        name=request.split(" ")[-1]

if __name__=="__main__":
    server=OnlineDictServer()
    server.main()



