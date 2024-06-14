import mysql.connector




def get_db_connection():
    
    connection=mysql.connector.connect(
    host='localhost',
    user='root',
    database='farmed',
    port=3306,
    password='harunkamande',
    )
    return connection





# cursor.close()
# connection.commit()

# import sqlite3
# connection=sqlite3.connect("users.db")
# cursor=connection.cursor()
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS userdetails(id INTEGER PRIMARY KEY,username TEXT,email TEXT UNIQUE,password TEXT)

# ''')
# cursor.execute('''CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY,post TEXT, userid INTEGER,title TEXT, date TEXT, FOREIGN KEY(userid) REFERENCES userdetails(id))''')

# cursor.execute('''CREATE TABLE IF NOT EXISTS feedback(id INTEGER PRIMARY KEY,topic TEXT, concern TEXT, date TEXT, userid INTEGER, FOREIGN KEY(userid) REFERENCES userdatails(id))''')

# cursor.execute('''CREATE TABLE IF NOT EXISTS profilepic(id INTEGER PRIMARY KEY,photo TEXT,userid INTEGER, FOREIGN KEY(userid) REFERENCES userdetails(id))''')
# cursor.execute("DELETE FROM userdetails")
# cursor.close()
# connection.commit()

# import datetime
# import time
# times=datetime.datetime.now()
# print(times.strftime("%B %d  %Y time %H:%M"))


