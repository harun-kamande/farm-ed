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
lists = [
    ('carol', 'carol@gmail.com'),
    ('peter', 'peter@gmail.com'),
    ('jose', 'jose@gmail.com')
]
cursor.execute("CREATE TABLE IF NOT EXISTS details(id INTEGER PRIMARY KEY,username TEXT,email TEXT UNIQUE)")
# cursor.executemany("INSERT INTO details(username,email) VALUES(?,?)",lists)

cursor.execute("SELECT username, email FROM details")
users = cursor.fetchall()



for data in users:
    print(data[1])
print(users)

cursor.close()
connection.commit()
