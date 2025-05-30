import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection(cims = 1):
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_DATABASE'+cims*'CIMS')
    )