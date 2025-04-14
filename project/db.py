import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="10.0.116.125",
        user="your_mysql_user",
        password="your_mysql_password",
        database="cs432gX"  # Replace with your group DB (e.g., cs432g14)
    )
