import MySQLdb as my
import os

host = os.environ.get('HOST')
dbname = os.environ.get('DB')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')


db = my.connect(host, user, password)
cursor = db.cursor()
sql = "CREATE DATABASE " + dbname
cursor.execute(sql)
db.close()
db = my.connect(host, user, password, dbname)
cursor = db.cursor()
sql = """CREATE TABLE test.user (
        USER_ID  INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        FIRST_NAME CHAR(20),
        LAST_NAME CHAR(20),
        USER_NAME CHAR(20) NOT NULL,
        PASSWORD VARCHAR(100) NOT NULL,
        EMAIL VARCHAR(100) NOT NULL) """
cursor.execute(sql)

db.close()

