from socket import *
import pymysql
from getpass import getpass
import sys

class OnlineDictClient():
    def __init__(self):
        self.ADDR=("127.0.0.1",5200) #服务器地址
        self.socketclient=socket()
        self.socketclient.connect(self.ADDR)
    # 主界面
    def mian(self):
        while True:
            print("""
            =======Online Dict=======
                1.注册 2.登录 3.退出
            =========================""")
            cmd=input("输入选项:")
            if cmd not in ("1","2","3"):
                print("请输入正确选项！")
                continue
            # 直接将选项作为请求格式，避免再次拟定发送格式
            if cmd=="1": # 注册
                self.regist()
            elif cmd=="2": # 登录
                self.login()
            elif cmd=="3": # 退出
                sys.exit("谢谢使用！")
    def regist(self):
        while True:
            name=input("请输入名称：")
            pwd=input("请输入密码：")
            pwdc=input("请再次确认密码：")
            # pwd=getpass()
            # pwdc=getpass("Again:")
            if pwd!=pwdc:
                print("输入密码不一致")
                continue
            if " " in name or " " in pwd:
                print("输入用户名或密码不合法，包含空格")
                continue
            s="R %s %s"%(name,pwd)
            self.socketclient.send(s.encode())
            confirm=self.socketclient.recv(1024)
            if confirm==b"OK":
                print("注册成功")
                break
            else:
                print("注册失败，用户名已存在！")
    def login(self):
        while True:
            # print("""
            # =======Online Dict=======
            #        用户登录界面
            # =========================
            # """)
            name = input("请输入您的名称：")
            pwd = input("请输入您的密码：")
            s="L %s %s"%(name,pwd)
            self.socketclient.send(s.encode())
            info_cfrm=self.socketclient.recv(1024)
            if info_cfrm==b"OK":
                print("恭喜登陆成功！")
                self.dict(name)
                break
            else:
                print("用户名或密码错误，请重新输入！")
    # 二级界面
    def dict(self,name):
        print("""
         =======Online Dict=======
               1.英语单词查询
               2.历史记录查看
               3.注销
         =========================
        """)
        cmd=input("请输入选项：")
        if cmd == "1":  # 查询
            self.search(name)
        elif cmd == "2":  # 历史记录
            self.history(name)
        elif cmd == "3":  # 退出
            return
    def search(self,name):
        self.socketclient.send(("S %s"%name).encode())
        while True:
            word =input("请输入查询单词：")
            if not word:
                self.socketclient.send(b"EXIT")
                break
            self.socketclient.send(word.encode())
            explain=self.socketclient.recv(1024)
            if explain==b"404":
                print("无此单词")
            else:
                print(explain.decode())
    def history(self,name):
        pass
if __name__=="__main__":
    client=OnlineDictClient()
    client.mian()
