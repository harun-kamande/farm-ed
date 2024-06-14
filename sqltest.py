# import mysql.connector

# connection=mysql.connector.connect(
#     host='localhost',
#     user='root',
#     port=3307,
#     password='harunkamande',

# )

# cursor=connection.cursor()
# cursor.execute("DROP DATABASE hellos")
# cursor.close()
# connection.commit()

import sqlite3
connection=sqlite3.connect("users.db")
cursor=connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS userdetails(id INTEGER PRIMARY KEY,username TEXT,email TEXT UNIQUE,password TEXT)

''')
cursor.execute('''CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY,post TEXT, userid INTEGER,title TEXT, date TEXT, FOREIGN KEY(userid) REFERENCES userdetails(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS feedback(id INTEGER PRIMARY KEY,topic TEXT, concern TEXT, date TEXT, userid INTEGER, FOREIGN KEY(userid) REFERENCES userdatails(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS profilepic(id INTEGER PRIMARY KEY,photo TEXT,userid INTEGER, FOREIGN KEY(userid) REFERENCES userdetails(id))''')

cursor.close()
connection.commit()

import datetime
import time
times=datetime.datetime.now()
print(times.strftime("%B %d  %Y time %H:%M"))
