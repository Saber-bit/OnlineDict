import pymysql
import hashlib
class DataBase():
    # 初始化，连接数据库
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
    # 密码加密，hashlib模块MD5处理密码
    def secret(self,pwd):
        hash=hashlib.md5("salt**来干小日本！".encode())
        hash.update(pwd.encode())
        return hash.hexdigest()
    # 用户注册，数据库写操作-->table user:name password
    def register(self, name, pwd):
        # 对密码进行加密处理
        pwd=self.secret(pwd)
        # 判断是否存在该用户名
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
    # 用户登录，数据库读操作<--select from user
    def login(self,name,pwd):
        pwd = self.secret(pwd)
        sql="select * from user where name='%s' and password='%s'"%(name,pwd)
        self.cur.execute(sql)
        if self.cur.fetchone():
            return True
        else:
            return False
    # 用户查询，插入查询name,word和time-->history
    def inserthistory(self,name,word):
        sql="insert into history (name,word) values ('%s','%s')"%(name,word)
        try:
            self.cur.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
    # 用户查询,记录，读单词解释<--select words:explain
    def search(self,name,word):
        self.inserthistory(name,word)
        sql = "select wordexplain from words where word='%s'" % word
        self.cur.execute(sql)
        # 返回结果为元组
        explain=self.cur.fetchone()
        if explain:
            return explain[0]
    # 历史记录查看，返回最近10条记录
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