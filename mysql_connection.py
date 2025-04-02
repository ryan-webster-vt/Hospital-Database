import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration from environment variables
config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'hospital')
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
        
        # Test if we can connect and access tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Successfully connected to {config['database']} database")
        print(f"Available tables: {', '.join([table[0] for table in tables])}")
        
        # Get sample data
        cursor.execute("SELECT COUNT(*) FROM patients")
        count = cursor.fetchone()[0]
        print(f"Number of patients in database: {count}")
        
        connection.close()
        return True
    except pymysql.Error as e:
        print(f"Error connecting to the database: {e}")
        return False

if __name__ == '__main__':
    # Test the connection when running this file directly
    test_connection()
