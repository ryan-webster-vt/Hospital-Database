import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME')
}

def get_connection():
    """
    Create and return a database connection
    """
    try:
        connection = pymysql.connect(**config)
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to the database: {e}")
        raise

def test_connection():
    """
    Test if the database connection works
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"Successfully connected to MariaDB version {version[0]}")
        connection.close()
        return True
    except pymysql.Error as e:
        print(f"Error connecting to the database: {e}")
        return False

if __name__ == '__main__':
    test_connection()
