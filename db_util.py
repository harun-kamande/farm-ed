import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        database='farmed',
        port=3306,
        password='harunkamande',
    )


def close_db_connection(connection):
    connection.close()
