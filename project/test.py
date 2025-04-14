from db import get_connection
import mysql.connector  # Import this to handle mysql.connector.Error

try:
    conn = get_connection()
    print("Connection successful!")
    conn.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")