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


