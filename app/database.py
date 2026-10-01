import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="easo1234",
            database="smart_service"
        )

        if connection.is_connected():
            print("MySQL database connected successfully!")
            return connection

    except Error as e:
        print("Database connection failed:", e)

    return None