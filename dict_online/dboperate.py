import pymysql
import hashlib
class DataBase():
    def __init__(self):
        self.db=pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123456",
            database="dict",
            charset='utf8' )
        # 游标
        self.cur = self.db.cursor()
    def secret(self,pwd):
        hash=hashlib.md5("salt**来干小日本！".encode())
        hash.update(pwd.encode())
        return hash.hexdigest()
    def register(self, name, pwd):
        # 对密码进行加密处理
        pwd=self.secret(pwd)
        sql = "select name from user where name='%s';" % name
        self.cur.execute(sql)
        if self.cur.fetchone():
            return False
        # 插入记录
        try:
            sql = "insert into user (name,password) values ('%s','%s')" % (name, pwd)
            self.cur.execute(sql)
            # 写操作
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
    def login(self,name,pwd):
        pwd = self.secret(pwd)
        sql="select * from user where name='%s' and password='%s'"%(name,pwd)
        self.cur.execute(sql)
        if self.cur.fetchone():
            return True
        else:
            return False
    def inserthistory(self,name,word):
        sql="insert into history (name,word) values ('%s','%s')"%(name,word)
        try:
            self.cur.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
    def search(self,name,word):
        self.inserthistory(name,word)
        sql = "select wordexplain from words where word='%s'" % word
        self.cur.execute(sql)
        # 返回结果为元组
        explain=self.cur.fetchone()
        if explain:
            return explain[0]
    def history(self,name):
        sql = "select * from history where name=%s order by searchtime desc limit 10"
        self.cur.execute(sql,[name])
        records=self.cur.fetchall()
        str_=""
        for record in records:
            str_+=(str(record)+"\n")
        return str_
if __name__=="__main__":
    db=DataBase()
    res=db.history("lei")
    print(res)