# import sys
# import os
# file=("C")

# nums=[1222,13,1221,3,45656,7,88,99,445,433,4435,5]
# sizew=os.path.getsize(nums)

# print(f"{sizew} bytes")


import sqlite3
connection=sqlite3.connect("User.db")
cursor=connection.cursor()
cursor.execute("CREATE TABLE details(id INTEGER PRIMARY KEY,username TEXT,email TEXT UNIQUE)")
cursor.close()

connection.commit()
connection.close()