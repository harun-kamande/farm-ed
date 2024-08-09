import mysql.connector
import os


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        database='farmed',
        port=3306,
        # Accessing my db password from my Os environment variable
        password=os.environ.get('mydb'),
    )
